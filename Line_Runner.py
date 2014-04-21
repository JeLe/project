#importation de ttes les 'libraries' necessaires pour le programme 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *
from random import *

ESCAPE = '\033'

# variables pour la fenetre du programme 
window = 0
alpha =0

#variables pour le score et l'acceleration au cours du jeu
score=0
upscore=5
acceleration=10
increment=0.01


#creation de l'objet 'player' (ce sera le personnage/le 'truc' qui devra eviter les obstacles dans le jeu)
class player (object):
    def __init__ (self, Ax, Ay, couleur):
        self.red = couleur[0]
        self.green = couleur[1]
        self.blue = couleur[2]
        self.Ax = Ax
        self.Ay = Ay
    
    def getvertices(self):
        self.vertices = [[self.Ax,self.Ay,0],[self.Ax,self.Ay+.3,0],[self.Ax+0.3,self.Ay+.3,0],[self.Ax+.3,self.Ay,0]]
        
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
        global increment
        #ici il ne faut pas que ca reste += .01, because sinon ca ne va pas accelerer ! Il faut ajouter -increment a chaque faois !!
        self.Ax -= increment
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

#liste faisant apparaitre les premiers obstacles du jeu
list1=[carre(0.9,0.5,[0.8,0.2,0.1]),carre(0.9,0.1,[.0,.4,.5]),carre(0.9,0.8,[0.1,.8,.6])]

def NewObstacle(counter):
    x=randint in range(0,5)
    y=randint in range(0,5)
    list1[counter]=carre(x/10,y/10,[0.5,0.2,0.7])
    global score, upscore, acceleration, increment #plus bas tu utilise des variables non declarees comme globales, alos je les ai declarees..
    #deans la ligne suivante tu utilise une variable qui nexiste pas (points.) alors qu'elle s'appelle score...
    score+=upscore
    increment+=0.05

    if score>acceleration: # pourquoi > acceleration ??? faudrait plutot une barriere plus arbitraire non ? parce qu'acceleration, c'est bizzare comme truc..
        #d'ailleurs il sert a quoi acceleration ..
        upscore+=2
        acceleration+=100*0.5*upscore
        print(score)
    
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
    #condition pour la mort du joueur:
    if (monplayer.Ax < moncarre.Ax < monplayer.Ax+0.3 or monplayer.Ax<moncarre.Ax+0.5<monplayer.Ax+0.3)  and (monplayer.Ay<=moncarre.Ay<=monplayer.Ay+0.3 or monplayer.Ay<=moncarre.Ay+0.5<=monplayer.Ay+0.3):
        sys.exit()
    #conditions pour que le joueur reste dans l'ecran
    if monplayer.Ay>=1.7:
        monplayer.Ay=1.7
    if monplayer.Ay<=-2:
        monplayer.Ay=-2
    #condition pour faire apparaitre les nouveaux obstacles
    if moncarre.Ax<=monplayer.Ax:
        counter=0
        for item in list1:
            if item.Ax<=-0.5:
                item=NewObstacle(counter)
            counter+=1
	    
    # dessinnr les carres de la liste1
    for item in list1:
        item.getvertices()
        item.drawcarre()

    
        ##############################################
        
    glutSwapBuffers()   
    
    #on defini ici les touches et les actions correspondantes
def keyPressed(*args):
    global window
    global alpha
    if args[0] == ESCAPE or args[0] == 'q': # Si on appuie sur 'q' ou 'echap', ferme le programme
        sys.exit()
    if args[0] == 'z': #si on appuie sur 'z' le personnage se deplace vers le haut
        monplayer.Ay+=0.1
    if args[0] == 's': #si on appuie sur 's' le personnage se deplace vers le bas
	monplayer.Ay-=0.1

def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(640, 480) #defini la taille de la fenetre
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow( "Line_Runner")  #donne un nom a la fenetre
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

main()
