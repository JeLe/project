from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *


ESCAPE = '\033'

# Number of the glut window.
window = 0
alpha =0

class player (object):
    def __init__ (self, Ax, Ay, couleur):
	self.red = couleur[0]
	self.green = couleur[1]
	self.blue = couleur[2]
	self.Ax = Ax
  self.Ay = Ay
    
    def getvertices(self):
	self.vertices = [[self.Ax-.7,self.Ay-0.7,0],[self.Ax-.7,self.Ay-.4,0],[self.Ax-.4,self.Ay-.4,0],[self.Ax-.4,self.Ay-.7,0]]
	
    def drawplayer(self):
	      glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()

class carre (object):
    def __init__ (self, Ax, Ay, couleur):
        self.red = couleur[0]
        self.green = couleur[1]
        self.blue = couleur[2]
        self.Ax = Ax
        self.Ay = Ay
    def getvertices(self):
        self.Ax -= .01
	self.vertices = [[self.Ax,self.Ay,0],[self.Ax,self.Ay+0.5,0],[self.Ax+0.5,self.Ay+0.5,0],[self.Ax+0.5,self.Ay,0]]
      
    def drawcarre(self):
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()
        
        
        
monplayer= player (-1.7,-1.2,[0.8,0.2,0.6])    
moncarre = carre (.9,.9,[0.2,0.3,0.5])



# Fonction d'initialisation pour OpenGL. Paramètres de base.
def InitGL(Width, Height):				# On appelle cette fonction juste après que la fenetre ait été créée.

    glClearColor(0.0, 0.0, 0.0, 0.0)	# change la couleur de fond de la fenetre
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

# fonction principale de dessin.
def DrawGLScene():
    global texture
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
    glLoadIdentity()					# Reset The View
    global alpha
    glTranslatef(0.,0.0,-5.0)			# Move Into The Screen
    glRotatef(alpha*4, 0, 1, 0)
    moncarre.getvertices()
    monplayer.getvertices()
    monplayer.drawplayer()
    moncarre.drawcarre()
    

    
    
    ###################################
  
    
    glutSwapBuffers()


def keyPressed(*args):
    global window
    global alpha
    # Si "Echap" ou "q" est appuyé, ferme le programme.
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()
    if args[0] == 'm':
        alpha += -1.
    if args[0] == 'k':
        alpha += 1.
    if args[0] == 'a':
	monplayer.Ay+=0.5

def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow( "Line_Runner")
    
    
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    
    InitGL(640, 480)
    glutMainLoop()

main()
