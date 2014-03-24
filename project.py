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
##########################################

# je rajoute un commentaire
#hi ?
ESCAPE = '\033'
# Number of the glut window.
window = 0
alpha = -90
transz = 0
xold = 600

forward = 0
direction = 0

walls = []
doors = []
########################################
#this is where you put your dude classes

class foot (object):
    def __init__(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
    
    def getPoints(self):
        unite = .5
        x = self.Ax
        y = self.Ay
        z = self.Az
        self.footVertexList = [[x, y, z], [x+3*unite, y , z], [x+3*unite, y, z+3*unite], [x, y, z+3*unite],
                               [x, y, z], [x+3*unite, y , z], [x+3*unite, y+3*unite , z], [x, y+3*unite, z],
                               [x, y, z], [x, y+3*unite, z], [x, y+3*unite, z+3*unite], [x, y, z+3*unite],
                               [x, y, z+3*unite], [x, y+3*unite, z+3*unite], [x+3*unite, y+3*unite, z+3*unite], [x+3*unite, y, z+3*unite],
                               [x+3*unite, y , z], [x+3*unite, y+3*unite , z], [x+3*unite, y+3*unite , z+3*unite], [x+3*unite, y, z+3*unite],
                               [x, y+3*unite, z], [x+3*unite, y+3*unite, z], [x+3*unite, y+3*unite, z+3*unite],[x, y+3*unite, z+3*unite]]


class jambe (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
    
    def getPoints(self):
        unite = .5
        x = self.Ax
        y = self.Ay+3*unite
        z = self.Az
        self.jambeVertexList = [[x, y, z], [x, y+5*unite, z], [x+3*unite, y+5*unite, z], [x+3*unite, y, z],
                                [x, y, z], [x, y+5*unite, z], [x, y+5*unite, z+unite], [x, y, z+unite],
                                [x+3*unite, y, z], [x+3*unite, y+5*unite, z], [x+3*unite, y+5*unite, z+unite], [x+3*unite, y, z+unite],
                                [x, y, z+unite], [x, y+5*unite, z+unite], [x+3*unite, y+5*unite, z+unite], [x+3*unite, y, z+unite]]


class torse (object):
    def __init__ (self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
    
    def getPoints(self):
        unite = .5
        x = self.Ax
        y = self.Ay+8*unite
        z = self.Az
        self.torseVertexList = [[x, y, z], [x, y+5*unite, z], [x+7*unite, y+5*unite, z], [x+7*unite, y, z],
                                [x, y, z]]
                                


class bonhomme (object):
    def __init__(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.type = "moving"
    
    def getPoints(self):
        unite = .5
        myFoot = foot(self.Ax, self.Ay, self.Az)
        myFoot.getPoints()
        myFoot2 = foot(self.Ax+4*unite, self.Ay, self.Az)
        myFoot2.getPoints()
        myJambe = jambe(self.Ax, self.Ay, self.Az)
        myJambe.getPoints()
        myJambe2 = jambe(self.Ax+4*unite, self.Ay, self.Az)
        myJambe2.getPoints()
        self.vertexList = []
        self.vertexList.append(myFoot.footVertexList)
        self.vertexList.append(myJambe.jambeVertexList)
        self.vertexList.append(myFoot2.footVertexList)
        self.vertexList.append(myJambe2.jambeVertexList)
    
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

################################
#Jeremie's work :
#I need to get all te walls into one place, look at them one by one and see if the guy isn't in front of them....
#then for the "doors" : two poins need to be equal, but that's a little too damn precise, no?
#is that all ?
################################


class quad(object):
    def __init__(self, name, Ax, Ay, Az, Vx, Vy, Vz, Wx, Wy, Wz, red, green, blue):
        self.name = name
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
        self.wall = wall(self)

    def getQuadVertices(self):
        self.vertices = [[self.Ax, self.Ay, self.Az], [self.Ax+self.Vx, self.Ay+self.Vy, self.Az+self.Vz],[self.Ax+self.Vx+self.Wx, self.Ay+self.Vy+self.Wy, self.Az+self.Vz+self.Wz], [self.Ax+self.Wx, self.Ay+self.Wy, self.Az+self.Wz]]

    def drawQuad(self):
        self.getQuadVertices()
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

#self.wall.getWallVertices(self)
        if self.name != "floor":
            glBegin(GL_QUADS)
            glColor3f(0., 1., 0.)
            for vertex in self.wall.vertices:
                glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()

#here is where wa instanciate all the objects....
#we now need to get the walls for all the machines and ... youpii

floor = quad("floor", -5, 0.0, 5, 0., 0.0, -10., 10., 0.0, 0., 1.0, 1., 0.)
test = quad("test", -10, 0.0, 0, 10., 0.0, 0., 0, 2., 0., 0., 0.4, 0.7)

print (walls[1].vertices)

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
    global alpha, transz, direction
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

    MyBonhomme.move()
    MyBonhomme.drawBonhomme()
    
        
    glutSwapBuffers()
        
        

def keyPressed(*args):
    #global alpha
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
    if xold<x:
        alpha += 1
    if xold>x:
        alpha += -1
    xold=x

    glutPostRedisplay()

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










		
