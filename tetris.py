from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys,threading,random

ESCAPE = '\033'

direct = 0
score = 0
dead = 0

# Number of the glut window
window = 0


class carre(object):

    def __init__(self,x,y,couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
    def getVertices(self):
        self.vertices = [[self.x,self.y,0],[self.x,self.y+1, 0],[self.x+1, self.y+1, 0],[self.x+1,self.y, 0]]

    def draw(self):
        self.getVertices()
        glBegin(GL_QUADS)
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2]) #ca permet de changer la couleur facilement pour faire des tests
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()


##ici pour le sol, moi j'aime bien les objets alors j'en fait un !
class floor(object):
    def __init__(self):
        self.top = []
        for i in range(0, 12):
            self.top.append(carre(i, 0, [0, 1, 0]))
        self.bottom = []
    
    def checkLine(self):
        for i in range(1,20):
            counter = 0
            for thing in self.top:
                if thing.y == i:
                    counter+=1
            if counter == 12:
                global score
                score+=1
                for thing in self.top :
                    if thing.y == i:
                        thing.y = 0
                    if thing.y> i:
                        thing.y -=1
                self.checkLine()
                print (score)

    def draw(self):
        for item in self.top:
            item.draw()
        for item in self.bottom:
            #for thing in item:
            item.draw()


#Pour bouger tous les carres en meme temps, ils faut qu'ils partent tous du meme point, et ce point on doit y avoir acces facilement. Alors ce point c'est maintenant ton instance de ton objetc (appelons le pieceR) comme ceci : pieceR.x, meme principe pour le y...   (PAS UNDERSTAND, fin on le retrouve ou ?)


