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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

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

direct = 0


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


#Pour bouger tous les carres en meme temps, ils faut qu'ils partent tous du meme point, et ce point on doit y avoir acces facilement. Alors ce point c'est maintenant ton instance de ton objetc (appelons le mapiece) comme ceci : mapiece.Ax, meme principe pour le y...   (PAS UNDERSTAND, fin on le retrouve ou ?)


class piece1(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[0,1,0]  # vert / S a droite
        self.list = [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color)]

class piece2(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[1,0,0]  # rouge / S a gauche
        self.list = [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x-1,self.y-2,self.color)]
    
class piece3(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[0,0,1]  # bleu / ligne
        self.list = [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x,self.y-3,self.color)]
    
class piece4(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[1,1,0]  # jaune / carre
        self.list = [carre(self.x,self.y,self.color),carre(self.x+1,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]
    
class piece5(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[1,0,1]  # violet / T
        self.list = [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y-2,self.color)] 
    
class piece6(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[0,1,0]  # cyan  / anti L
        self.list = [carre(self.x+1,self.y,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color),carre(self.x,self.y-2,self.color)] 
    
class piece7(object):
    def __init__(self):
        self.x = 4 
        self.y = 12
        self.color =[1,0.2,0.4]  # orange / L
        self.list = [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x+1,self.y-2,self.color)] 
    
    
    #ca c'est pour recuperer ta fameuse liste que tu avais au depart. Sauf que la en plus tu peux mettre les autres listes pour la rotation et faire un truc qui choisit la bonne :) ( LISTE TOUT EN HAUT ? OU DU COUP JPEUX METTRE MES OBJETS PIECES ? )
    def getSquareList(self):
        test = true # cette ligne c'est juste pour eviter une erreur, il faut qua tu ecrives ta methode...
        self.bas #il faut aussi que ici tu mette un parametre a ton objet pour savoir ou est le bas... Comme ca tu compares ce parametre a ce qui representera le bas pour savoir si il est atteint ou pas..
    
    #cette methode descend ton objet, il faut l'appeler dans le timer... (JE L'AI APPELE DANS LE MOVE OU YA LE TIMER) ( MAIS VOILA YA DEUX MOVE ..)
    def down(self):
        self.y -= 1 

    #ca c'est pour bouger de gauche a droite. Il faut pourvoir le faire plus d'une fois par timer, donc on l'appelle a chaque fois qu'une touche est enfoncee. c'est a dire dans la fonction Keypressed ! ( LE PERMIER MOVE(SELF) )
    def move(self):
        self.y += direct
        direct = 0

    def draw(self):
        test = true
        #alors ici il faut que tu prenne le self.list rafraichit (c'est a dire apres avor appele la methode getSquareList, et que tu fasse une boucle pour appeler la methode draw de chaque element (les instances de la classe carre ) de ta liste.



def randomPiece():
    test = true #meme principe : faut que tu te fasse ta fonction ! alors soit tu fait comme t'avais fait, tu fais une liste d'instances de classes pieces (une de chaque) et tu fait ton choice
    #tu peux donc par exemple faire ta liste comme ceci
    piecerandom = [piece1(), piece2(), etc] #avec piece1 et tout ca etant des classes et entre les () tu mets ce qu'il faut quoi !
    pieceR = random.choice(piecerandom)     #du coup cette ligne tu peux peut etre la garder :)

def bas():
    test = true #si tu continue a lire mes commentaires ti verras ce que c'est que cette fonction :)
    # du coup pour comprendre cette fonction va voir le commentaire dans le timer et apres reviens ici.
    #c'est donc ici qu'il faut placer tes if : pour savoir si t'est en bas, et si c'est le cas tu as deux choses a faire : ajouter la piece qui viens d'atterrir a ce qui represente la ligne du bas, puis appeler ta fonction randomPiece() pour refaire une piece qui recomence a descendre.
    #c'est peut etre aussi dans cette fonction qu'il faudrait regarder si tu as fait une ligne et si oui te rajouter des points dans une variable globale :)

def move():
    threading.Timer(0.8, move).start()     # (ET LA LE DEUXIEME MOVE )
    #global x
    #global y
    #global direct
    #du coup tu n'as plus besoin que de ta variable globale qui est l'objet qui est en train de descendre !
    global pieceR  #mais tu n'auras pas besoin de cette ligne, car c'est un objet...     (DONC LA JE COMPREND PAS DU COUP, JE SAIS PLUS QUOI GARDER)
    
    down()
    
   
    if pieceR.y>3 :
        #j'ai enleve le truc du x, il est deja apelle dans le keyboardfunc...
        #mais ici on fait descendre la piece
        pieceR.down()
        

    if pieceR.y<=3 : #ca ca veut dire que ta piece est arrivée en bas...
        #alors il va faloir gerer une representation dynamique de ce qu'est le bas. C'est a dire que une fois qu'on a commence a jouer le bas n'est plus juste une ligne...
        #donc moi je te propose de faire une nouvelle fonction par exemple bas(), que j'ai declaree plus haut, et qui va regarder si le pieceR.bas est sur la ligne du bas et si c'est le cas va faire en sorte d'incorporer cette piece qui vient d'atterir dans ce que tu choisira pour representer le bas, soit un objet, soit une liste ou ce que tu veux, mais choisit bien parce que ca va deja etre assez galere comme ca .... :( Du coup les ifs de cette fonction ne servent plus a grand chose, il faudra juste appeler ta nouvelle fonction bas avant de descendre ta piece..
        test = true#et donc pour l'instant je te mets ma super ligne qui ne sert a rien mais evite une erreur d'indentation a cause du if :




#FABRICATION
#Grille de jeu

# est ce qu'elle sert vraiment a qqch ta grille ? parce qu'en fait t'es parti avec des pieces independantes et pas des etats de pixels (les carres de la gille...) mais c'est pas grave du tout c'est ta facon de faire et ca marche tout aussi bien :)
# cela dit laisse la ou elle est pour l'instant... elle ne gene personne !

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

    pieceR.draw()

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
          direct = 1

    if key == 'q':
          direct = 0

    if key == 's':
          direct = -1

    move()


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

#alors maintenant avant d'appeler tes fonctions (move() et main()), il faut creer une premiere piece qui descend et qui est choisie aleatoirement :
randomPiece()

move()
main()
