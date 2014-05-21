from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, time
from math import sin,cos,sqrt,pi
import numpy
from random import *
import Line_Runner, snake, tetris


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




class wall (object):
    def __init__(self, thingToWall):
        self.getPoints(thingToWall)
        self.getPoints(thingToWall)
        walls.append(self)


    def getPoints(self, thingToWall):
        #oui j'aurais du utiliser les fonctions min et max de python, mais au final la elles sont faites maison...
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
        #ici on verifie que le bonhomme n'aissaie pas de passer a travers un mur
        if self.vertexList[0][0]<=myBonhomme.Ax<=self.vertexList[1][0] and self.vertexList[2][2]<=myBonhomme.Az<=self.vertexList[0][2] : #this condition is kinda crappy.. Because we only test one side of the dude
            print("We don't need no education!") # on est dans un Wall ou pas ? :)
            return 1 #returns 1...
        else :
            return 0


class gate (object):
    def __init__ (self, list, id):
        self.vertexList = list
        gates.append(self)
        self.id = id
    #ici on regarde si le bonhomme est dans une porte ou pas. Celles ci declanchent un jeu, selon devant quelle borne on est, a qui est associe une porte et donc un jeu
    def checkifgate(self):
        a = min(self.vertexList[0][0], self.vertexList[1][0], self.vertexList[2][0])
        b = max(self.vertexList[0][0], self.vertexList[1][0], self.vertexList[2][0])
        c = min(self.vertexList[0][2], self.vertexList[1][2], self.vertexList[2][2])
        d = max(self.vertexList[0][2], self.vertexList[1][2], self.vertexList[2][2])
        if a<myBonhomme.Ax<b and c<myBonhomme.Az<d :#meme probleme avec la condition que pour les murs
            return self.id#cet identifient definit quel jeu sera lance
        else :
            return 0

#le tout premier objet de tout le projet. Une instance de celui ci est un carre definit par un point, deux vecteurs et une couleur (avec ses coordonnes RVB)
class quad(object):
    def __init__(self, name, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz, red, green, blue):
        self.name = name
        self.type = "static" # ce type est discutable...
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
        self.normalList=getNormals(self.vertexList) #le vecteur normal associe au carre... Cela devait servir pour la lumiere, mais nous avons decide d'implementer celle ci ulterieurement.

#la methode qui calcule les 4 points du carre a partir du point et des 2 vecteurs de l'initialisation
    def getPoints(self):
        self.vertexList = [[self.Ax, self.Ay, self.Az], [self.Ax+self.Vx, self.Ay+self.Vy, self.Az+self.Vz],[self.Ax+self.Vx+self.Wx, self.Ay+self.Vy+self.Wy, self.Az+self.Vz+self.Wz], [self.Ax+self.Wx, self.Ay+self.Wy, self.Az+self.Wz]]

#la methode qui dessine le carre a l'ecran, grace a OpenGl. Cette methode ne doit etre appele a partir de DrawGLScene directement ou indirectement
    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        counter = 0
        for vertex in self.vertexList:
            glNormal3f(0., -1., 0.) #une normale arbitraire, vu que l'implementation de la lumiere doit attendre, cela n'a aucune incidence.
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()



#deubut des classes associees au bonhomme. Les noms parlent d'eux meme ( ou pas :)

unite = .3

