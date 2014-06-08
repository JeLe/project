from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, time
from Image import *

from math import sin,cos,sqrt,pi
import numpy
from random import *
import Line_Runner, snake, tetris
from globjects import *
import globjects

#all global variables
ESCAPE = '\033'
game = 0

# Number of the glut window.
window = 0
alpha = [0, 1]
transz = [0, 0]
teta = [0, 0]
xold = 600


# et maintenat les fonctions qui permettent a open GL de marcher via GLUT

texture = 0

def LoadTextures():
    #global texture
    image = open("graal.bmp")
	
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
	
    # Create Texture
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))   # 2d texture (x and y size)
	
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    
    
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)



def DrawGLScene():
    # Clear The Screen And The Depth Buffer, load the current and only matrix
    global game

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    
    #la premiere translation de la piece vers l'arriere, afin qu'elle entre dans notre champ de vision
    glTranslatef(0., -3.0, -10.0)
  
    transz[1]=transz[1]+.1*transz[0]
    alpha[1]=alpha[1]+.1*alpha[0]
    if 0<=teta[1]+.01*teta[0]<=1:
        teta[1]=teta[1]+.01*teta[0]

    #les rotations et translations de la piece
    glTranslatef(0,0,transz[1])
    #       glRotatef(alpha, 0, 1, 0)
    
    gluLookAt(cos(alpha[1])*2, sin(teta[1])*2, sin(alpha[1])*2, 0, 0, 0, 0, 1, 0)

    for thing in drawables :
        if thing.type == "non static":
            thing.move()
        thing.draw() #ceci appelle les methodes de dessin de tous les objets qui doivent etre dessines..

    myBonhomme.move()
    myBonhomme.draw()
        
    glutSwapBuffers()

def keyPressed(*args):
    global transz, teta, alpha
    if args[0] == 'r':
        teta[0] = 1
    if args[0] == 'f':
        teta[0] = -1
    if args[0] == 'd':
        alpha[0] = -1
    if args[0] == 'g':
        alpha[0] = 1

    if args[0] == 's':
        transz[0] = -1
    if args[0]== 'z':
        transz[0] = 1

def keyReleased(*args):
    global transz, teta, alpha
    if args[0] == 'r' or args[0] == 'f':
        teta[0] = 0

    if args[0] == 'd' or args[0] == 'g':
        alpha[0] = 0
    
    if args[0] == 's' or args[0]== 'z':
        transz[0] =0


def specialKeyPressed(key, x, y):
    global game
    #celles ci servent a faire bouger le bonhomme.
    if key == GLUT_KEY_UP :
        globjects.forward = -1
    if key == GLUT_KEY_DOWN:
        globjects.forward = 1
    if key == GLUT_KEY_LEFT:
        globjects.direction = -1
    if key == GLUT_KEY_RIGHT:
        globjects.direction = 1


def specialKeyReleased(key, x, y):
    if key == GLUT_KEY_UP :
        globjects.forward = 0
    if key == GLUT_KEY_DOWN:
        globjects.forward = 0
    if key == GLUT_KEY_LEFT:
        globjects.direction = 0
    if key == GLUT_KEY_RIGHT:
        globjects.direction = 0



def myMouseMove (x, y):
    global xold
    if xold<x:
        diff = x-xold
    #     alpha = diff
    
    if xold>x:
        diff = xold-x
#   alpha = -diff



def Mouseclick (button, state, x, y):
    
    if GLUT_LEFT_BUTTON == button and state==0:
        print "mouse click"

    if GLUT_RIGHT_BUTTON == button and state == 0 :
        print ("right_click")

def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_RESCALE_NORMAL)
    glShadeModel(GL_SMOOTH)
    
    glEnable(GL_TEXTURE_2D)
    #    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    LoadTextures()


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



main()
