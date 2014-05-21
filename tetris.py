from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys,threading,random

ESCAPE = '\033'

direct = 0
score = 0
dead = 1

# Number of the glut window
window = 0


class carre(object):                 #objet representant un carre

    def __init__(self,x,y,couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
    def getVertices(self):
        self.vertices = [[self.x,self.y,0],[self.x,self.y+0.95, 0],[self.x+0.95, self.y+0.95, 0],[self.x+0.95,self.y, 0]]

    def draw(self):
        self.getVertices()
        glBegin(GL_QUADS)
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2]) # Permet de changer la couleur facilement pour faire des tests
        for vertex in self.vertices:
            glVertex3f(vertex[0],vertex[1],vertex[2])
        glEnd()


class floor(object):                       # objet representant le sol
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
            item.draw()


class piece(object):                 #objets representant chaque pieces
    def __init__(self):
        self.x = 4
        self.y = 20
        self.index = random.randint(0,6)
        self.config = 0
        colorList =[[1,0.2,0.4], [0,1,1], [1,0,1], [1,1,0], [0,0,1], [1,0,0], [0,1,0]]      #Liste de couleur (dans le meme ordre que les pieces)
        self.color = colorList[self.index]
        #Liste de toutes les pieces, on peut faire un random choice dedans, puisque les methodes ci dessous sont les memes pour toutes les pieces
        #Chaque liste dans la liste est une configuration de la piece, pour pouvoir la tourner facilement
        self.totalList = [[[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x+1,self.y-2,self.color)], [carre(self.x-1,self.y-1,self.color), carre(self.x,self.y-1,self.color), carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y,self.color)], [carre(self.x,self.y-2,self.color), carre(self.x,self.y-1,self.color), carre(self.x,self.y,self.color),carre(self.x-1,self.y,self.color)], [carre(self.x-1,self.y-1,self.color), carre(self.x,self.y-1,self.color), carre(self.x+1,self.y-1,self.color),carre(self.x-1,self.y-2,self.color)]],
                
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x-1,self.y-2,self.color)],[carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color)],[carre(self.x,self.y-2,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y,self.color),carre(self.x+1,self.y,self.color)],[carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x-1,self.y,self.color)]],
                          
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y-2,self.color)],[carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y,self.color)], [carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-2,self.color)], [carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x,self.y-2,self.color)]],
                          
                          
                    [[carre(self.x,self.y,self.color),carre(self.x+1,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]],
                          
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x,self.y-2,self.color),carre(self.x,self.y-3,self.color)],[carre(self.x-2,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]],
                          
                          
                [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color),carre(self.x-1,self.y-2,self.color)],[carre(self.x-1,self.y,self.color),carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color)]],
                          
                          
                    [[carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x+1,self.y-1,self.color),carre(self.x+1,self.y-2,self.color)],[carre(self.x+1,self.y,self.color),carre(self.x,self.y,self.color),carre(self.x,self.y-1,self.color),carre(self.x-1,self.y-1,self.color)]]]
        self.list = self.totalList[self.index][self.config]

    def checkOnFloor(self):               # Cette methode sert a verifier si la piece est en contact avec le sol
        flag =0
        for thing in self.list:
            for item in sol.top:
                if item.x == thing.x and item.y+1 == thing.y:     ##juste si tu peux me renseigner sur ca represente quoi exactement dead
                    flag = 1
                if flag == 1 and thing.y>=18:
                    flag = 2
        if flag ==1: 
            for item in self.list:
                sol.top.append(item) 
            sol.checkLine()
            self.__init__()
        if flag == 2:
            global dead
            dead = 1
            print(dead)

    def checkBoundries(self):
        global direct
        for thing in self.list:            #Cette boucle sert a verifier s'il on est sur les cotes
            if thing.x+direct ==-1 or thing.x+direct == 12 :
                return 0

        for thing in self.list:      #Cette boucle verifie si la piece arrive sur une zone deja occupee par une autre piece
            for item in sol.top:
                if thing.y == item.y and thing.x+direct == item.x:
                    return 0
        return 1 

    def down(self):             #Sert a faire descendre la piece manuellement
        self.checkOnFloor()
        self.y -=1
        for item in self.totalList[self.index]:
            for thing in item:
                thing.y-= 1
        self.list = self.totalList[self.index][self.config]

    def changeConfig(self, spin):          #Sert a changer la configuration de la piece, ( la faire tourner)
        oldConfig = self.config
        self.config = self.config+spin
        if self.config == len(self.totalList[self.index]):
            self.config =0
        if self.config == -1:
            self.config = len(self.totalList[self.index])-1

        self.list = self.totalList[self.index][self.config]
        
        if self.checkBoundries() == 0:
            self.list = self.totalList[self.index][oldConfig]


    def backAndForth(self):                 #Sert a deplacer la piece sur la gauche ou sur la droite
        global direct
        flag = self.checkBoundries()
        if flag == 1:
            for item in self.totalList[self.index]:
                for thing in item:
                    thing.x += direct
            self.x += direct 
        self.list = self.totalList[self.index][self.config]
        direct = 0

    def draw(self):
        for thing in self.list :
            thing.draw() #Ici on appelle la methode draw de l'objet carre



def move():                    #Sert a faire descendre la piece toutes les 0.8 secondes toute seule
    threading.Timer(.8, move).start()

    global dead
    if dead != 1:
        pieceR.down()
    


# A general OpenGL initialization function. Sets all of the initial parameters.
def InitGL(Width, Height): # We call this right after our OpenGL window is created.

    glClearColor(0.0, 0.0, 0.0, 0.0) # This Will Clear The Background Color To Black
    glClearDepth(1.0) # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS) # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST) # Enables Depth Testing
    glShadeModel(GL_SMOOTH) # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() # Reset The Projection Matrix
                                                # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0: # Prevent A Divide By Zero If The Window Is Too Small
          Height = 1
    
    glViewport(0, 0, Width, Height)	# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Fonction de dessin principale

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
    glLoadIdentity()	# Reset The View
    glTranslatef(-5.,-10.0,-25.0)	# Move Into The Screen
    global dead
    if dead == 4:
        for item in lost:
            item.draw()

    #DESSIN (sol et piece)

    pieceR.draw()
    sol.draw()
       
    glutSwapBuffers()


def keyPressed(key, x, y):
    global direct
    # Si t ou echap presse, tout effacer
    if key == ESCAPE or key == 't':
        sys.exit()

    if key == 'd':          #touche pour deplacer la piece a droite
        direct = 1
    if key == 'q':          #touche pour deplacer la piece a gauche
        direct = -1
    if key=='s':            #touche pour descendre la piece, avec appel de la fonction down
        pieceR.down()
    if key == 'k':                   #touche pour tourner la piece a droite
        pieceR.changeConfig(1)
    if key == 'l':                   #touche pour tourner la piece a gauche
        pieceR.changeConfig(-1)

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


sol = floor()                            ##et a quoi ca sert cette partie
pieceR = piece()

move()
#main()

