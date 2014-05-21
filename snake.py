
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import threading, random, sys

# python snake.py
# Some api in the chain translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'
window = 0
grid=[]
snake=[]
coord=[]
snakeColor=[0.8,0.1,0.1]

i=0
j=0
temps=0
momentum=0
taille = 3
direction = 'm'
speed=2.5

class carre(object):
	def __init__(self,x,y,couleur):
		self.red=couleur[0]
		self.green=couleur[1]
		self.blue=couleur[2]
		self.vertices = [[x,y,0],[x,y+0.99, 0],[x+0.99, y+0.99, 0],[x+0.99,y, 0]]
	def drawSquare(self):
		glBegin(GL_QUADS)
		glColor3f(self.red, self.green, self.blue)
		for vertex in self.vertices:
			glVertex3f(vertex[0],vertex[1],vertex[2])
		glEnd()


def miam() :
	
	global foodcoord
	i=random.randint(0,15)
	j=-random.randint(0,7)
	foodcoord=[i,j]
	return(carre(i,j,[1.,1.,0.]))


food=miam()

def move():


	global i,j,direction,snakeColor,temps,grid,taille,foodcoord,momentum,food,speed
        threading.Timer(1/speed, move).start()
	temps+=1   #Sert pour ne pas tricher !
			
	if direction == 'm' :
		i+=1			
	if direction == 'k' :
		i-=1
	if direction == 'o' :
		j+=1
	if direction == 'l':
		j-=1

	coord.append([i,j])
        
	if foodcoord==coord[len(snake)] :
		taille+=1
		if speed<4 :
			speed+=0.5
		if speed >=4 and speed<10 :
			speed+=0.3
		else :
			speed+=0.07
		food=miam()
                for item in coord :
                        if item == foodcoord :
                                food=miam()


	if len(snake)>=taille :
		snake.pop(0)
		coord.pop(0)
	
	coord2 = []
	for item  in coord :
		if item in coord2 :
			reset()
		else:
			coord2.append(item)
	
	snake.append(carre(i,j,snakeColor))

	if i>15 or i<0 or j>0 or j<(-7):
                reset()


def reset() :
	global direction,i,j,taille,speed,momentum,temps

	snake[:]=[]
	coord[:]=[]
        momentum=temps
	taille=3
	speed=2.50
	if direction=='k' :
		direction = 'l'
		i=0
		j=1
	else :
		direction ='m'
		i=-1
		j=0

def InitGL(Width, Height):				
	glClearColor(0.0, 0.0, 0.0, 0.0)	
	glClearDepth(1.0)					
	glDepthFunc(GL_LESS)				
	glEnable(GL_DEPTH_TEST)				
     	glShadeModel(GL_SMOOTH)				
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()				
										
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)



def ReSizeGLScene(Width, Height):
	if Height == 0:						
		Height = 1

	glViewport(0, 0, Width, Height)	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)



def DrawGLScene():                        #La fonction dessin 
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(-8., 3.069, -10.) 
        global food
	
	
	for item in snake :
		item.drawSquare()

	food.drawSquare()

	for item in grid :
		item.drawSquare()

			     
	glutSwapBuffers()
	

  


def keyPressed(key, x, y):
	global window,direction,temps,momentum,i,j


	if key == ESCAPE or key == 'q':
		sys.exit()
	if key == 'r' :
		reset()
	
	if  key == 'm' and direction != 'k' and momentum!=temps :
		
		direction = 'm'
		momentum=temps

	if  key == 'k' and direction != 'm' and momentum!=temps :
		
		direction = 'k'
		momentum=temps

	if  key == 'l' and direction != 'o' and momentum!=temps :
		
		direction = 'l'
		momentum=temps

	
	if  key == 'o' and direction != 'l' and momentum!=temps :
		
		direction = 'o'
		momentum=temps
			
def main():
	global window
	
	move()

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	glutInitWindowSize(1600,900)   #HAUTEUR = 839
	 
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Snake")
 
	InitGL(1600,900)
   
	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(DrawGLScene)
	glutReshapeFunc(ReSizeGLScene)
	glutKeyboardFunc(keyPressed)
	glutMainLoop()


for l in range(0,8) :
	for c in range(0,16) :
		grid.append(carre(c,0-l,[0.1,0.15,0.53]))  #random.random()



#main() # ca c'est en comment uniquement pour pouvoir le mettre dans le projet complet !

