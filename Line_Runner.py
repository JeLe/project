#importation de ttes les 'libraries' necessaires pour le programme
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *
from random import *

ESCAPE = '\033'

# variables pour la fenetre du programme
LRwindow = 1
stop = 0

#variables pour le score et l'acceleration au cours du jeu
LRscore=0
LRupscore=5
LRvalue=10
LRincrement=0.2
LRpausedIncrement =0
LRupdown =0


#creation de l'objet 'player' (ce sera le personnage/le 'truc' qui devra eviter les obstacles dans le jeu)
class LRplayer (object):
    def __init__ (self, Ax, Ay, couleur):
        self.red = couleur[0]
        self.green = couleur[1]
        self.blue = couleur[2]
        self.Ax = Ax
        self.Ay = Ay

    def getvertices(self):
        global LRupdown
        self.Ay += LRupdown*0.01

        if -2.02<=self.Ay<=-2.:
            self.Ay = -2

        if 1.7<=self.Ay<=1.72:
            self.Ay = 1.7

        self.vertices = [[self.Ax,self.Ay,0],[self.Ax,self.Ay+.3,0],[self.Ax+0.3,self.Ay+.3,0],[self.Ax+.3,self.Ay,0]]

    def drawplayer(self):
        self.getvertices()
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()

#creation de l'objet 'carre' (ce seront les obstacles dans le jeu)
class LRcarre (object):
    def __init__ (self, Ax, Ay, couleur):
        self.red = couleur[0]
        self.green = couleur[1]
        self.blue = couleur[2]
        self.Ax = Ax
        self.Ay = Ay

    def getvertices(self):
        global LRincrement
        self.Ax -= LRincrement
        self.vertices = [[self.Ax,self.Ay,0],[self.Ax,self.Ay+0.5,0],[self.Ax+0.5,self.Ay+0.5,0],[self.Ax+0.5,self.Ay,0]]

    def drawcarre(self):
        self.getvertices()
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()

#creation d'un player en precisant ses parametres (coordonnees, couleur)
LRmonplayer = LRplayer (-1.7,-0.9,[1.,1.,0.0])

#ok alors des fois y'a que deux carres pace qu'il... en fait j'en sais rien !!!
#alors cette liste, c'est les valeurs possibles pour y : choice, ca prend un element de la liste au hazard...
LRtestValues = [0., 5., 10., 15., 20., 25., 30., 35.] #du coup quand on leu mets des points c'est mieux... :)

def LRnewObstacle(counter):
    #x=choice(LRtestValues)
    x=randint(5,55)
    y=choice(LRtestValues)#randint(0,37)
    a=random()
    b=random()
    c=random()
    LRlist1[counter]=LRcarre(2.5+x/10,-2+y/10,[a,b,c])
    global LRscore, LRupscore, LRvalue, LRincrement
    LRscore+=LRupscore
    if LRscore>LRvalue:
        LRincrement+=0.003
        LRupscore+=2
        LRvalue+=10*LRupscore
    print(LRscore)



#liste faisant apparaitre les premiers obstacles du jeu
LRlist1=[LRcarre(2,-2,[0,0,0]), LRcarre(2,-2,[0,0,0]), LRcarre(2,-2,[0,0,0]), LRcarre(2,-2,[0,0,0])]
#petit truc pour que meme les trois premiers soient random
for i in range (0,4):
    LRnewObstacle(i)

#faut remettre les valeurs initiales de ca, sinon c'est tout casse..
LRscore=0
LRupscore=5
LRvalue=10
LRincrement=0.01


# Fonction d'initialisation d'OpenGL. Defini les parametres principaux.
def LRinitGL(Width, Height):			         	# On l'appelle juste apres que la fenetre OpenGL ait ete creee.
    glClearColor(0, 0, 0, 0.0)     #glClearColor(0.2, 0.5, 0.8, 0.0)                            # permet de changer la couleur de fond de la fenetre
    glShadeModel(GL_SMOOTH)                      	# Enables Smooth Color Shading
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					                # Reset The Projection Matrix
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_RESCALE_NORMAL)

    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)










