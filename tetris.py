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
    #ca c'est pour recuperer ta fameuse liste que tu avais au depart. Sauf que la en plus tu peux mettre les autres listes pour la rotation et faire un truc qui choisit la bonne :) ( LISTE TOUT EN HAUT ? OU DU COUP JPEUX METTRE MES OBJETS PIECES ? )
    ##Alors en fait, self.list, c'est la vraie liste de tes carres. Tu pourra meme y ajouter les listes de tes differentes configurartions, et comme ca en fait, tu fais la representation de ta piece dans ton code... c'est ca qui est dessine dans la methode draw(). Et non, tu ne peux pas mettre tes objets pieces, parce que jusqua ce que je dirai stop, c'est dans la classe piece, donc ca c'est la liste de cette piece en particulier...
    ##je crois que ca c'est toujours pas tres clair, alors si t'a des questions dessus n'hesite pas :)
    ##mais du coup la ca marche et donc je sais pas si ca te va ou pas...

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

##de la...

##en fait, cette fonction elle est un peu pourrie, et a cause d'elle tu as besoin de 50000 classes de pieces differentes. Alors je l'ai remplacee par un choix random dans la classe piece unique que j'ai refaite a partir des autres classes que toi tu avait. c'est en gros une refonte, un espece de deux en 1 quoi, donc c'est moins cher et c'est plus pratique !
def randomPiece():
    test = 0 #meme principe : faut que tu te fasse ta fonction ! alors soit tu fait comme t'avais fait, tu fais une liste d'instances de classes pieces (une de chaque) et tu fait ton choice
    #tu peux donc par exemple faire ta liste comme ceci
    piecerandom = [piece6(), piece()] #avec piece1 et tout ca etant des classes et entre les () tu mets ce qu'il faut quoi !
    return( random.choice(piecerandom) )    #du coup cette ligne tu peux peut etre la garder :)

def bas():
    test = 0 #si tu continue a lire mes commentaires ti verras ce que c'est que cette fonction :)
    # du coup pour comprendre cette fonction va voir le commentaire dans le timer et apres reviens ici.
    #c'est donc ici qu'il faut placer tes if : pour savoir si t'est en bas, et si c'est le cas tu as deux choses a faire : ajouter la piece qui viens d'atterrir a ce qui represente la ligne du bas, puis appeler ta fonction randomPiece() pour refaire une piece qui recomence a descendre.
    #c'est peut etre aussi dans cette fonction qu'il faudrait regarder si tu as fait une ligne et si oui te rajouter des points dans une variable globale :)

##a de la, ca sert a rien...

def move():
    threading.Timer(.8, move).start()     # (ET LA LE DEUXIEME MOVE ).8
    #global x
    #global y
    #global direct
    #du coup tu n'as plus besoin que de ta variable globale qui est l'objet qui est en train de descendre !
    #global pieceR  #mais tu n'auras pas besoin de cette ligne, car c'est un objet...     (DONC LA JE COMPREND PAS DU COUP, JE SAIS PLUS QUOI GARDER)
    
    ##ce que je voulais dire, c'est qu'en fait pieceR ne va plus etre une variabl globale : ce sera maintenat une instance d'un des objets piece.
    ## et vu que tu va jouer avec les x et y de cette instance, tu n'a plus besoin de tes 15000 variables globales qui sont en commmentaire audessus !
    ##voila donc a quoi ca va ressembler :
    
    #if pieceR.y>3 :
        #j'ai enleve le truc du x, il est deja apelle dans le keyboardfunc...
        #mais ici on fait descendre la piece
        
        ##et on la fait descendre que si on est encore vivant :)
    global dead
    if dead != 1:
        pieceR.down()
    ##tout simplement :) Mainetant tout le travail est fait a l'interieur de ta classe piece quelle qu'ell soit !

        ## ca ca ne sert a rien, il faut tout faire dans notre sol !
        # if pieceR.y<=3 : #ca ca veut dire que ta piece est arrivee en bas...
        #alors il va faloir gerer une representation dynamique de ce qu'est le bas. C'est a dire que une fois qu'on a commence a jouer le bas n'est plus juste une ligne...
        #donc moi je te propose de faire une nouvelle fonction par exemple bas(), que j'ai declaree plus haut, et qui va regarder si le pieceR.bas est sur la ligne du bas et si c'est le cas va faire en sorte d'incorporer cette piece qui vient d'atterir dans ce que tu choisira pour representer le bas, soit un objet, soit une liste ou ce que tu veux, mais choisit bien parce que ca va deja etre assez galere comme ca .... :( Du coup les ifs de cette fonction ne servent plus a grand chose, il faudra juste appeler ta nouvelle fonction bas avant de descendre ta piece..
#pieceR.__init__()##ca c'est parce au final, si la piece arrive en bas il faut en refaire une nouvelle !




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
    global dead
    if dead == 4:
        for item in lost:
            item.draw()
    #DESSIN

    pieceR.draw()
    sol.draw()
        #for item in grille :
        # for trucs in item :
        #       trucs.draw()

    
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



#FABRICATION
#Grille de jeu

# est ce qu'elle sert vraiment a qqch ta grille ? parce qu'en fait t'es parti avec des pieces independantes et pas des etats de pixels (les carres de la gille...) mais c'est pas grave du tout c'est ta facon de faire et ca marche tout aussi bien :)
# cela dit laisse la ou elle est pour l'instant... elle ne gene personne !
##bon ba au final non la grille elle sert a rien...
moncarre=carre(0,0,[1.0,1.0,1.0])
machin=[]
grille=[]

for colonne in range(20):
    for ligne in range(12):
        machin.append(carre(ligne,colonne,[1.0,1.0,1.0]))
    grille.append(machin)

##il faut donc ici, car c'est ici qu'on fabrique tout visiblement, fabriquer pieceR :

#alors maintenant avant d'appeler tes fonctions (move() et main()), il faut creer une premiere piece qui descend et qui est choisie aleatoirement :
sol = floor()
pieceR = piece()

##moi j'ai trouve ca rigolo... mais ca marche pas... pour l'instant ! C'etatit pour ecrire "lost" avec les pices... Et mon high score de l'avion c'est 105 non en fait 147 et mort par suicide... faut vraiment que ca accelere !(une demie heure de jeu avec deux carres sur le sol, ca me parrait un peu facile...)lignes... Ce qui serait cool, c'est qu'il accelkere non ? demande a pincon, lui son truc il accelere !
lost = [piece(), piece(), piece(), piece()]
lost[0].index = 0
lost[0].x = 0
lost[0].y = 7

lost[1].index = 4
lost[1].x = 3
lost[1].y = 7

lost[2].index = 6
lost[2].x = 6
lost[2].y = 7

lost[3].index = 3
lost[3].x = 9
lost[3].y = 7
for item in lost:
    item.list = item.totalList[item.index][0]
    item.list[0].x = item.x
    item.list[0].y = item.y


main()
