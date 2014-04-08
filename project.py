from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, time
from math import sin,cos,sqrt,pi
import numpy
import snake

##########################################
#to do list for tomorrow !
#make draw method function so all objects can use the same one. not necessairy for now...

#make door and wall objetcs common to objects easier to use. If static, they sould only be calculated once and should be in a seperate list
#wall objects will be made like they are now, excepet add sort of vertices and take only extremes into account. That will lighten the memory use.
#cameras move when in corners...

################################
#Jeremie's work :
#I need to get all te walls into one place, look at them one by one and see if the guy isn't in front of them....
#then for the "doors" : two poins need to be equal, but that's a little too damn precise, no?
#is that all ?

##########################################



##########################################
#all global variables
ESCAPE = '\033'
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
#
#All main vertex lists must be self.vertexList, except for gates...


class wall (object):
    def __init__(self, thingToWall):
        #i don't really need any thing to be in my wall yet...
        self.getPoints(thingToWall)
        walls.append(self)
    
    def getPoints(self, thingToWall):
        thingToWall.getPoints()
        
        self.vertices = []
        for vertex in thingToWall.vertexList:
            self.vertices.append([vertex[0], 0.1, vertex[2]])
    
    #z2-z0, z3-z1
    def checkNotOnWall(self):
        self.equation1 = (self.vertices[2][2]-self.vertices[0][2])/(self.vertices[2][0]-self.vertices[0][0])

#here we will put the gate class

class gate (object):
    def __init__ (self):
        True
    
    def checkifgate(self):
        if machine.list[1][0]<myBonhomme.Ax<machine.list[1][0]+1 and machine.list[1][2]<myBonhomme.Az<machine.list[2][2] :
            print("Youpi")
        else :
            print("notyoupi")


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
        
        self.normalList=CalculateNormal(self)
    
    def draw(self):
        self.getPoints()
        glBegin(GL_QUADS)
        counter = 0
        for item in self.vertexList:
            #this works because we enabled it in init.
            #so if we need ambient, diffuse and specular lighting I don't know if it's wise...
            glColor3f(0.7, 0.4, 0.9)
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
        if forward != 0:
            b= self.Az-direction*self.Ax
            self.Ax = self.Ax + forward
            self.Az = (direction*self.Ax)+b
            
            forward = 0


#END OF DUDE
machineUnit = 3

class machine(object):
    def __init__(self,name,Ax,Ay,Az):
        self.name=name
        self.Ax=Ax
        self.Ay=Ay
        self.Az=Az
        self.type = "static"
        self.getPoints()
        self.normalList=CalculateNormal(self)
        self.myWall = wall(self)
        self.myGate = gate()
    
    def getPoints(self):
        global machineUnit
        self.vertexList = [[self.Ax+0,self.Ay+0,self.Az+0],[self.Ax+0.5*machineUnit,self.Ay+0,self.Az+0],[self.Ax+0.5*machineUnit,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0,self.Ay+0,self.Az-0.6*machineUnit],
                               
                               
                               [self.Ax+0.5*machineUnit,self.Ay+0,self.Az+0],[self.Ax+0.5*machineUnit,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az+0],
                               
                               [self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az+0],[self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az+0],[self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az+0],[self.Ax+0.6*machineUnit,self.Ay+0.8*machineUnit,self.Az+0],[self.Ax+0.6*machineUnit,self.Ay+0.8*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.6*machineUnit,self.Ay+0.8*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.9*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.9*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.6*machineUnit,self.Ay+0.8*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.3*machineUnit,self.Ay+0.9*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+1.3*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+1.3*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0.9*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.3*machineUnit,self.Ay+1.3*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.4*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.4*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+1.3*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.4*machineUnit,self.Ay+1.4*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.6*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.4*machineUnit,self.Ay+1.4*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.4*machineUnit,self.Ay+1.6*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az+0],
                               
                               [self.Ax+0,self.Ay+1.6*machineUnit,self.Az+0],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0,self.Ay+0,self.Az+0],
                               
                               #the sides (dark or not, as you want)
                               [self.Ax+0,self.Ay+0,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+1.6*machineUnit,self.Az+0],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az+0],
                               
                               [self.Ax+0.3*machineUnit,self.Ay+0,self.Az+0],[self.Ax+0.5*machineUnit,self.Ay+0,self.Az+0],[self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.6*machineUnit,self.Az+0],
                               
                               [self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.6*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.7*machineUnit,self.Az+0],[self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az+0],
                               
                               [self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.7*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+0.9*machineUnit,self.Az+0],[self.Ax+0.6*machineUnit,self.Ay+0.8*machineUnit,self.Az+0],
                               
                               [self.Ax+0.3*machineUnit,self.Ay+1.3*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.4*machineUnit,self.Az+0],[self.Ax+0.4*machineUnit,self.Ay+1.6*machineUnit,self.Az+0],[self.Ax+0.3*machineUnit,self.Ay+1.6*machineUnit,self.Az+0],
                               
                               
                               
                               [self.Ax+0,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.3*machineUnit,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0.5*machineUnit,self.Ay+0,self.Az-0.6*machineUnit],[self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0.6*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.5*machineUnit,self.Ay+0.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0.7*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.6*machineUnit,self.Ay+0.7*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0.7*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+0.9*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.6*machineUnit,self.Ay+0.8*machineUnit,self.Az-0.6*machineUnit],
                               
                               [self.Ax+0.3*machineUnit,self.Ay+1.3*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.4*machineUnit,self.Ay+1.4*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.4*machineUnit,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit],[self.Ax+0.3*machineUnit,self.Ay+1.6*machineUnit,self.Az-0.6*machineUnit]]

    
    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.4, 0.6)
        counter = 0
        for item in self.vertexList:
            #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, red)
            glNormal3f(self.normalList[counter][0],self.normalList[++counter][1],self.normalList[++counter][2])
            glVertex3f(item[0], item[1], item[2])
        #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, white)
        glEnd()


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
        self.normalList=CalculateNormal(self)

        self.wall = wall(self)
    
    def getPoints(self):
        self.vertexList = [[self.Ax, self.Ay, self.Az], [self.Ax+self.Vx, self.Ay+self.Vy, self.Az+self.Vz],[self.Ax+self.Vx+self.Wx, self.Ay+self.Vy+self.Wy, self.Az+self.Vz+self.Wz], [self.Ax+self.Wx, self.Ay+self.Wy, self.Az+self.Wz]]
    
    def draw(self):

        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        counter = 0
        for vertex in self.wall.vertices:
            #glNormal3f(self.normalList[counter][0],self.normalList[0][1],self.normalList[0][2])
            glNormal3f(0., -1., 0.)
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()




