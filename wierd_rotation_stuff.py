from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, time
from math import *

# je rajoute un commentaire
#hi ?
ESCAPE = '\033'
# Number of the glut window.
window = 0
alpha = 0
transz = 0
modl = 0
argus = 0

# all my classes here, and then the instanciation of my first objects !


class wall (object):
    def __init__(self):
        True
    
    def getWallVertices(self, thingToWall):
        thingToWall.getQuadVertices()
        
        self.vertices = []
        for vertex in thingToWall.vertices:
            self.vertices.append([vertex[0], 0.1, vertex[2]])
#z2-z0, z3-z1
    def checkNotOnWall(self):
        self.equation1 = (self.vertices[2][2]-self.vertices[0][2])/(self.vertices[2][0]-self.vertices[0][0])


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
        self.wall = wall()
        
    def getQuadVertices(self):
        self.vertices = [[self.Ax, self.Ay, self.Az], [self.Ax+self.Vx, self.Ay+self.Vy, self.Az+self.Vz],[self.Ax+self.Vx+self.Wx, self.Ay+self.Vy+self.Wy, self.Az+self.Vz+self.Wz], [self.Ax+self.Wx, self.Ay+self.Wy, self.Az+self.Wz]]

    def drawQuad(self):
        self.getQuadVertices()
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        self.wall.getWallVertices(self)
        if self.name != "floor":
            glBegin(GL_QUADS)
            glColor3f(0., 1., 0.)
            for vertex in self.wall.vertices:
                glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()



quads= [ quad("floor", -5, 0.0, 5, 0., 0.0, -10., 10., 0.0, 0., 1.0, 1., 0.)]


# A general OpenGL initialization function. Sets all of the initial parameters.
def InitGL(Width, Height):	# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)	# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)	# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)	# Enables Depth Testing
    glShadeModel(GL_SMOOTH)	# Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()	# Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    
    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:	# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)	# Reset The Current Viewport And Perspective Transformation
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
    glTranslatef(0., -3.0, -10.0)

    # my rotation of the whole world to know what i'm doing...
    global alpha
    global transz

    glTranslatef(0,0,transz)
 

    for item in quads :
        item.drawQuad()

    glutSwapBuffers()



def rotategood ():
    global alpha
    global modl
    global argus

    lspoint = quads[0].getQuadVertices()
    #calculating module et argument pour chaque point 
    
    modl = hypot(quads[0].vertices[0][0],quads[0].vertices[0][2])
    argus = atan(quads[0].vertices[0][2]/quads[0].vertices[0][0])
    #    argus = argus+alpha #on ajoute la valeur de alpha qui dpend des touches
    argus = argus+alpha
    quads[0].Ax = modl*cos(argus)#on reporte sur x et z 
    quads[0].Az = modl*sin(argus)
    
    lspoint = quads[0].getQuadVertices()
    modl = hypot(quads[0].vertices[1][0],quads[0].vertices[1][2])
    argus = atan(quads[0].vertices[1][2]/quads[0].vertices[1][0])
    argus = argus+alpha
    quads[0].Vx = modl*cos(argus)
    quads[0].Vz = modl*sin(argus)
    
    lspoint = quads[0].getQuadVertices()
    modl = hypot(quads[0].vertices[3][0],quads[0].vertices[3][2])
    argus = atan(quads[0].vertices[3][2]/quads[0].vertices[3][0])
    argus = argus+alpha
    quads[0].Wx = modl*cos(argus)
    quads[0].Wz = modl*sin(argus)
    

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
    global alpha
    global transz
    # If escape or q is pressed, kill everything.
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()
    if args[0] == 'm':
        alpha += 0.5
        rotategood()
    if args[0] == 'k':
        alpha += -0.5
        rotategood()
    if args[0] == 'r':
        transz += -1.
    if args[0]== 'f':
        transz += 1.

def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 50)
    window = glutCreateWindow("Benkiwi :D")
    InitGL(640, 480)
    
    
    glutDisplayFunc(DrawGLScene)
    
    #glutFullScreen()
    
    # these are the callbacks to the functions that actually do something...
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    
    
    glutMainLoop()
    


main()