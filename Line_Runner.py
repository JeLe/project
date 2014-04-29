#importation de ttes les 'libraries' necessaires pour le programme
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *
from random import *

ESCAPE = '\033'

# variables pour la fenetre du programme 
window = 1
alpha =0

#variables pour le score et l'acceleration au cours du jeu
score=0
upscore=5
value=10
increment=0.2
pausedIncrement =0
updown =0


#creation de l'objet 'player' (ce sera le personnage/le 'truc' qui devra eviter les obstacles dans le jeu)
class player (object):
    def __init__ (self, Ax, Ay, couleur):
        self.red = couleur[0]
        self.green = couleur[1]
        self.blue = couleur[2]
        self.Ax = Ax
        self.Ay = Ay
    
    def getvertices(self):
        global updown
        self.Ay += updown*0.01

        if -2.02<=monplayer.Ay<=-2.:
            monplayer.Ay = -2
        
        if 1.7<=monplayer.Ay<=1.72:
            monplayer.Ay = 1.7
        
        self.vertices = [[self.Ax,self.Ay,0],[self.Ax,self.Ay+.3,0],[self.Ax+0.3,self.Ay+.3,0],[self.Ax+.3,self.Ay,0]]
        
    def drawplayer(self):
        self.getvertices()
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
        global increment
        self.Ax -= increment
        self.vertices = [[self.Ax,self.Ay,0],[self.Ax,self.Ay+0.5,0],[self.Ax+0.5,self.Ay+0.5,0],[self.Ax+0.5,self.Ay,0]]
      
    def drawcarre(self):
        self.getvertices()
        glBegin(GL_QUADS)
        glColor3f(self.red, self.green, self.blue)
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()
       
#creation d'un player en precisant ses parametres (coordonnees, couleur)        
monplayer = player (-1.7,-0.9,[1.,1.,0.0])

#ok alors des fois y'a que deux carres pace qu'il... en fait j'en sais rien !!!
#alors cette liste, c'est les valeurs possibles pour y : choice, ca prend un element de la liste au hazard...
testValues = [0., 5., 10., 15., 20., 25., 30., 35.] #du coup quand on leu mets des points c'est mieux... :)

def NewObstacle(counter):
    #x=choice(testValues)
    x=randint(5,55)
    y=choice(testValues)#randint(0,37)
    a=random()
    b=random()
    c=random()
    list1[counter]=carre(2.5+x/10,-2+y/10,[a,b,c])
    global score, upscore, value, increment
    score+=upscore
    if score>value: 
        increment+=0.003
        upscore+=2
        value+=10*upscore
    print(score)



#liste faisant apparaitre les premiers obstacles du jeu
list1=[carre(2,-2,[0,0,0]), carre(2,-2,[0,0,0]), carre(2,-2,[0,0,0]), carre(2,-2,[0,0,0])]
#petit truc pour que meme les trois premiers soient random
for i in range (0,4):
    NewObstacle(i)

#faut remettre les valeurs initiales de ca, sinon c'est tout casse..
score=0
upscore=5
value=10
increment=0.01


# Fonction d'initialisation d'OpenGL. Defini les parametres principaux.
def InitGL(Width, Height):			         	# On l'appelle juste apres que la fenetre OpenGL ait ete creee.
    glClearColor(0, 0, 0, 0.0)     #glClearColor(0.2, 0.5, 0.8, 0.0)                            # permet de changer la couleur de fond de la fenetre
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
    monplayer.drawplayer()

    #condition pour faire apparaitre les nouveaux obstacles
    counter=0
    for item in list1:
        if item.Ax<=-3.2:
            NewObstacle(counter)
        counter+=1

    # dessiner les carres de list1

        item.drawcarre()

    #condition pour la mort du joueur:

        if (item.Ax<=monplayer.Ax<=item.Ax+.5 or item.Ax<=monplayer.Ax+0.3<=item.Ax+0.5)  and (item.Ay<=monplayer.Ay<=item.Ay+.5 or item.Ay<=monplayer.Ay+.3<=item.Ay+.5):
            sys.exit()

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
def keyPressed(*args):
    global window
    global alpha
    global increment, pausedIncrement, updown
    
    if args[0] == ESCAPE or args[0] == 'q': # Si on appuie sur 'q' ou 'echap', ferme le programme
    #glutDestroyWindow(window)
        sys.exit()


    if pausedIncrement == 0 :
        if args[0] == 'a' or args[0] == 'A':#and monplayer.Ay<=1.7: #si on appuie sur 'z' le personnage se deplace vers le haut
            updown = 1
            #monplayer.Ay+=0.1
        if args[0] == 'f' or args[0] == 'F':#and monplayer.Ay>=-2.: #si on appuie sur 's' le personnage se deplace vers le bas
            updown = -1
            #monplayer.Ay-=0.1

    if args[0] == 'p': #si on appuie sur 'p' ca fait pause !
        
        if pausedIncrement == 0 :
            pausedIncrement = increment
            increment = 0
        else : #ca ca depause
            increment = pausedIncrement
            pausedIncrement = 0

#high score : 2990


def keyReleased(*args):
    global increment, pausedIncrement, updown
    
    if args[0] == 'a' or args[0] == 'f' or args[0] == 'A' or args[0] == 'F' :
        updown = 0



def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(640, 480) #defini la taille de la fenetre
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow( "Line_Runner")  #donne un nom a la fenetre
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)

    glutIgnoreKeyRepeat(1)
    glutKeyboardFunc(keyPressed)
    glutKeyboardUpFunc(keyReleased)

    glutFullScreen()

    InitGL(640, 480)

    glutMainLoop()

main()
