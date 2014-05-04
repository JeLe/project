from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, time
from math import sin,cos,sqrt,pi
import numpy
from random import *
import Line_Runner

#make door and wall objetcs common to objects easier to use. If static, they sould only be calculated once and should be in a seperate list
#wall objects will be made like they are now, excepet add sort of vertices and take only extremes into account. That will lighten the memory use.


#all global variables
ESCAPE = '\033'
game = 0

# Number of the glut window.
window = 0
alpha = 0
transz = 0
teta = 0
xold = 600

forward = 0
direction = 0

#colors with numpy
cyan = numpy.array((0., .8, .8, 1.), 'f')
red = numpy.array((1., 0., 0., 1.), 'f')
white = numpy.array((1., 1., 1., 1.), 'f')

#wall and door buffers
walls = []
gates = []



########################################
#ALL THE OBJECT CLASSES

#All main vertex lists must be self.vertexList, except for gates and wall, et encore :)...


class wall (object):
    def __init__(self, thingToWall):
        self.getPoints(thingToWall)
        self.getPoints(thingToWall)
        walls.append(self)


    def getPoints(self, thingToWall):
        xmin = thingToWall.vertexList[0][0]
        zmin = thingToWall.vertexList[0][2]
        xmax = thingToWall.vertexList[0][0]
        zmax = thingToWall.vertexList[0][2]
        for thing in thingToWall.vertexList :
            if thing[0] < xmin:
                xmin = thing[0]
            if thing[2] < zmin:
                zmin = thing[2]
            if thing[0] > xmax:
                xmax = thing[0]
            if thing[2] > zmax:
                zmax = thing[2]


        self.vertexList = [[xmin,0, zmax], [xmax, 0, zmax], [xmax, 0, zmin], [xmin,0, zmin]]

    def  noneShallPass(self):
        if self.vertexList[0][0]<=myBonhomme.Ax<=self.vertexList[1][0] and self.vertexList[2][2]<=myBonhomme.Az<=self.vertexList[0][2] : #this condition is kinda crappy..
            print("We don't need no education!")
            return 1 #returns 1...
        else :
            return 0


class gate (object):
    def __init__ (self, list, id):
        self.vertexList = list
        gates.append(self)
        self.id = id
    
    def checkifgate(self):
        if self.vertexList[0][0]<myBonhomme.Ax<self.vertexList[1][0] and self.vertexList[2][2]<myBonhomme.Az<self.vertexList[0][2] :
            return self.id
        else :
            print("not Youpi")
            return 0

class quad(object):
    def __init__(self, name, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz, red, green, blue):
        self.name = name
        self.type = "static"
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
        self.red = red
        self.green = green
        self.blue = blue
        #we get the vertices here in init because it's static
        self.getPoints()
        self.normalList=getNormals(self.vertexList)

    #    self.wall = wall(self)

    def getPoints(self):
        self.vertexList = [[self.Ax, self.Ay, self.Az], [self.Ax+self.Vx, self.Ay+self.Vy, self.Az+self.Vz],[self.Ax+self.Vx+self.Wx, self.Ay+self.Vy+self.Wy, self.Az+self.Vz+self.Wz], [self.Ax+self.Wx, self.Ay+self.Wy, self.Az+self.Wz]]

    def draw(self):

        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        counter = 0
        for vertex in self.vertexList:

            glNormal3f(0., -1., 0.)
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()