class piece(object):
    def __init__(self):
        self.x = 4 
        self.y = 20
        self.index = random.randint(0,6)
        self.config = 0
        ## et la c'est une liste des couleurs dans le meme ordre que les pieces !
        colorList =[[1,0.2,0.4], [0,1,1], [1,0,1], [1,1,0], [0,0,1], [1,0,0], [0,1,0]]
        self.color = colorList[self.index]
        #ca c'est la liste de toutes les pieces comme ca on peut faire un random choice dedans, puisque les methodes ci dessous sont les memes pour toutes les pieces !
        ##chaque liste dans la liste c'est une config ... comme ca on peux tourner tranquille :)
        self.totalList = [[[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x+1,self.y-2,self.color)], [carre(self.x-1,self.y-1,self.color), carre(self.x,self.y-1,self.color), carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y,self.color)], [carre(self.x,self.y-2,self.color), carre(self.x,self.y-1,self.color), carre(self.x,self.y,self.color),carre(self.x-1,self.y,self.color)],  [carre(self.x-1,self.y-1,self.color), carre(self.x,self.y-1,self.color), carre(self.x+1,self.y-1,self.color),carre(self.x-1,self.y-2,self.color)]],
                
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x-1,self.y-2,self.color)],[carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color)],[carre(self.x,self.y-2,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y,self.color),carre(self.x+1,self.y,self.color)],[carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x-1,self.y,self.color)]],
                          
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y-2,self.color)],[carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y,self.color)], [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-2,self.color)], [carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y-2,self.color)]],
                          
                          
                    [[carre(self.x,self.y,self.color),carre(self.x+1,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]],
                          
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x,self.y-3,self.color)],[carre(self.x-2,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]],
                          
                          
                [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x-1,self.y-2,self.color)],[carre(self.x-1,self.y,self.color),carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]],
                          
                          
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color)],[carre(self.x+1,self.y,self.color),carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color)]]]
        self.list = self.totalList[self.index][self.config]
    

    def checkOnFloor(self):
        flag =0
        for thing in self.list:
            for item in sol.top:
                if item.x == thing.x and item.y+1 == thing.y:
                    flag = 1
                if flag == 1 and thing.y>=18:
                    flag = 2
        if flag ==1: ##this flag avoids a serious bug ! Believe me..., and avoids appending duplicates to sol.top
            for item in self.list:
                sol.top.append(item) #on peux se permettre d'utiliser l'instance de sol parce que il n'y en aura toujours qu'un !
            sol.checkLine()
            self.__init__()
        if flag == 2:
            global dead
            dead = 1
            print(dead)

    def checkBoundries(self):
        global direct
        #this loop checks the sides
        for thing in self.list:
            if thing.x+direct ==-1 or thing.x+direct == 12 :
                return 0
        #this loop checks if it lands on other pieces already in self.top
        for thing in self.list:
            for item in sol.top:
                if thing.y == item.y and thing.x+direct == item.x:
                    return 0
        return 1 #never reached if there is a problem

    #cette methode descend ton objet, il faut l'appeler dans le timer... (JE L'AI APPELE DANS LE MOVE OU YA LE TIMER) ( MAIS VOILA YA DEUX MOVE ..)
    ##oui c'est ce qu'il fallait faire :)
    def down(self):
        self.checkOnFloor()
        self.y -=1
        for item in self.totalList[self.index]:
            for thing in item:
                thing.y-= 1
        self.list = self.totalList[self.index][self.config]

    def changeConfig(self, spin):
        oldConfig = self.config
        self.config = self.config+spin
        if self.config == len(self.totalList[self.index]):
            self.config =0
        if self.config == -1:
            self.config = len(self.totalList[self.index])-1

        self.list = self.totalList[self.index][self.config]
        # ici je ne comprends pas pourquoi ca ne marche pas...
        if self.checkBoundries() == 0:
            self.list = self.totalList[self.index][oldConfig]

    #ca c'est pour bouger de gauche a droite. Il faut pourvoir le faire plus d'une fois par timer, donc on l'appelle a chaque fois qu'une touche est enfoncee. c'est a dire dans la fonction Keypressed ! ( LE PERMIER MOVE(SELF) )
    ##j'en ai marre et il fait chaud !!!!!!!!
    ## mais sinon ca va :)
    def backAndForth(self):
        global direct
        flag = self.checkBoundries()
        if flag == 1:
            for item in self.totalList[self.index]:
                for thing in item:
                    thing.x += direct
            self.x += direct ##il va falloir ajouter une condition pour qu'on ne puisse pas sortir de la zone de jeu...
        self.list = self.totalList[self.index][self.config]
        direct = 0

    def draw(self):
        #alors ici il faut que tu prenne le self.list rafraichit (c'est a dire apres avor appele la methode getSquareList, et que tu fasse une boucle pour appeler la methode draw de chaque element (les instances de la classe carre ) de ta liste.
        #donc vu qu'il me le faut pour faire des tests je te fais cette boucle, que tu n'aurais eu aucun mal a faire quoi qu'il arrive
        ##comme je l'ai dit ca ca sert plus a rien : self.getSquareList()
        for thing in self.list :
            thing.draw() #on appelle ici la methode draw de l'objet carre, et on s'en fout si on a 2 draw, parce que ils sont dans 2 classes differentes (la classe carre et la classe piece...)

##LA FIN DE LA ClASSE C'EST ICI !


def move():
    threading.Timer(.8, move).start()
    global dead
    if dead != 1:
        pieceR.down()


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
    ##ici en fait y'avait pas besoin de variables globales...
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
    glLoadIdentity()	# Reset The View
    glTranslatef(-5.,-10.0,-25.0)	# Move Into The Screen

    #DESSIN

    pieceR.draw()
    sol.draw()

    
    glutSwapBuffers()


def keyPressed(key, x, y):
    global direct
    # Si t ou echap presse, tout effacer
    if key == ESCAPE or key == 't':
        sys.exit()

    if key == 'm':
        direct = 1
    if key == 'k':
        direct = -1
    if key=='a':
        pieceR.down()
    if key == 'o':
        pieceR.changeConfig(1)
    if key == 'l':
        pieceR.changeConfig(-1)

##    move()
##c'etait pas move(timer) qu'il fallait appeler, mais ce qui est maintenat backAndForth, une methode, donc il faut l'instance . backandforth...
    pieceR.backAndForth()


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
    glutFullScreen()
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    move()
    glutMainLoop()


sol = floor()
pieceR = piece()


#main()
