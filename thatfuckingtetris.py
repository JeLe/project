from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


ESCAPE = '\033'

# Number of the glut window.
window = 0
alpha = 0

class carre(object):
      def __init__(self,x,y,couleur):
            self.red=couleur[0]
            self.green=couleur[1]
            self.blue=couleur[2]
            self.vertices = [[x,y,0],[x,y+1, 0],[x+1, y+1, 0],[x+1,y, 0]]
      def draw(self):
            glBegin(GL_QUADS)
            glColor3f(self.red, self.green, self.blue)
            for vertex in self.vertices:
                  glVertex3f(vertex[0],vertex[1],vertex[2])
            glEnd()

 

#FABRICATION

moncarre=carre(0,0,[1.0,1.0,1.0])
machin=[]
grille=[]

for ligne in range(10):
      for colonne in range(20):
            machin.append(carre(ligne,colonne,[1.0,1.0,1.0]))
      grille.append(machin)







# A general OpenGL initialization function. Sets all of the initial parameters.
def InitGL(Width, Height):               	# We call this right after our OpenGL window is created.

    glClearColor(0.0, 0.0, 0.0, 0.0)           	# This Will Clear The Background Color To Black
    glClearDepth(1.0)                    	# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                 	# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)             	# Enables Depth Testing
    glShadeModel(GL_SMOOTH)             	# Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    	# Reset The Projection Matrix
                                                # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:                   	# Prevent A Divide By Zero If The Window Is Too Small
          Height = 1
    
    glViewport(0, 0, Width, Height)	# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Fonction de dessin principale
def DrawGLScene():
    global texture
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
    glLoadIdentity()	# Reset The View
    global alpha
    glTranslatef(-5.,-10.0,-25.0)	# Move Into The Screen
    glRotatef(alpha*4, 0, 1, 0)
 

#DESSIN

    for item in grille :
          for trucs in item :
                trucs.draw()
    
    
    
    ##############################################
    #C'est ici qu'on ecrit pour dessiner les trucs
  
    
    glutSwapBuffers()


def keyPressed(*args):
    global window

    # Si q ou echap presse, tout effacer
    if args[0] == ESCAPE or args[0] == 'q':
        sys.exit()


def main():
      global window
      glutInit(sys.argv)
      glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

      glutInitWindowSize(640, 480)
      glutInitWindowPosition(0, 0)
      window = glutCreateWindow("Bonjour Bob !")
    
    
      glutDisplayFunc(DrawGLScene)
      glutIdleFunc(DrawGLScene)
      glutReshapeFunc(ReSizeGLScene)
      glutKeyboardFunc(keyPressed)
      
      InitGL(640, 480)
      glutMainLoop()

main()