#this is where you put your dude classes
unite = .3
class foot (object):
    def __init__(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        global unite
        x = self.Ax
        y = self.Ay
        z = self.Az

        self.footVertexList = [[x, y, z], [x+2*unite, y , z], [x+2*unite, y, z+3*unite], [x, y, z+3*unite],
                               [x, y, z], [x+2*unite, y , z], [x+2*unite, y+unite , z], [x, y+unite, z],
                               [x, y, z], [x, y+unite, z], [x, y+unite, z+3*unite], [x, y, z+3*unite],
                               [x, y, z+3*unite], [x, y+unite, z+3*unite], [x+2*unite, y+unite, z+3*unite], [x+2*unite, y, z+3*unite],
                               [x+2*unite, y , z], [x+2*unite, y+unite , z], [x+2*unite, y+unite , z+3*unite], [x+2*unite, y, z+3*unite],
                               [x, y+unite, z], [x+2*unite, y+unite, z], [x+2*unite, y+unite, z+3*unite],[x, y+unite, z+3*unite]]


class jambe (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        global unite
        x = self.Ax
        y = self.Ay+unite
        z = self.Az
        self.jambeVertexList = [[x, y, z], [x, y+8*unite, z], [x+2*unite, y+8*unite, z], [x+2*unite, y, z],
                                [x, y, z], [x, y+8*unite, z], [x, y+8*unite, z+2*unite], [x, y, z+2*unite],
                                [x+2*unite, y, z], [x+2*unite, y+8*unite, z], [x+2*unite, y+8*unite, z+unite], [x+2*unite, y, z+unite],
                                [x, y, z+2*unite], [x, y+8*unite, z+2*unite], [x+2*unite, y+8*unite, z+2*unite], [x+2*unite, y, z+2*unite]]


class torse (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        global unite
        x = self.Ax
        y = self.Ay+9*unite
        z = self.Az
        self.torseVertexList = [[x, y, z], [x, y+7*unite, z], [x+5*unite, y+7*unite, z], [x+5*unite, y, z],
                                [x, y, z], [x, y+7*unite, z], [x, y+7*unite, z+2*unite], [x, y, z+2*unite],
                                [x+5*unite, y, z], [x+5*unite, y+7*unite, z], [x+5*unite, y+7*unite, z+2*unite], [x+5*unite, y, z+2*unite],
                                [x, y, z+2*unite], [x, y+7*unite, z+2*unite], [x+5*unite, y+7*unite, z+2*unite], [x+5*unite, y, z+2*unite]]

class brazo (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        global unite
        x = self.Ax
        y = self.Ay+16*unite
        z = self.Az
        self.brazoVertexList = [[x, y, z+0.5*unite], [x-unite, y, z+0.5*unite], [x-unite, y, z+1.5*unite], [x, y, z+1.5*unite],
                                [x, y, z+0.5*unite], [x-unite, y, z+0.5*unite], [x-unite, y-9*unite, z+0.5*unite], [x, y-9*unite, z+0.5*unite],
                                [x-unite, y, z+0.5*unite], [x-unite, y, z+1.5*unite], [x-unite, y-9*unite, z+1.5*unite], [x-unite, y-9*unite, z+0.5*unite],
                                [x, y, z+0.5*unite], [x, y, z+1.5*unite], [x, y-9*unite, z+1.5*unite], [x, y-9*unite, z+0.5*unite],
                                [x, y, z+1.5*unite], [x-unite, y, z+1.5*unite], [x-unite, y-9*unite, z+1.5*unite], [x, y-9*unite, z+1.5*unite],
                                [x, y-9*unite, z+0.5*unite], [x-unite, y-9*unite, z+0.5*unite], [x-unite, y-9*unite, z+1.5*unite], [x, y-9*unite, z+1.5*unite]]

class cou (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        global unite
        x = self.Ax+2*unite
        y = self.Ay+16*unite
        z = self.Az
        self.couVertexList = [[x, y, z+0.5*unite], [x+unite, y, z+0.5*unite], [x+unite, y+unite, z+0.5*unite], [x, y+unite, z+0.5*unite],
                              [x, y, z+0.5*unite], [x, y+unite, z+0.5*unite], [x, y+unite, z+1.5*unite], [x, y, z+1.5*unite],
                              [x, y, z+1.5*unite], [x, y+unite, z+1.5*unite], [x+unite, y+unite, z+1.5*unite], [x+unite, y, z+1.5*unite],
                              [x+unite, y, z+0.5*unite], [x+unite, y+unite, z+0.5*unite], [x+unite, y+unite, z+1.5*unite], [x+unite, y, z+1.5*unite]]

class kopf (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        global unite
        x = self.Ax+unite
        y = self.Ay+17*unite
        z = self.Az
        self.kopfVertexList = [[x, y, z], [x+3*unite, y, z], [x+3*unite, y, z+3*unite], [x, y, z+3*unite],
                               [x, y, z], [x+3*unite, y, z], [x+3*unite, y+3*unite, z], [x, y+3*unite, z],
                               [x, y, z], [x, y+3*unite, z], [x, y+3*unite, z+3*unite], [x, y, z+3*unite],
                               [x, y, z+3*unite], [x+3*unite, y, z+3*unite], [x+3*unite, y+3*unite, z+3*unite], [x, y+3*unite, z+3*unite],
                               [x+3*unite, y, z], [x+3*unite, y+3*unite, z], [x+3*unite, y+3*unite, z+3*unite], [x+3*unite, y, z+3*unite],
                               [x, y+3*unite, z], [x+3*unite, y+3*unite, z], [x+3*unite, y+3*unite, z+3*unite], [x, y+3*unite, z+3*unite]]

class bonhomme (object):
    def __init__(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.type = "moving"

    def getPoints(self):
        global unite
        myFoot = foot(self.Ax, self.Ay, self.Az)
        myFoot.getPoints()
        myFoot2 = foot(self.Ax+3*unite, self.Ay, self.Az)
        myFoot2.getPoints()
        maJambe = jambe(self.Ax, self.Ay, self.Az)
        maJambe.getPoints()
        maJambe2 = jambe(self.Ax+3*unite, self.Ay, self.Az)
        maJambe2.getPoints()
        myTorse = torse(self.Ax, self.Ay, self.Az)
        myTorse.getPoints()
        miBrazo = brazo(self.Ax, self.Ay, self.Az)
        miBrazo.getPoints()
        miBrazo2 = brazo(self.Ax+6*unite, self.Ay, self.Az)
        miBrazo2.getPoints()
        monCou = cou(self.Ax, self.Ay, self.Az)
        monCou.getPoints()
        meineKopf = kopf(self.Ax, self.Ay, self.Az)
        meineKopf.getPoints()
        self.vertexList = []
        self.vertexList.extend(myFoot.footVertexList)
        self.vertexList.extend(maJambe.jambeVertexList)
        self.vertexList.extend(myFoot2.footVertexList)
        self.vertexList.extend(maJambe2.jambeVertexList)
        self.vertexList.extend(myTorse.torseVertexList)
        self.vertexList.extend(miBrazo.brazoVertexList)
        self.vertexList.extend(miBrazo2.brazoVertexList)
        self.vertexList.extend(monCou.couVertexList)
        self.vertexList.extend(meineKopf.kopfVertexList)

        self.normalList = getNormals(self.vertexList)

    def draw(self):
        self.getPoints()
        glBegin(GL_QUADS)
        counter = 0
        for item in self.vertexList:
            #this works because we enabled it in init.
            #so if we need ambient, diffuse and specular lighting I don't know if it's wise...
            glColor3f(0.9, 0.9, 0.9)
            #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, cyan)
            glNormal3f(self.normalList[counter][0],self.normalList[++counter][1],self.normalList[++counter][2])
            glVertex3f(item[0], item[1], item[2])
        #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, white)
        glEnd()

    def move(self):
        global forward
        global direction
        #ok so direction devient le coefi dir de ladroite sur laquelle se deplace le bnhomme, on incremente de ce qu'on veut siur x, on calcule z et voila...
        #pb : on voit pas quand il tourne...
        oldX = self.Ax
        oldZ = self.Az
        if forward != 0:
            self.Az += .01*forward
        if direction != 0:
            self.Ax += .02*direction
        for item in walls:
            if item.noneShallPass()==1: #one means it's on the wall !!!
                self.Ax = oldX
                self.Az = oldZ


#END OF DUDE
machineUnit = 3

class machine(object):
    def __init__(self,name,Ax,Ay,Az,Vx,Vy,Vz):
        self.name=name
        self.Ax=Ax
        self.Ay=Ay
        self.Az=Az
        self.Vx=Vx
        self.Vy=Vy
        self.Vz=Vz
        self.type = "static"
        self.getPoints()
        self.normalList = getNormals(self.vertexList)
        self.myWall = wall(self)
        self.myGate = gate(self.gateList, self.name)

    def getPoints(self):
        global machineUnit
        #alors au final j'avais raconte n'importe quoi, pour que ca marche vraiment, il faut deux vecteurs!! Alors pour simplifier la tache, on va reutiliser la premiere classe de Graal Corp, la classe quad !
        #je fais donc un quad, avec le point et les deux vecteurs que il faudra maintenant donner a la creation de ta machine.
        self.start = quad("machine first", self.Ax, self.Ay, self.Az, 0.5*machineUnit*self.Vx, self.Ay, 0.5*machineUnit*self.Vz, -0.6*machineUnit*self.Vz, self.Ay, -0.6*machineUnit*self.Vx, 1., 1., 0.).vertexList #mais je n'en garde que la liste de vertexs. De cette liste, qui represente les points de ton premier carre (celui du dessous), je vais recuperer les quatres points A, B, C, D, qui vont servir a redessiner tous les autres :)
        #de plus, la carrosserie est en acier inoxidable, mais en vrai, pour faire le vecteurW de pour la classe quad, j'ai inverse le *self.Ax et le * self.Az dans les coordonnees, parce que en gros, si c'est pas l'un c'est l'autre, je t'expliquerai ca plus mieux un jour ou je ne prends pas l'avion !
        #alors decollage a 10:20, on est audessus de la mer a 10:30 ! # 3 minutes pour traverser la manche??? #11 :00 , re audessus de la mer ? y'a top de nuages on dirait qu'on survole le pole nord ( les pauvres anglzais !! hihi :) # ah non en fait on peut toujours s'ecraser sur un patelin...  ! 11:06 ohhhh des montagnes, avec des lacs et un tout petit peu de glace.. et la mer derriere ?? 11:11  :on viens de passer un estuaire... Et cette machine est tres galere !! mais c'est bon y'a du sprite !!!! et y'a plein d'eoliennes dans les montagnes.
        #11:20 deuxieme estuaire, avec une grosse ville et une petite lagune.. 11:23 les montagnes ont grandi et veilent aller se beigner !!

        self.Ax = self.start[0][0]
        self.Ay = self.start[0][1]
        self.Az = self.start[0][2]

        self.Bx = self.start[1][0]
        self.By = self.start[1][1]
        self.Bz = self.start[1][2]

        self.Cx = self.start[2][0]
        self.Cy = self.start[2][1]
        self.Cz = self.start[2][2]

        self.Dx = self.start[3][0]
        self.Dy = self.start[3][1]
        self.Dz = self.start[3][2]

        self.gateList = [[self.Bx, 1, self.Bz], [self.Bx+0.5*machineUnit*self.Vx, 1, self.Bz+0.5*machineUnit*self.Vz], [self.Cx+0.5*machineUnit*self.Vx, 1, self.Cz+0.5*machineUnit*self.Vz], [self.Cx, 1, self.Cz]]

        self.vertexList = [[self.Ax,self.Ay,self.Az],[self.Bx,self.By,self.Bz], [self.Cx,self.Cy,self.Cz], [self.Dx,self.Dy,self.Dz],

                           #et maintenat qu'on a les quatres points de la base de la machine qui sont calcules avec des vecteurs, on calcule les autres points a partir de ceux la, et avec les vecteurs de temps en temps ausssi! Les vecteurs ne servent a rien uniquement quand il n'y a que y qui change : quand on va vers le haut quoi !
                           [self.Bx, self.By+0, self.Bz+0 ],[self.Cx, self.Cy+0, self.Cz],[self.Cx, self.Cy+0.6*machineUnit, self.Cz],[self.Bx, self.By+0.6*machineUnit, self.Bz],

                           [self.Bx, self.By+0.6*machineUnit, self.Bz],[self.Cx, self.Cy+0.6*machineUnit, self.Cz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.7*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Bx+0.1*machineUnit*self.Vx, self.By+0.7*machineUnit, self.Bz+0.1*machineUnit*self.Vz],
                           #11:30, il s comencent deja a servir les repas, ahlala, et y'a plein de nuages, c'est tres joli mais en plus je crois qu'on est re audessus de la mer... et je commence le 3e album du jour vert de la journeee.
                           # et a chaque carre, on repart avec les coords de celui d'avant ! et j'aimerai pas etre sur la mer sous les nuages la tout de suite, qu'est ce qu'il doit faire froid !!
                           [self.Bx+0.1*machineUnit*self.Vx, self.By+0.7*machineUnit, self.Bz+0.1*machineUnit*self.Vz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.7*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.8*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Bx+0.1*machineUnit*self.Vx, self.By+0.8*machineUnit, self.Bz+0.1*machineUnit*self.Vz],
                           # pff, le paysage est vraiment ennuyeux, je vais pouvoir me concentrer ! (il doit etre a peu pres midi, midi et quart...
                           #je viens de trouver le bug dans mes vecteurs, il est 12:40, on arrive je pense sur le groenland, ca on vient de toucher TERRE ! (a la cristophe colomb) et qyue y'a de la glace partout, c'est rigolo ! (et je viens de voir sur l'ecran de gens devant que dehors il fait -54... Farenheit!! (ca fait -47 celsius)la neige est belle !Bon, a mes vecteurs.. Mais il y a un enorme trou dans une montagne ! ce doit etre un volcan !!
                           #j'en ai marre cette machine ne fonctionne pas du tout, et les montagnes enneigees me donnent envie d'aller faire du ski !
                           #une heure et demie, ca y est ca marche, et ben, c'est pas splendide les vecteurs ! et c'est nul les gens derriee avaeint le soleil dans la tete, du coup je ne peux plus regarder la mer... Parce que c'est grand la mer en fait... (on a passe la petite peninsule du groenland il y a 15mn..
                           # bon je vais essayer de finir la machine dans la demi heure...
                           #plutot 3/4 d'heure...
                           [self.Bx+0.1*machineUnit*self.Vx, self.By+0.8*machineUnit, self.Bz+0.1*machineUnit*self.Vz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.8*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+0.9*machineUnit, self.Cz-0.1*machineUnit*self.Vz], [self.Bx-0.1*machineUnit*self.Vx, self.By+0.9*machineUnit, self.Bz-0.1*machineUnit*self.Vz],

                           [self.Bx-0.1*machineUnit*self.Vx, self.By+0.9*machineUnit, self.Bz-0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+0.9*machineUnit, self.Cz-0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+1.3*machineUnit, self.Cz-0.1*machineUnit*self.Vz],[self.Bx-0.1*machineUnit*self.Vx, self.By+1.3*machineUnit, self.Bz-0.1*machineUnit*self.Vz],

                           [self.Bx-0.1*machineUnit*self.Vx, self.By+1.3*machineUnit, self.Bz-0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+1.3*machineUnit, self.Cz-0.1*machineUnit*self.Vz], [self.Cx, self.Cy+1.4*machineUnit, self.Cz],[self.Bx, self.By+1.4*machineUnit, self.Bz],

                           [self.Bx, self.By+1.4*machineUnit, self.Bz],[self.Cx, self.Cy+1.4*machineUnit, self.Cz],[self.Cx, self.Cy+1.6*machineUnit, self.Cz],[self.Bx, self.By+1.6*machineUnit, self.Bz],

                           [self.Ax,self.Ay+1.6*machineUnit,self.Az],[self.Bx,self.By+1.6*machineUnit,self.Bz], [self.Cx,self.Cy+1.6*machineUnit,self.Cz], [self.Dx,self.Dy+1.6*machineUnit,self.Dz],

                           [self.Ax+0 ,self.Ay,self.Az+0 ],[self.Dx+0 ,self.Dy, self.Dz],[self.Dx+0 ,self.Dy+1.6*machineUnit, self.Dz],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az+0],
                           #il est deux heures et demie, j'arrive pas du tout a me concentrer a cause de tous les films sur tous les ecrans de tout le monde, forcement le mien il ne marche pas !!! et je crois qu'on est pas top loin du cercle polaire, parce que j'ai jete un oeuil dehors (ca fait mal), c'est que de la glace !! magnifique, je qualifierai meme ca de , miraculeux ! (tiens voila ce que je vais regarder parce que j'en ai marre de cette machine !

                           #the sides (dark or not, as you want)
                           #c'est grand le groenland... Et la il est 4:30, je commence a trouver le temps long...
                           [self.Ax ,self.Ay,self.Az], [self.Bx-0.1*machineUnit*self.Vx,self.By,self.Bz-0.1*machineUnit*self.Vz], [self.Bx-0.1*machineUnit*self.Vx,self.By+1.6*machineUnit,self.Bz-0.1*machineUnit*self.Vz], [self.Ax, self.Ay+1.6*machineUnit, self.Az],
                           [self.Dx ,self.Dy,self.Dz], [self.Cx-0.1*machineUnit*self.Vx,self.Cy,self.Cz-0.1*machineUnit*self.Vz], [self.Cx-0.1*machineUnit*self.Vx,self.Cy+1.6*machineUnit,self.Cz-0.1*machineUnit*self.Vz], [self.Dx, self.Dy+1.6*machineUnit, self.Dz]
                           #[self.Ax+0,self.Ay+0,self.Az+0],[self.Ax+0.3*machineUnit -0.2,self.Ay+0 ,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+1.6*machineUnit +1.6,self.Az+0 ],[self.Ax+0 -0.5,self.Ay+1.6*machineUnit +1.6,self.Az+0 ],

                           #[self.Ax+0.3*machineUnit -0.2,self.Ay+0 ,self.Az+0 ],[self.Ax+0.5*machineUnit ,self.Ay+0 ,self.Az+0 ],[self.Ax+0.5*machineUnit ,self.Ay+0.6*machineUnit +0.6,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.6*machineUnit +0.6,self.Az+0 ],

                           #[self.Ax+0.5*machineUnit ,self.Ay+0.6*machineUnit +0.6,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.6*machineUnit +0.6,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.7*machineUnit +0.7,self.Az+0 ],[self.Ax+0.6*machineUnit +0.1,self.Ay+0.7*machineUnit +0.7,self.Az+0 ],

                           #[self.Ax+0.6*machineUnit +0.1,self.Ay+0.7*machineUnit +0.7,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.7*machineUnit +0.7,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.9*machineUnit ,self.Az+0 ],[self.Ax+0.6*machineUnit +0.1,self.Ay+0.8*machineUnit +0.8,self.Az+0 ],

                           #[self.Ax+0.3*machineUnit -0.2,self.Ay+1.3*machineUnit +1.3,self.Az+0 ],[self.Ax+0.4*machineUnit -0.1,self.Ay+1.4*machineUnit +1.4,self.Az+0 ],[self.Ax+0.4*machineUnit -0.1,self.Ay+1.6*machineUnit +1.6,self.Az+0 ],[self.Ax+0.3*machineUnit -0.2,self.Ay+1.6*machineUnit +1.6,self.Az+0 ],



                           #[self.Ax+0 -0.5,self.Ay+0 ,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+0 ,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+1.6*machineUnit +1.6,self.Az-0.6*machineUnit +1.6],[self.Ax+0 -0.5,self.Ay+1.6*machineUnit +1.6,self.Az-0.6*machineUnit -0.6],

                           #[self.Ax+0.3*machineUnit -0.2,self.Ay+0 ,self.Az-0.6*machineUnit -0.6],[self.Ax+0.5*machineUnit ,self.Ay+0 ,self.Az-0.6*machineUnit -0.6],[self.Ax+0.5*machineUnit ,self.Ay+0.6*machineUnit +0.6,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.6*machineUnit +0.6,self.Az-0.6*machineUnit -0.6],

                           #[self.Ax+0.5*machineUnit ,self.Ay+0.6*machineUnit +0.6,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.6*machineUnit +0.6,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.7*machineUnit +0.7,self.Az-0.6*machineUnit -0.6],[self.Ax+0.6*machineUnit +0.1,self.Ay+0.7*machineUnit +0.7,self.Az-0.6*machineUnit -0.6],

                           #[self.Ax+0.6*machineUnit +0.1,self.Ay+0.7*machineUnit +0.7,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.7*machineUnit +0.7,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+0.9*machineUnit +0.9,self.Az-0.6*machineUnit -0.6],[self.Ax+0.6*machineUnit +0.1,self.Ay+0.8*machineUnit +0.8,self.Az-0.6*machineUnit -0.6],

                           #[self.Ax+0.3*machineUnit -0.2,self.Ay+1.3*machineUnit +1.3,self.Az-0.6*machineUnit -0.6],[self.Ax+0.4*machineUnit -0.1,self.Ay+1.4*machineUnit +1.4,self.Az-0.6*machineUnit -0.6],[self.Ax+0.4*machineUnit -0.1,self.Ay+1.6*machineUnit +1.6,self.Az-0.6*machineUnit -0.6],[self.Ax+0.3*machineUnit -0.2,self.Ay+1.6*machineUnit +1.6,self.Az-0.6*machineUnit -0.6]
                           ]




    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(1., 1., 1.)
        counter = 0
        for item in self.vertexList:
            glNormal3f(self.normalList[counter][0],self.normalList[++counter][1],self.normalList[++counter][2])
            glVertex3f(item[0], item[1], item[2])
        glEnd()
        glBegin(GL_LINES)
        glColor3f(1., 0., 0.)
        counter =0
            # for item in self.normalList :
            #counter+=3
            #glVertex3f(item[0], item[1], item[2])
            #glVertex3f(self.vertexList[counter][0], self.vertexList[counter][1], self.vertexList[counter][2])

        glEnd()



#And in init(if static) or in getVertices (if not static) add this line self.normalList=CalculateNormal(self)
def getNormals(vertexList) :
    normalList=[]
    counter=0
    while counter!=len(vertexList):
        Xa=vertexList[counter+3][0]-vertexList[counter][0]
        Xb=vertexList[counter+1][0]-vertexList[counter][0]
        Ya=vertexList[counter+3][1]-vertexList[counter][1]
        Yb=vertexList[counter+1][1]-vertexList[counter][1]
        Za=vertexList[counter+3][2]-vertexList[counter][2]
        Zb=vertexList[counter+1][2]-vertexList[counter][2]
        N=[Ya*Zb-Za*Yb, Za*Xb-Xa*Zb, Xa*Yb-Ya*Xb]
        normalList.append(N)
        counter+=4

    return(normalList)


#now our GL functions. DraxFunc is first cause most important



# The main drawing function.
def DrawGLScene():
    # Clear The Screen And The Depth Buffer, load the current and only matrix
    global alpha, transz, teta, game

    if game ==1 and Line_Runner.stop == 0:
        Line_Runner.LRdrawGLScene()
    else :
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()

    # push the origin of (x, y, z) to wher you can see it
    #and go a little higher than the origin to be above the floor
    #without having to rotate the whole thing..
        glTranslatef(0., -3.0, -15.0)

    #Here are the movements you do when you move around or for/backwards
    #Hey Ben, I found out you need to do all your translations first
    #then you rotations, or you get wierd stuff...
        glTranslatef(0,0,transz)
        glRotatef(alpha, 0, 1, 0)
        glRotatef(teta, 0, 0, 1)


    ######################################
    #here we start the light stuff !!

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, numpy.array((0.50, 0.50, 0.50, 0.5), 'f'))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, numpy.array((1., 0., 0., 1.0), 'f'))


    #glEnable(GL_LIGHT1)

        lightpos = numpy.array((5., 2., 0., 0.), 'f')
        lightdir = numpy.array((1, 0, 0), 'f')
        glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, lightdir)
        glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 90)



    #the line is the lamps stand !
        glBegin(GL_LINES)
        glColor3f(0,0,1)
        glVertex3f(-5,.3,5)
        glVertex3f(5,.3,5)
        glEnd()

    #drawables is the list that has all the object instances we will need to draw.
        for thing in drawables :
            if thing.type == "non static":
                thing.move()
            thing.draw() #this includes refreshing vertices for non statics

        myBonhomme.move()
        myBonhomme.draw()

        glutSwapBuffers()



def keyPressed(*args):
    global transz, teta, alpha, game

    # If escape or q is pressed, kill everything.
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()

    #manual rotations and zooms
    #OK THE TETA IS CRAP but can be cool for tests..
    if args[0] == 'e' and teta<30:
        teta += 2
    if args[0] == 'd' and teta>-45:
        teta += -2
    if args[0] == 's':
        transz += -1.
    if args[0]== 'z':
        transz += 1.
    if args[0]== 'h':
        game = 1
        Line_Runner.stop = 0
        #only for 3D stuff...
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

    if args[0]== 't' or Line_Runner.stop == 1:
        game = 0
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    if game == 1:
        Line_Runner.LRkeyPressed(args)

def keyReleased(*args):
    global game
    if game ==1 :
        Line_Runner.LRkeyReleased(args)

def specialKeyPressed(key, x, y):
    global direction, forward, game

    #to move the dude...
    if key == GLUT_KEY_UP :
        forward = 1
    if key == GLUT_KEY_DOWN:
        forward = -1
    if key == GLUT_KEY_LEFT:
        direction = -1
    if key == GLUT_KEY_RIGHT:
        direction = 1



def specialKeyReleased(key, x, y):
    global forward, direction

    if key == GLUT_KEY_UP :
        forward = 0
    if key == GLUT_KEY_DOWN:
        forward = 0
    if key == GLUT_KEY_LEFT:
        direction = 0
    if key == GLUT_KEY_RIGHT:
        direction = 0



def myMouseMove (x, y):
    global alpha
    global xold
    #the mouse is now sensitive ! the faster you go the more you turn ! :)
    if xold<x:
        diff = x-xold
        alpha = diff

    if xold>x:
        diff = xold-x
        alpha = -diff

    glutPostRedisplay()


def Mouseclick (button, state, x, y):
    #state is to do stuff while you are only pressed down a,d haven't released the mouse button yet for example (down gives state 0..)
    if GLUT_LEFT_BUTTON == button and state==0:
        for element in gates :
            if element.checkifgate() != 0 :
                print(element.checkifgate())
                if element.checkifgate() == 'LR':
                    global game
                    game = 1
                    Line_Runner.stop = 0
                    #only for 3D stuff...
                    glDisable(GL_DEPTH_TEST)
                    glDisable(GL_LIGHTING)


    if GLUT_RIGHT_BUTTON == button and state == 0 :
        print ("right_click")


#these are the inital functions
def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_RESCALE_NORMAL)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)


    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def reSizeGLScene(Width, Height):
    if Height == 0:						        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)		               # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 50)
    window = glutCreateWindow("Lucile's Dude :)")
    InitGL(640, 480)
    glutSetWindow(window)

    #these are the callbacks to the functions that actually do something...
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(reSizeGLScene)

    glutFullScreen()

    glutIgnoreKeyRepeat(1)
    glutKeyboardFunc(keyPressed)
    glutKeyboardUpFunc(keyReleased)

    glutSpecialFunc(specialKeyPressed)
    #le sprite c'est trop bon !!!!! :)
    glutSpecialUpFunc(specialKeyReleased)

    glutMouseFunc(Mouseclick)
    glutPassiveMotionFunc(myMouseMove)

    glutMainLoop()

#here is where we instanciate all the objects....
#must be here or all necessary funcs haven't apeared yet...
#we now need to get the walls for all the machines and ... youpii
drawables = [quad("floor", -5, 0.0, 5, 0., 0.0, -10., 10., 0.0, 0., 1.0, 1., 0.), machine("LR", 0, 0, 0, 1, 0, 0), machine("test", -3, 0, -3, 0, 0, 1)]
myBonhomme = bonhomme(-3.0,0.0,0.1)



main()
