

#piece1 =[[[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]],[[0,0,0,0],[0,0,1,1],[0,1,1,0],[0,0,0,0]],[[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]],[[0,0,0,0],[0,0,1,1],[0,1,1,0],[0,0,0,0]]]  


# O 
# O O
#   O


#piece2 = [[[0,0,2,0],[0,2,2,0],[0,2,0,0],[0,0,0,0]],[[0,0,0,0],[0,2,2,0],[0,0,2,2],[0,0,0,0]],[[0,0,2,0],[0,2,2,0],[0,2,0,0],[0,0,0,0]],[[0,0,0,0],[0,2,2,0],[0,0,2,2],[0,0,0,0]]]     
    
#   O
# O O
# O



#piece3 = [[[0,3,0,0],[0,3,0,0],[0,3,0,0],[0,3,0,0]],[[3,3,3,3],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,3,0,0],[0,3,0,0],[0,3,0,0],[0,3,0,0]],[[3,3,3,3],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]      

# O
# O
# O
# O
 

#piece4 = [[[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]],[[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]],[[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]],[[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]]]

# O O
# O O 
    
#piece5 = [[[0,5,0,0],[0,5,5,0],[0,5,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,5,0],[0,5,5,5],[0,0,0,0]],[[0,0,0,5],[0,0,5,5],[0,0,0,5],[0,0,0,0]],[[0,5,5,5],[0,0,5,0],[0,0,0,0],[0,0,0,0]]]     

# O
# O O
# O

#piece6 = [[[0,0,6,0],[0,0,6,0],[0,6,6,0],[0,0,0,0]],[[0,0,0,0],[0,6,6,6],[0,0,0,6],[0,0,0,0]],[[0,6,6,0],[0,6,0,0],[0,6,0,0],[0,0,0,0]],[[0,0,0,0],[0,6,0,0],[0,6,6,6],[0,0,0,0]]]     

#   O
#   O
# O O 

#piece7 = [[[0,7,0,0],[0,7,0,0],[0,7,7,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,7],[0,7,7,7],[0,0,0,0]],[[0,7,7,0],[0,0,7,0],[0,0,7,0],[0,0,0,0]],[[0,0,0,0],[0,7,7,7],[0,7,0,0],[0,0,0,0]]]     

# O
# O
# O O

#alors j'ai mis tout ca ici parce que pour lire c'est plus pratique :)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys,threading,random

ESCAPE = '\033'

x=4
y=12

piececolor=[0,1,0]
piececolor2=[1,0,0]
piececolor3=[0,0,1]
piececolor4=[1,1,0]
piececolor5=[1,0,1]
piececolor6=[0,1,1]
piececolor7=[1,0.2,0.4]

direct = "f"


# Number of the glut window
window = 0


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

#Les pieces. J'en ai fait des objets, c'est plus pratique a utiliser, et ce sera beacoup plus simple d'ajouter les rotation.
#comme tu l'avais tres bien fait, une piece, c'est une liste de carrés. Mais pour bouger tous les carrés en meme temps, i faut qu'ils partent tous du meme point, et ce point on doit y avoir acces facilement. Alors ce point c'est maintenant ton instance de ton objetc (appelons le mapiece) comme ceci : mapiece.Ax, meme principe pour le y...


class piece1(object):
    def __init__(self):
        self.x = 4
        self.y = 12
        self.color =[0,1,0]  # green
        self.list = [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color)]
    
    def down(self):
        self.y -= 1

    def move(self):
        if direct = "d":
            self.y -= 1



piece2 = [carre(x,y,piececolor2),carre(x,y-1,piececolor2),carre(x-1,y-1,piececolor2),carre(x-1,y-2,piececolor2)] #red
piece3 = [carre(x,y,piececolor3),carre(x,y-1,piececolor3),carre(x,y-2,piececolor3),carre(x,y-3,piececolor3)] #line
piece4 = [carre(x,y,piececolor4),carre(x+1,y,piececolor4),carre(x,y-1,piececolor4),carre(x+1,y-1,piececolor4)] #square
piece5 = [carre(x,y,piececolor5),carre(x,y-1,piececolor5),carre(x+1,y-1,piececolor5),carre(x,y-2,piececolor5)] #t
piece6 = [carre(x+1,y,piececolor6),carre(x+1,y-1,piececolor6),carre(x+1,y-2,piececolor6),carre(x,y-2,piececolor6)] #anti - L
piece7 = [carre(x,y,piececolor7),carre(x,y-1,piececolor7),carre(x,y-2,piececolor7),carre(x+1,y-2,piececolor7)] # L


#newspiece=

piecerandom=[piece7]

pieceR = random.choice(piecerandom)

def move():
    #ne sert que a faire descendre la piece...
    threading.Timer(0.8, move).start()
    global x
    global y
    global direct
    global pieceR
    

    if y>3 :
        if direct == 'd' :
            x+=1
        if direct == 'q' :
            x-=1
     
        if y<=12 :
            y-=1
    if y<=3 :
        y=3


    pieceR = random.choice(piecerandom)




#FABRICATION
#Grille de jeu

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
    global piece1,piece2,piece3,piece4,piece5,piece6,piece7,piecerandom,pieceR
    global x
    global y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
    glLoadIdentity()	# Reset The View
    glTranslatef(-5.,-7.0,-15.0)	# Move Into The Screen


    #DESSIN

    for item in  pieceR :
          item.draw()

    for item in grille :
          for trucs in item :
                trucs.draw()
  
    
    glutSwapBuffers()


def keyPressed(key, x, y):
    global window
    global direct, stop

    # Si t ou echap presse, tout effacer
    if key == ESCAPE or key == 't':
        sys.exit()

    if key == 'd':
          direct = 'd'
          


    if key == 'q':
          direct = 'q'


    if key == 's':
          direct = 's'


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


move()
main()