#And in init(if static) or in getVertices (if not static) add this line self.normalList=CalculateNormal(self)
def CalculateNormal(objectToNormalize) :
    q=0
    normalList=[]
    while q!=len(objectToNormalize.vertexList)-4:
        U=[objectToNormalize.vertexList[q+1][0]-objectToNormalize.vertexList[q][0],objectToNormalize.vertexList[q+1][1]-objectToNormalize.vertexList[q][1],objectToNormalize.vertexList[q+1][2]-objectToNormalize.vertexList[q][2]]
        V=[objectToNormalize.vertexList[q+2][0]-objectToNormalize.vertexList[q][0],objectToNormalize.vertexList[q+2][1]-objectToNormalize.vertexList[q][1],objectToNormalize.vertexList[q+2][2]-objectToNormalize.vertexList[q][2]]
        N=[U[1]*V[2]-U[2]*V[1], U[2]*V[1]-U[1]*V[2], U[0]*V[1]-U[1]*V[0]]
        normalList.append(N)
        q+=4

    return(normalList)


#now our GL functions. DraxFunc is first cause most important

# The main drawing function.
def DrawGLScene():
    # Clear The Screen And The Depth Buffer, load the current and only matrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # push the origin of (x, y, z) to wher you can see it
    #and go a little higher than the origin to be above the floor
    #without having to rotate the whole thing..
    glTranslatef(0., -3.0, -15.0)
    
    #Here are the movements you do when you move around or for/backwards
    #Hey Ben, I found out you need to do all your translations first
    #then you rotations, or you get wierd stuff...
    global alpha, transz, teta
    glTranslatef(0,0,transz)
    glRotatef(alpha, 0, 1, 0)
    glRotatef(teta, 0, 0, 1)
    
    
    ######################################
    #here we start the light stuff !!
    
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, numpy.array((0.50, 0.50, 0.50, 0.5), 'f'))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, numpy.array((1., 0., 0., 1.0), 'f'))
    

    #glEnable(GL_LIGHT1)
        
    lightpos = numpy.array((-5., 2., -0.5, 0.), 'f')
    lightdir = numpy.array((1, 0, 0), 'f')
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, lightdir)
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 90)


    
    #the line is the lamps stand !
    #    glBegin(GL_LINES)
    #glColor3f(0,0,1)
    #glVertex3f(-5,.3,5)
    #glVertex3f(5,.3,5)
    #glEnd()
    
    #drawables is the list that has all the object instances we will need to draw.
    for thing in drawables :
        if thing.type == "non static":
            thing.move()
        thing.draw() #this includes refreshing vertices for non statics

    myBonhomme.move()
    myBonhomme.draw()
    
    glutSwapBuffers()



def keyPressed(*args):
    global transz, teta
    
    # If escape or q is pressed, kill everything.
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()
    
    #manual rotations and zooms
    #OK THE TETA IS CRAP but can be cool for tests..
    if args[0] == 'e' and teta<30:
        teta += 2
    if args[0] == 'd' and teta>-45:
        teta += -2
    if args[0] == 'z':
        transz += -1.
    if args[0]== 's':
        transz += 1.
    if args[0]== 'h':
        snake.main()



def specialKeyPressed(key, x, y):
    global direction, forward

    #to move the dude...
    if key == GLUT_KEY_UP :
        forward = .1
    if key == GLUT_KEY_DOWN:
        forward = -.1
    if key == GLUT_KEY_LEFT:
        direction += .1
    if key == GLUT_KEY_RIGHT:
        direction += -.1



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
     if button == GLUT_LEFT_BUTTON:
         print("prout")
         for element in gates :
            element.checkifgate()



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
    

def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)
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
    
    
    glutDisplayFunc(DrawGLScene)
    
    #glutFullScreen()
    
    #these are the callbacks to the functions that actually do something...
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(specialKeyPressed)

    glutMouseFunc( myMouseMove)
    glutPassiveMotionFunc( myMouseMove)
    
    glutMainLoop()
    
#here is where we instanciate all the objects....
#must be here or all necessary funcs haven't apeared yet...
#we now need to get the walls for all the machines and ... youpii
drawables = [quad("floor", -5, 0.0, 5, 0., 0.0, -10., 10., 0.0, 0., 1.0, 1., 0.), machine("test", 0, 0, 0)]
myBonhomme = bonhomme(0.0,0.0,0.0)


main()










		