def LRreSizeGLScene(Width, Height):
    if Height == 0:						        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)		               # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Fonction principale pour dessiner les objets a l'ecran.
def LRdrawGLScene():

    glClear(GL_COLOR_BUFFER_BIT)	# Clear The Screen Buffer
    glLoadIdentity()					# Reset The View
    glTranslatef(0.,0.0,-5.0)			# Move Into The Screen
    LRmonplayer.drawplayer()

    #condition pour faire apparaitre les nouveaux obstacles
    counter=0
    for item in LRlist1:
        if item.Ax<=-3.2:
            LRnewObstacle(counter)
        counter+=1

    # dessiner les carres de list1

        item.drawcarre()

    #condition pour la mort du joueur:

        if (item.Ax<=LRmonplayer.Ax<=item.Ax+.5 or item.Ax<=LRmonplayer.Ax+0.3<=item.Ax+0.5)  and (item.Ay<=LRmonplayer.Ay<=item.Ay+.5 or item.Ay<=LRmonplayer.Ay+.3<=item.Ay+.5):
            global LRincrement, stop
            LRincrement = 0
            stop = 1
    #conditions pour que le joueur reste dans l'ecran
    #elles sont maintenant dans le keypresed, pour eviter que le joueur soit dessine pouis remonte, ca faisait un petit truc moche quoi, mais rien de dramatique... mais moi ca m'enervait :)

    glBegin(GL_LINES)
    glVertex3f(-2, -2, 0)
    glVertex3f(2, -2, 0)
    glVertex3f(-2, 2, 0)
    glVertex3f(2, 2, 0)
    glEnd()


        ##############################################

    glutSwapBuffers()

    #on defini ici les touches et les actions correspondantes
def LRkeyPressed(args):
    global LRwindow
    global LRincrement, LRpausedIncrement, LRupdown

    if args[0] == ESCAPE or args[0] == 'q': # Si on appuie sur 'q' ou 'echap', ferme le programme
    #glutDestroyWindow(window)
        sys.exit()


    if LRincrement != 0 :
        if args[0] == 'a' or args[0] == 'A':#and monplayer.Ay<=1.7: #si on appuie sur 'z' le personnage se deplace vers le haut
            LRupdown = 1
            #monplayer.Ay+=0.1
        if args[0] == 'f' or args[0] == 'F':#and monplayer.Ay>=-2.: #si on appuie sur 's' le personnage se deplace vers le bas
            LRupdown = -1
            #monplayer.Ay-=0.1

    if args[0] == 'p': #si on appuie sur 'p' ca fait pause !

        if LRpausedIncrement == 0 :
            LRpausedIncrement = LRincrement
            LRincrement = 0
        else : #ca ca depause
            LRincrement = LRpausedIncrement
            LRpausedIncrement = 0



#high score jele: 2990


def LRkeyReleased(args):
    global LRincrement, LRpausedIncrement, LRupdown

    if args[0] == 'a' or args[0] == 'f' or args[0] == 'A' or args[0] == 'F' :
        LRupdown = 0



def LRmain():
    global LRwindow
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(640, 480) #defini la taille de la fenetre
    glutInitWindowPosition(0, 0)
    LRwindow = glutCreateWindow( "Line_Runner")  #donne un nom a la fenetre
    glutDisplayFunc(LRdrawGLScene)
    glutIdleFunc(LRdrawGLScene)
    glutReshapeFunc(LRreSizeGLScene)

    glutIgnoreKeyRepeat(1)
    glutKeyboardFunc(LRkeyPressed)
    glutKeyboardUpFunc(LRkeyReleased)

#glutFullScreen()

    LRinitGL(640, 480)

    glutMainLoop()

#LRmain()
