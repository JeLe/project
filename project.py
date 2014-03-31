from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, time
from math import sin,cos,sqrt,pi

##########################################
#to do list for tomorrow !
#make draw method function so all objects can use the same one. not necessairy for now...
#Put all objects in list
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
alpha = -90
transz = 0
xold = 600

forward = 0
direction = 0


#wall and door buffers
walls = []
gates = []


########################################
#ALL THE OBJECT CLASSES
#
#All main vertex lists must be self.vertexList, except for gates...

#this is where you put your dude classes
unite = .5
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
        self.vertexList.append(myFoot.footVertexList)
        self.vertexList.append(maJambe.jambeVertexList)
        self.vertexList.append(myFoot2.footVertexList)
        self.vertexList.append(maJambe2.jambeVertexList)
        self.vertexList.append(myTorse.torseVertexList)
        self.vertexList.append(miBrazo.brazoVertexList)
        self.vertexList.append(miBrazo2.brazoVertexList)
        self.vertexList.append(monCou.couVertexList)
        self.vertexList.append(meineKopf.kopfVertexList)
    
    def drawBonhomme(self):
        self.getPoints()
        glBegin(GL_QUADS)
        for truc in self.vertexList:
            for item in truc:
                glColor3f(0.7, 0.4, 0.9)
                glVertex3f(item[0], item[1], item[2])
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

class quad(object):
    def __init__(self, name, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz, red, green, blue):
        self.name = name
        #self.type = "static or not??"
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
        #I ommited the creation of the vertices here because they might need to be regurlarly updated...
        #But all statics wont need to be updated !!
        self.wall = wall(self)
    
    def getQuadVertices(self):
        self.vertexList = [[self.Ax, self.Ay, self.Az], [self.Ax+self.Vx, self.Ay+self.Vy, self.Az+self.Vz],[self.Ax+self.Vx+self.Wx, self.Ay+self.Vy+self.Wy, self.Az+self.Vz+self.Wz], [self.Ax+self.Wx, self.Ay+self.Wy, self.Az+self.Wz]]
    
    def drawQuad(self):
        self.getQuadVertices()
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertexList:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        
        #self.wall.getWallVertices(self)
        if self.name != "floor":
            glBegin(GL_QUADS)
            glColor3f(0., 1., 0.)
            for vertex in self.wall.vertices:
                glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()


class wall (object):
    def __init__(self, thingToWall):
        #i don't really need any thing to be in my wall yet...
        self.getWallVertices(thingToWall)
        walls.append(self)
    
    def getWallVertices(self, thingToWall):
        thingToWall.getQuadVertices()
        
        self.vertices = []
        for vertex in thingToWall.vertices:
            self.vertices.append([vertex[0], 0.1, vertex[2]])

#z2-z0, z3-z1
    def checkNotOnWall(self):
        self.equation1 = (self.vertices[2][2]-self.vertices[0][2])/(self.vertices[2][0]-self.vertices[0][0])

#here we will put the gate class

class gate (object):
    def __init__ (self):
        True
    
    def checkifgate(self):
        if machine.list[1][0]<mybonhomme.Ax<machine.list[1][0]+1 and machine.list[1][2]<mybonhomme.Az<machine.list[2][2] :
            print("Youpi")
        else :
            print("notyoupi")

#here is where we instanciate all the objects....
#we now need to get the walls for all the machines and ... youpii

floor = quad("floor", -5, 0.0, 5, 0., 0.0, -10., 10., 0.0, 0., 1.0, 1., 0.)
test = quad("test", -10, 0.0, 0, 10., 0.0, 0., 0, 2., 0., 0., 0.4, 0.7)


def CalculateNormal():
    U=[MyBonhomme.vertexList[1][0]-MyBonhomme.vertexList[0][0],MyBonhomme.vertexList[1][1]-MyBonhomme.vertexList[0][1],MyBonhomme.vertexList[1][2]-MyBonhomme.vertexList[0][2]]
    V=[MyBonhomme.vertexList[2][0]-MyBonhomme.vertexList[0][0],MyBonhomme.vertexList[2][1]-MyBonhomme.vertexList[0][1],MyBonhomme.vertexList[2][2]-MyBonhomme.vertexList[0][2]]
    N=[CalculateNormal.U[1]*CalculateNormal.V[2]-CalculateNormal.U[2]*CalculateNormal.V[1],CalculateNormal.U[2]*CalculateNormal.V[1]-CalculateNormal.U[1]*CalculateNormal.V[2],CalculateNormal.U[0]*CalculateNormal.V[1]-CalculateNormal.U[1]*CalculateNormal.V[0]]
    print("caca")


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
    global alpha, transz
    glTranslatef(0,0,transz)
    glRotatef(alpha, 0, 1, 0)
    
    
    #the line is the y axis
    glBegin(GL_LINES)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glEnd()
    
    #and here is the floor :)
    floor.drawQuad()
    test.drawQuad()
    
    #here is the dude !
    MyBonhomme.move()
    MyBonhomme.drawBonhomme()
    
    
    glutSwapBuffers()



def keyPressed(*args):
    global transz
    global alpha
    
    # If escape or q is pressed, kill everything.
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()
    
    #manual rotations and zooms
    if args[0] == 'g':
        alpha += 1
    if args[0] == 'd':
        alpha += -1
    if args[0] == 'r':
        transz += -1.
    if args[0]== 'f':
        transz += 1.


def specialKeyPressed(key, x, y):
    global direction
    global forward
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
    glShadeModel(GL_SMOOTH)
    
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
    
    #    glutFullScreen()
    
    #these are the callbacks to the functions that actually do something...
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(specialKeyPressed);

    glutMouseFunc( myMouseMove)
    glutPassiveMotionFunc( myMouseMove)
    
    glutMainLoop()
    

MyBonhomme = bonhomme(0.0,0.0,0.0)

main()










		
