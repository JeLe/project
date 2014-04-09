#importation de ttes les 'libraries' necessaires pour le programme 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *


ESCAPE = '\033'

# variables pour la fenetre du programme 
window = 0
alpha =0

#creation de l'objet 'player' (ce sera le personnage/le 'truc' qui devra eviter les obstacles dans le jeu)
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

#creation de l'objet 'carre' (ce seront les obstacles dans le jeu)
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
       
#creation d'un player et d'un obstacle en precisant leurs parametres (coordonnees, couleur)        
monplayer= player (-1.7,-0.9,[1.,1.,0.0])
moncarre = carre (0.9,0.9,[0.1,0.8,0.5])

# Fonction d'initialisation d'OpenGL. Defini les parametres principaux.
def InitGL(Width, Height):			         	# On l'appelle juste apres que la fenetre OpenGL ait ete creee.
    glClearColor(0.2, 0.5, 0.8, 0.0)                            # permet de changer la couleur de fond de la fenetre
    glShadeModel(GL_SMOOTH)                      	# Enables Smooth Color Shading
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					                # Reset The Projection Matrix
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
   
    glMatrixMode(GL_MODELVIEW)
    
    
def ReSizeGLScene(Width, Height):
    if Height == 0:						        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1
        
    glViewport(0, 0, Width, Height)		               # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
# Fonction principale pour dessiner les objets a l'ecran.
def DrawGLScene():
    global texture
    glClear(GL_COLOR_BUFFER_BIT)	# Clear The Screen Buffer
    glLoadIdentity()					# Reset The View
    global alpha
    glTranslatef(0.,0.0,-5.0)			# Move Into The Screen
    moncarre.getvertices()
    monplayer.getvertices()
    monplayer.drawplayer()
    moncarre.drawcarre()
    
    if -2.3 < moncarre.Ax < -2.00 and moncarre.Ay<=monplayer.Ay:#(monplayer.Ay<=moncarre.Ay<=monplayer.Ay+0.3 or monplayer.Ay<=moncarre.Ay+0.3<=monplayer.Ay+0.3):
        print(monplayer.Ay)
        print(moncarre.Ay)
        sys.exit()
        
        ##############################################
        
    
    glutSwapBuffers()
    
    
    
    
    #on defini ici les touches et les actions correspondantes
def keyPressed(*args):
    global window
    global alpha
    if args[0] == ESCAPE or args[0] == 'q': # Si on appuie sur 'q' ou 'echap', ferme le programme
        sys.exit()
    if args[0] == 'z':
        monplayer.Ay+=0.1
    if args[0] == 's':
	monplayer.Ay-=0.1


def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow( "Line_Runner")  #donne un nom a la fenetre
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    
    InitGL(640, 480)
    glutMainLoop()

main()
