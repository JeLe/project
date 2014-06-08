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
alpha = 0
transz = 0
teta = 0
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

#La fonction ou on dessine tout a l'ecran
def DrawGLScene():
    # Clear The Screen And The Depth Buffer, load the current and only matrix
    global alpha, transz, teta, game

    if game == 1 and Line_Runner.stop == 0:
        Line_Runner.LRdrawGLScene()
    elif game == 2 and tetris.dead == 0:
        tetris.DrawGLScene()
    elif game == 3 and snake.dead == 0:
        snake.DrawGLScene()
    else :
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()

#la premiere translation de la piece vers l'arriere, afin qu'elle entre dans notre champ de vision
        glTranslatef(0., -3.0, -10.0)
        #glTranslatef(-myBonhomme.Ax, 0.0, -myBonhomme.Az)
        

#les rotations et translations de la piece
        glTranslatef(0,0,transz)
#       glRotatef(alpha, 0, 1, 0)

        gluLookAt(0, 3, 5, 0, 0, 0, 0, 1, 0)
        #        glRotatef(5, 1, 0, 0)#used to be teta..


    ######################################
    #ici sont nos tests de lumiere, ils ne sont pas actifs, car il fallait decommenter la ligne glEnable(GL_LIGHTING) dans la faonction initGL

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, numpy.array((0.01, 0.01, 0.01, 0.5), 'f'))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, numpy.array((1., 1., 1., 1.0), 'f'))


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
    if game == 0:
#si echape ou q est touche, l'application est fermee
        if args[0] == ESCAPE :
            sys.exit()

#zooms et rotations manuelles
#le teta fait pivoter la salle sur l'axe z, ce qui est nul, mais utile pour certains tests. C'est pour cela qu'on le fait saturer
        if args[0] == 'r' and teta<30:
            teta += 2
        if args[0] == 'f' and teta>-45:
            teta += -2
    
        if args[0] == 's':
            transz += -1.
        if args[0]== 'z':
            transz += 1.


    if args[0]== 't':
        game = 0
        tetris.dead = 1

#ici on appelle la fonction de clavier du line runner, en lui envoyant les arguments recus, c'est a dire les entrees du clavier
    if game == 1:
        Line_Runner.LRkeyPressed(args)
    elif game == 2:
        tetris.keyPressed(args[0], args[1], args[2])
    elif game == 3:
        snake.keyPressed(args[0], args[1], args[2])



#la fonction qui est appellee si une touche est relachee.
def keyReleased(*args):
    global game
    #meme principe que quand une touche est enfoncee
    if game ==1 :
        Line_Runner.LRkeyReleased(args)


#les fonctions qui sont appellees lorsqu'une touche dite speciale est enfoncee ou relachee. Ici on ne regarde que les etats des touches directionnelles.

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





def launcher(id):
    global game
    if id == 'LR':
        game = 1
        Line_Runner.stop = 0
        
    if id == 'tetris':
        game = 2
        tetris.dead = 0
    
    if id == 'snake':
        print("rout")
        game = 3
        snake.reset()

    glDisable(GL_DEPTH_TEST)





#si il y a un clique, on regarde si le bonhomme se trouve dans une porte quelconque...
def Mouseclick (button, state, x, y):

    if GLUT_LEFT_BUTTON == button and state==0: #state == 0 signifie que le bouton de la souris est enfonce.
        for element in gates :
            if element.checkifgate() != 0 :
                print (element.checkifgate())

                launcher(element.checkifgate())
                #si la borne a pour identifiant LR, on lance le Line_runner.


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
