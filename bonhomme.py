from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

ESCAPE = '\033'

# Number of the glut window.
window = 0
forward =0
direction = 0
alpha = 0

#############################
#this is where you put your dude classes

class foot (object):
    def __init__(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az

    def getPoints(self):
        unite = 1
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
        unite = 1
        x = self.Ax
        y = self.Ay+3*unite
        z = self.Az
        self.jambeVertexList = [[x, y, z], [x, y+5*unite, z], [x+3*unite, y+5*unite, z], [x+3*unite, y, z],
                                [x, y, z], [x, y+5*unite, z], [x, y+5*unite, z+unite], [x, y, z+unite],
                                [x+3*unite, y, z], [x+3*unite, y+5*unite, z], [x+3*unite, y+5*unite, z+unite], [x+3*unite, y, z+unite],
                                [x, y, z+unite], [x, y+5*unite, z+unite], [x+3*unite, y+5*unite, z+unite], [x+3*unite, y, z+unite]]

class bonhomme (object):
    def __init__(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.type = "moving"

    def getPoints(self):
        myFoot = foot(self.Ax, self.Ay, self.Az)
        myFoot.getPoints()
        self.vertexList = myFoot.footVertexList
        #self.vertexList.append()
        
    def drawBonhomme(self):
        self.getPoints()
        glBegin(GL_QUADS)
        for item in self.vertexList:
            glVertex3f(item[0], item[1], item[2])
        glEnd()

    def move(self):
        global forward
        global direction
        
        if direction == 0 and forward ==1:
            self.Ax = self.Ax +1
        if direction == 1:
            self.Az = self.Az +1


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.

    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
	    Height = 1
    
    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function.
def DrawGLScene():
    global texture
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
    glLoadIdentity()					# Reset The View
    global alpha
    glTranslatef(0.,0.0,-15.0)			# Move Into The Screen
    glRotatef(alpha*4, 0, 1, 0)
    MyBonhomme.move()
    MyBonhomme.drawBonhomme()

    
    
    ###################################
    #this is wherr eyou draw the stuff
  
    
    glutSwapBuffers()


def keyPressed(*args):
    global window
    global alpha
    global direction
    global forward
    # If escape or q is pressed, kill everything.
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()
    if args[0] == 'o':
        forward = 1.

    if args[0] == 'l':
        forward = -1.
    if args[0] == 's':
        forward = 0
    if args[0] == 'm':
        direction += -1.
    if args[0] == 'k':
        direction += 1.

def main():
	global window
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Hey Lucile !")
    
    
	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(DrawGLScene)
	glutReshapeFunc(ReSizeGLScene)
	glutKeyboardFunc(keyPressed)
    
	InitGL(640, 480)
	glutMainLoop()


MyBonhomme = bonhomme(-1.0,0.0,0.0)
main()