class foot (object):
    def __init__(self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
    
    
    
    def getPoints(self):
        global unite
        self.start = quad("foot", self.Ax, self.Ay, self.Az, 2*unite*self.Vx, self.Vy, 2*unite*self.Vz, -3*unite*self.Wx, self.Wy, -3*unite*self.Wz, 1., 1., 0.).vertexList
        
        self.x = self.start[0][0]
        self.y = self.start[0][1]
        self.z = self.start[0][2]
        
        self.Bx = self.start[1][0]
        self.By = self.start[1][1]
        self.Bz = self.start[1][2]
        
        self.Cx = self.start[2][0]
        self.Cy = self.start[2][1]
        self.Cz = self.start[2][2]
        
        self.Dx = self.start[3][0]
        self.Dy = self.start[3][1]
        self.Dz = self.start[3][2]
        
        self.footVertexList = [[self.x,self.y,self.z], [self.Bx,self.By,self.Bz], [self.Cx,self.Cy,self.Cz], [self.Dx,self.Dy,self.Dz],
                               [self.x,self.y,self.z], [self.Bx,self.By,self.Bz], [self.Bx,self.By+unite,self.Bz], [self.x,self.y+unite,self.z],
                               [self.x,self.y,self.z], [self.x,self.y+unite,self.z], [self.Dx,self.Dy+unite,self.Dz], [self.Dx,self.Dy,self.Dz],
                               [self.Dx,self.Dy,self.Dz], [self.Dx,self.Dy+unite,self.Dz], [self.Cx,self.Cy+unite,self.Cz], [self.Cx,self.Cy,self.Cz],
                               [self.Bx,self.By,self.Bz], [self.Bx,self.By+unite,self.Bz], [self.Cx,self.Cy+unite,self.Cz], [self.Cx,self.Cy,self.Cz],
                               [self.x,self.y+unite,self.z], [self.Bx,self.By+unite,self.Bz], [self.Cx,self.Cy+unite,self.Cz],[self.Dx,self.Dy+unite,self.Dz]]





class ashi (object):
    def __init__ (self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
    
    
    
    def getPoints(self):
        global unite
        self.start = quad("ashi", self.Ax, self.Ay, self.Az, 2*unite*self.Vx, self.Vy, 2*unite*self.Vz, -2*unite*self.Wx, self.Wy, -2*unite*self.Wz, 1., 1., 0.).vertexList
        
        self.x = self.start[0][0]
        self.y = self.start[0][1] + unite
        self.z = self.start[0][2]
        
        self.Bx = self.start[1][0]
        self.By = self.start[1][1] + unite
        self.Bz = self.start[1][2]
        
        self.Cx = self.start[2][0]
        self.Cy = self.start[2][1] + unite
        self.Cz = self.start[2][2]
        
        self.Dx = self.start[3][0]
        self.Dy = self.start[3][1] + unite
        self.Dz = self.start[3][2]
        
        self.ashiVertexList = [[self.x, self.y, self.z], [self.x, self.y+8*unite, self.z], [self.Bx, self.By+8*unite, self.Bz], [self.Bx, self.By, self.Bz],
                               [self.x, self.y, self.z], [self.x, self.y+8*unite, self.z], [self.Dx, self.Dy+8*unite, self.Dz], [self.Dx, self.Dy, self.Dz],
                               [self.Bx, self.By, self.Bz], [self.Bx, self.By+8*unite, self.Bz], [self.Cx, self.Cy+8*unite, self.Cz], [self.Cx, self.Cy, self.Cz],
                               [self.Dx, self.Dy, self.Dz], [self.Dx, self.Dy+8*unite, self.Dz], [self.Cx, self.Cy+8*unite, self.Cz], [self.Cx, self.Cy, self.Cz]]





class torso (object):
    def __init__ (self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
    
    
    
    def getPoints(self):
        global unite
        self.start = quad("torso", self.Ax, self.Ay, self.Az, 5*unite*self.Vx, self.Vy, 5*unite*self.Vz, -2*unite*self.Wx, self.Wy, -2*unite*self.Wz, 1., 1., 0.).vertexList
        
        self.x = self.start[0][0]
        self.y = self.start[0][1] + 9*unite
        self.z = self.start[0][2]
        
        self.Bx = self.start[1][0]
        self.By = self.start[1][1] +9*unite
        self.Bz = self.start[1][2]
        
        self.Cx = self.start[2][0]
        self.Cy = self.start[2][1] +9*unite
        self.Cz = self.start[2][2]
        
        self.Dx = self.start[3][0]
        self.Dy = self.start[3][1] +9*unite
        self.Dz = self.start[3][2]
        
        self.torsoVertexList = [[self.x, self.y, self.z], [self.x, self.y+7*unite, self.z], [self.Bx, self.By+7*unite, self.Bz], [self.Bx, self.By, self.Bz],
                                [self.x, self.y, self.z], [self.x, self.y+7*unite, self.z], [self.Dx, self.Dy+7*unite, self.Dz], [self.Dx, self.Dy, self.Dz],
                                [self.Bx, self.By, self.Bz], [self.Bx, self.By+7*unite, self.Bz], [self.Cx, self.Cy+7*unite, self.Cz], [self.Cx, self.Cy, self.Cz],
                                [self.Dx, self.Dy, self.Dz], [self.Dx, self.Dy+7*unite, self.Dz], [self.Cx, self.Cy+7*unite, self.Cz], [self.Cx, self.Cy, self.Cz]]



class brazo (object):
    def __init__ (self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
    
    
    
    def getPoints(self):
        global unite
        self.start = quad("brazo", self.Ax, self.Ay, self.Az, 1*unite*self.Vx, self.Vy, 1*unite*self.Vz, -1*unite*self.Wx, self.Wy, -1*unite*self.Wz, 1., 1., 0.).vertexList
        
        self.x = self.start[0][0] -unite*self.Vx
        self.y = self.start[0][1] +7*unite
        self.z = self.start[0][2] +1.5*unite*self.Vz
        
        self.Bx = self.start[1][0] -unite*self.Vx
        self.By = self.start[1][1] +7*unite
        self.Bz = self.start[1][2] +1.5*unite*self.Vz
        
        self.Cx = self.start[2][0] -unite*self.Vx
        self.Cy = self.start[2][1] +7*unite
        self.Cz = self.start[2][2] +1.5*unite*self.Vz
        
        self.Dx = self.start[3][0] -unite*self.Vx
        self.Dy = self.start[3][1] +7*unite
        self.Dz = self.start[3][2] +1.5*unite*self.Vz
        
        self.brazoVertexList = [[self.x, self.y, self.z], [self.Bx, self.By, self.Bz], [self.Cx, self.Cy, self.Cz], [self.Dx, self.Dy, self.Dz],
                                [self.x, self.y, self.z], [self.x, self.y+9*unite, self.z], [self.Bx, self.By+9*unite, self.Bz], [self.Bx, self.By, self.Bz],
                                [self.x, self.y, self.z], [self.x, self.y+9*unite, self.z], [self.Dx, self.Dy+9*unite, self.Dz], [self.Dx, self.Dy, self.Dz],
                                [self.Dx, self.Dy, self.Dz], [self.Dx, self.Dy+9*unite, self.Dz], [self.Cx, self.Cy+9*unite, self.Cz], [self.Cx, self.Cy, self.Cz],
                                [self.Cx, self.Cy, self.Cz], [self.Cx, self.Cy+9*unite, self.Cz], [self.Bx, self.By+9*unite, self.Bz], [self.Bx, self.By, self.Bz],
                                [self.x, self.y+9*unite, self.z], [self.Bx, self.By+9*unite, self.Bz], [self.Cx, self.Cy+9*unite, self.Cz], [self.Dx, self.Dy+9*unite, self.Dz]]



class cou (object):
    def __init__ (self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
    
    
    def getPoints(self):
        global unite
        self.start = quad("cou", self.Ax, self.Ay, self.Az, 1*unite*self.Vx, self.Vy, 1*unite*self.Vz, -1*unite*self.Wx, self.Wy, -1*unite*self.Wz, 1., 1., 0.).vertexList
        
        self.x = self.start[0][0] +2*unite*self.Vx
        self.y = self.start[0][1] +16*unite
        self.z = self.start[0][2] +.5*unite*self.Vz
        
        self.Bx = self.start[1][0] +2*unite*self.Vx
        self.By = self.start[1][1] +16*unite
        self.Bz = self.start[1][2] +.5*unite*self.Vz
        
        self.Cx = self.start[2][0] +2*unite*self.Vx
        self.Cy = self.start[2][1] +16*unite
        self.Cz = self.start[2][2] +.5*unite*self.Vz
        
        self.Dx = self.start[3][0] +2*unite*self.Vx
        self.Dy = self.start[3][1] +16*unite
        self.Dz = self.start[3][2] +.5*unite*self.Vz
        
        self.couVertexList = [[self.x, self.y, self.z], [self.Bx, self.By, self.Bz], [self.Bx, self.By+unite, self.Bz], [self.x, self.y+unite, self.z],
                              [self.x, self.y, self.z], [self.x, self.y+unite, self.z], [self.Dx, self.Dy+unite, self.Dz], [self.Dx, self.Dy, self.Dz],
                              [self.Bx, self.By, self.Bz], [self.Bx, self.By+unite, self.Bz], [self.Cx, self.Cy+unite, self.Cz], [self.Cx, self.Cy, self.Cz],
                              [self.Dx, self.Dy, self.Dz], [self.Dx, self.Dy+unite, self.Dz], [self.Cx, self.Cy+unite, self.Cz], [self.Cx, self.Cy, self.Cz]]



class kopf (object):
    def __init__ (self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
    
    
    
    def getPoints(self):
        global unite
        self.start = quad("kopf", self.Ax, self.Ay, self.Az, 3*unite*self.Vx, self.Vy, 3*unite*self.Vz, -3*unite*self.Wx, self.Wy, -3*unite*self.Wz, 1., 1., 0.).vertexList
        
        self.x = self.start[0][0] +unite*self.Vx
        self.y = self.start[0][1] +17*unite
        self.z = self.start[0][2]
        
        self.Bx = self.start[1][0] +unite*self.Vx
        self.By = self.start[1][1] +17*unite
        self.Bz = self.start[1][2]
        
        self.Cx = self.start[2][0] +unite*self.Vx
        self.Cy = self.start[2][1] +17*unite
        self.Cz = self.start[2][2]
        
        self.Dx = self.start[3][0] +unite*self.Vx
        self.Dy = self.start[3][1] +17*unite
        self.Dz = self.start[3][2]
        
        self.kopfVertexList = [[self.x, self.y, self.z], [self.Bx, self.By, self.Bz], [self.Cx, self.Cy, self.Cz], [self.Dx, self.Dy, self.Dz],
                               [self.x, self.y, self.z], [self.Bx, self.By, self.Bz], [self.Bx, self.By+3*unite, self.Bz], [self.x, self.y+3*unite, self.z],
                               [self.x, self.y, self.z], [self.x, self.y+3*unite, self.z], [self.Dx, self.Dy+3*unite, self.Dz], [self.Dx, self.Dy, self.Dz],
                               [self.Dx, self.Dy, self.Dz], [self.Cx, self.Cy, self.Cz], [self.Cx, self.Cy+3*unite, self.Cz], [self.Dx, self.Dy+3*unite, self.Dz],
                               [self.Bx, self.By, self.Bz], [self.Bx, self.By+3*unite, self.Bz], [self.Cx, self.Cy+3*unite, self.Cz], [self.Cx, self.Cy, self.Cz],
                               [self.x, self.y+3*unite, self.z], [self.Bx, self.By+3*unite, self.Bz], [self.Cx, self.Cy+3*unite, self.Cz], [self.Dx, self.Dy+3*unite, self.Dz]]



class bonhomme (object):
    def __init__(self, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.Wx = Wx
        self.Wy = Wy
        self.Wz = Wz
        self.type = "moving"
    
    
    
    def getPoints(self):
        global unite
        myFoot = foot(self.Ax, self.Ay, self.Az, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        myFoot.getPoints()
        myFoot2 = foot(self.Ax+3*unite*self.Vx, self.Ay, self.Az+3*unite*self.Vz, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        myFoot2.getPoints()
        watashiNoAshi = ashi(self.Ax, self.Ay, self.Az, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        watashiNoAshi.getPoints()
        watashiNoAshi2 = ashi(self.Ax+3*unite*self.Vx, self.Ay, self.Az+3*unite*self.Vz, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        watashiNoAshi2.getPoints()
        mioTorso = torso(self.Ax, self.Ay, self.Az, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        mioTorso.getPoints()
        miBrazo = brazo(self.Ax, self.Ay, self.Az, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        miBrazo.getPoints()
        miBrazo2 = brazo(self.Ax+6*unite*self.Vx, self.Ay, self.Az+6*unite*self.Vz, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        miBrazo2.getPoints()
        monCou = cou(self.Ax, self.Ay, self.Az, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        monCou.getPoints()
        meineKopf = kopf(self.Ax, self.Ay, self.Az, self.Vx, self.Vy, self.Vz, self.Wx, self.Wy, self.Wz)
        meineKopf.getPoints()
        
        self.vertexList = []
        self.vertexList.extend(myFoot.footVertexList)
        self.vertexList.extend(watashiNoAshi.ashiVertexList)
        self.vertexList.extend(myFoot2.footVertexList)
        self.vertexList.extend(watashiNoAshi2.ashiVertexList)
        self.vertexList.extend(mioTorso.torsoVertexList)
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
            glColor3f(1.0, 0.4, 0.2)
            #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, cyan)
            glNormal3f(self.normalList[counter][0],self.normalList[++counter][1],self.normalList[++counter][2])
            glVertex3f(item[0], item[1], item[2])
        #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, white)
        glEnd()
    
    
    
    def move(self):
        global forward,direction
        oldX = self.Ax
        oldZ = self.Az
        
        if forward != 0:
            self.Az += .025*forward

        if direction != 0:
            self.Ax += .025*direction
        
        for item in walls:
            if item.noneShallPass()==1: #one means it's on the wall !!!
                self.Ax = oldX
                self.Az = oldZ


#Fin de des classes relatives au bonhomme

#debut des machines

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
        #pour que la machine puisse etre tournee dans le bon sens ( vers l'interur de la piece) il faut qu'elle soit entierement calculee a partir d'un quad et de ses vecteurs, comme ca on peut la faire tourner avec les vecteurs !
        self.start = quad("machine first", self.Ax, self.Ay, self.Az, 0.5*machineUnit*self.Vx, self.Ay, 0.5*machineUnit*self.Vz, -0.6*machineUnit*self.Vz, self.Ay, -0.6*machineUnit*self.Vx, 1., 1., 0.).vertexList

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

          
                           [self.Bx, self.By+0, self.Bz+0 ],[self.Cx, self.Cy+0, self.Cz],[self.Cx, self.Cy+0.6*machineUnit, self.Cz],[self.Bx, self.By+0.6*machineUnit, self.Bz],

                           [self.Bx, self.By+0.6*machineUnit, self.Bz],[self.Cx, self.Cy+0.6*machineUnit, self.Cz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.7*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Bx+0.1*machineUnit*self.Vx, self.By+0.7*machineUnit, self.Bz+0.1*machineUnit*self.Vz],
            
                           [self.Bx+0.1*machineUnit*self.Vx, self.By+0.7*machineUnit, self.Bz+0.1*machineUnit*self.Vz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.7*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.8*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Bx+0.1*machineUnit*self.Vx, self.By+0.8*machineUnit, self.Bz+0.1*machineUnit*self.Vz],
           
                           [self.Bx+0.1*machineUnit*self.Vx, self.By+0.8*machineUnit, self.Bz+0.1*machineUnit*self.Vz],[self.Cx+0.1*machineUnit*self.Vx, self.Cy+0.8*machineUnit, self.Cz+0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+0.9*machineUnit, self.Cz-0.1*machineUnit*self.Vz], [self.Bx-0.1*machineUnit*self.Vx, self.By+0.9*machineUnit, self.Bz-0.1*machineUnit*self.Vz],

                           [self.Bx-0.1*machineUnit*self.Vx, self.By+0.9*machineUnit, self.Bz-0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+0.9*machineUnit, self.Cz-0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+1.3*machineUnit, self.Cz-0.1*machineUnit*self.Vz],[self.Bx-0.1*machineUnit*self.Vx, self.By+1.3*machineUnit, self.Bz-0.1*machineUnit*self.Vz],

                           [self.Bx-0.1*machineUnit*self.Vx, self.By+1.3*machineUnit, self.Bz-0.1*machineUnit*self.Vz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy+1.3*machineUnit, self.Cz-0.1*machineUnit*self.Vz], [self.Cx, self.Cy+1.4*machineUnit, self.Cz],[self.Bx, self.By+1.4*machineUnit, self.Bz],

                           [self.Bx, self.By+1.4*machineUnit, self.Bz],[self.Cx, self.Cy+1.4*machineUnit, self.Cz],[self.Cx, self.Cy+1.6*machineUnit, self.Cz],[self.Bx, self.By+1.6*machineUnit, self.Bz],

                           [self.Ax,self.Ay+1.6*machineUnit,self.Az],[self.Bx,self.By+1.6*machineUnit,self.Bz], [self.Cx,self.Cy+1.6*machineUnit,self.Cz], [self.Dx,self.Dy+1.6*machineUnit,self.Dz],

                           [self.Ax+0 ,self.Ay,self.Az+0 ],[self.Dx+0 ,self.Dy, self.Dz],[self.Dx+0 ,self.Dy+1.6*machineUnit, self.Dz],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az+0],
         
                               #les cotes
                           [self.Ax ,self.Ay,self.Az], [self.Bx-0.1*machineUnit*self.Vx,self.By,self.Bz-0.1*machineUnit*self.Vz], [self.Bx-0.1*machineUnit*self.Vx,self.By+1.6*machineUnit,self.Bz-0.1*machineUnit*self.Vz], [self.Ax, self.Ay+1.6*machineUnit, self.Az],
                           [self.Dx ,self.Dy,self.Dz], [self.Cx-0.1*machineUnit*self.Vx,self.Cy,self.Cz-0.1*machineUnit*self.Vz], [self.Cx-0.1*machineUnit*self.Vx,self.Cy+1.6*machineUnit,self.Cz-0.1*machineUnit*self.Vz], [self.Dx, self.Dy+1.6*machineUnit, self.Dz],
                           
                       
                           
                           
                            [self.Bx,self.By,self.Bz],[self.Bx-0.1*machineUnit*self.Vx, self.By, self.Bz-0.1*machineUnit*self.Vz ],[self.Bx-0.1*machineUnit*self.Vx,self.By+0.9*machineUnit,self.Bz-0.1*machineUnit*self.Vz ],[self.Bx,self.By+0.6*machineUnit,self.Bz ],
                           
                            [self.Cx,self.Cy,self.Cz],[self.Cx-0.1*machineUnit*self.Vx, self.Cy, self.Cz-0.1*machineUnit*self.Vz ],[self.Cx-0.1*machineUnit*self.Vx,self.Cy+0.9*machineUnit,self.Cz-0.1*machineUnit*self.Vz ],[self.Cx,self.Cy+0.6*machineUnit,self.Cz ],
                           
                           
                           [self.Bx,self.By+0.6*machineUnit,self.Bz+0 ],[self.Bx+0.1*machineUnit*self.Vx,self.By+0.7*machineUnit,self.Bz+0.1*machineUnit*self.Vz ],[self.Bx+0.1*machineUnit*self.Vx ,self.By+0.8*machineUnit,self.Bz+0.1*machineUnit*self.Vz ],[self.Bx-0.1*machineUnit*self.Vx,self.By+0.9*machineUnit ,self.Bz-0.1*machineUnit*self.Vz ],
                           [self.Cx,self.Cy+0.6*machineUnit,self.Cz+0 ],[self.Cx+0.1*machineUnit*self.Vx,self.Cy+0.7*machineUnit,self.Cz+0.1*machineUnit*self.Vz ],[self.Cx+0.1*machineUnit*self.Vx ,self.Cy+0.8*machineUnit,self.Cz+0.1*machineUnit*self.Vz ],[self.Cx-0.1*machineUnit*self.Vx,self.Cy+0.9*machineUnit ,self.Cz-0.1*machineUnit*self.Vz ],
                           
                           [self.Bx-0.1*machineUnit*self.Vx, self.By+1.3*machineUnit, self.Bz-0.1*machineUnit*self.Vz],[self.Bx, self.By+1.4*machineUnit, self.Bz],[self.Bx,self.By+1.6*machineUnit,self.Bz], [self.Bx-0.1*machineUnit*self.Vx, self.By+1.6*machineUnit, self.Bz-0.1*machineUnit*self.Vz],
                           [self.Cx-0.1*machineUnit*self.Vx, self.Cy+1.3*machineUnit, self.Cz-0.1*machineUnit*self.Vz],[self.Cx, self.Cy+1.4*machineUnit, self.Cz],[self.Cx,self.Cy+1.6*machineUnit,self.Cz], [self.Cx-0.1*machineUnit*self.Vx, self.Cy+1.6*machineUnit, self.Cz-0.1*machineUnit*self.Vz]
                           
                           ]




    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(.3, .9, 5.)
        counter = 0
        for item in self.vertexList:
            glNormal3f(self.normalList[counter][0],self.normalList[++counter][1],self.normalList[++counter][2])
            glVertex3f(item[0], item[1], item[2])
        glEnd()
        glBegin(GL_LINES)
        glColor3f(1., 0., 0.)
        glEnd()

#fin de la machine et des classes diverses. Suivent les fonctions plus classiques

#l'algorythme de calcul des normales, mais les tests lumineux n'etant pas concluants, il est pour l'instant de peu d'utilite

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


# et maintenat les fonctions qui permettent a open GL de marcher via GLUT



#La fonction ou on dessine tout a l'ecran
def DrawGLScene():
    # Clear The Screen And The Depth Buffer, load the current and only matrix
    global alpha, transz, teta, game

    if game ==1 and Line_Runner.stop == 0:
        Line_Runner.LRdrawGLScene()
    else :
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()

#la premiere translation de la piece vers l'arriere, afin qu'elle entre dans notre champ de vision
        glTranslatef(0., -3.0, -15.0)

#les rotations et translations de la piece
        glTranslatef(0,0,transz)
        glRotatef(alpha, 0, 1, 0)
        glRotatef(teta, 0, 0, 1)


    ######################################
    #ici sont nos tests de lumiere, ils ne sont pas actifs, car il fallait decommenter la ligne glEnable(GL_LIGHTING) dans la faonction initGL

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, numpy.array((0.50, 0.50, 0.50, 0.5), 'f'))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, numpy.array((1., 0., 0., 1.0), 'f'))


        lightpos = numpy.array((5., 2., 0., 0.), 'f')
        lightdir = numpy.array((1, 0, 0), 'f')
        glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, lightdir)
        glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 90)



        #Ceci dessine une ligne sur le devant de la piece
        glBegin(GL_LINES)
        glColor3f(0,0,1)
        glVertex3f(-5,.3,5)
        glVertex3f(5,.3,5)
        glEnd()

    #drawables est la liste qui contient tout ce qui doit etre dessine a l'exception du bonhomme
        for thing in drawables :
            if thing.type == "non static":
                thing.move()
            thing.draw() #ceci appelle les methodes de dessin de tous les objets qui doivent etre dessines..
        myBonhomme.move()
        myBonhomme.draw()

        glutSwapBuffers()


#la fonction qui est appellee si une touche est enfoncee

def keyPressed(*args):
    global transz, teta, alpha, game

#si echape ou q est touche, l'application est fermee
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()

#zooms et rotations manuelles
#le teta fait pivoter la salle sur l'axe z, ce qui est nul, mais utile pour certains tests. C'est pour cela qu'on le fait saturer
    if args[0] == 'e' and teta<30:
        teta += 2
    if args[0] == 'd' and teta>-45:
        teta += -2
    
    if args[0] == 's':
        transz += -1.
    if args[0]== 'z':
        transz += 1.

##la c'est mal fait..
    if args[0]== 'h':
        game = 1
        Line_Runner.stop = 0
        #only for 3D stuff...
        glDisable(GL_DEPTH_TEST)


    if args[0]== 't':
        game = 0


#ici on appelle la fonction de clavier du line runner, en lui envoyant les arguments recus, c'est a dire les entrees du clavier
    if game == 1:
        Line_Runner.LRkeyPressed(args)

#la fonction qui est appellee si une touche est relachee.
def keyReleased(*args):
    global game
    #meme principe que quand une touche est enfoncee
    if game ==1 :
        Line_Runner.LRkeyReleased(args)


#les fonctions qui sont appellees lorsqu'une touche dite speciale est enfoncee ou relachee. Ici on ne regarde que les etats des touches directionnelles.

def specialKeyPressed(key, x, y):
    global direction, forward, game
#celles ci servent a faire bouger le bonhomme.
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


#Les fonctions qui regardent quand il se passe quelque chose avec la souris..

#ici le mouvement, sur les axes x et y
def myMouseMove (x, y):
    global alpha, xold
    #un mouvement ici fait tourner la salle.. et plus la difference entre le point de depart et celui d'arrivee est grande, plus on tourne !
    if xold<x:
        diff = x-xold
        alpha = diff

    if xold>x:
        diff = xold-x
        alpha = -diff

    glutPostRedisplay()

#si il y a un clique, on regarde si le bonhomme se trouve dans une porte quelconque...
def Mouseclick (button, state, x, y):

    if GLUT_LEFT_BUTTON == button and state==0: #state == 0 signifie que le bouton de la souris est enfonce.
        for element in gates :
            if element.checkifgate() != 0 :
                print(element.checkifgate())
                #si la borne a pour identifiant LR, on lance le Line_runner.
                if element.checkifgate() == 'LR':
                    global game
                    game = 1
                    Line_Runner.stop = 0
                    #et il faut enlever ce test, car il ne sert que quand il y a une profondeur.. (c'est a dire de la 3D)
                    glDisable(GL_DEPTH_TEST)

                if element.checkifgate() == 'tetris':

                    tetris.dead = 0
                    #et il faut enlever ce test, car il ne sert que quand il y a une profondeur.. (c'est a dire de la 3D)
                    glDisable(GL_DEPTH_TEST)


#notre clique droit ne sert pas a grand chose...
    if GLUT_RIGHT_BUTTON == button and state == 0 :
        print ("right_click")


#Les fonctions d'initialisation d'OpenGL
def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_RESCALE_NORMAL)
    glShadeModel(GL_SMOOTH)
    #glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)


    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

#fonction appelee lorsque la fenetre est redimensionnee
def reSizeGLScene(Width, Height):
    if Height == 0:						        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)		               # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


#fonction principale.
def main():
    global window
    #sequence d'initialisation
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 50)
    window = glutCreateWindow("ROOTS")
    InitGL(640, 480)


    #declaration des fonctions pour GLUT. Ce sont ces seules fonctions qui sont appellees chaque fois que la boucle infinie recommence.

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(reSizeGLScene)


    #permet le plein ecran
    glutFullScreen()


    glutIgnoreKeyRepeat(1)
    glutKeyboardFunc(keyPressed)
    glutKeyboardUpFunc(keyReleased)

    glutSpecialFunc(specialKeyPressed)
    #le sprite c'est trop bon !!!!! :)
    glutSpecialUpFunc(specialKeyReleased)

    glutMouseFunc(Mouseclick)
    glutPassiveMotionFunc(myMouseMove)

#et on lance la boucle infinie qui fait que la fenetre reste ouverte jusqu'a ce qu'on detruise l'aplication anec sys.exit
    glutMainLoop()


#ici on cree les instances de nos objets avant d'entrer dans la boucle principale.
drawables = [quad("floor", -5, 0.0, 5, 0., 0.0, -10., 10., 0.0, 0., 1.0, 1., 0.), machine("LR", 0, 0, 0, 1, 0, 0), machine("snake", -3, 0, -3, 0, 0, 1), machine("tetris", 0, 0, -5, 0, 0, 1)]
#myBonhomme = bonhomme(-3.0,0.0,0.1, 0.707, 0, -0.707, 0.707, 0, 0.707)
myBonhomme = bonhomme(-3.0,0.0,0.1, -1, 0, 0, 0, 0, -1)


main()
