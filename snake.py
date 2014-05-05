
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
c=0
l=0
i=0
j=0
time=0
momentum=0
taille = 3
dir = 'm'
fi=10
fj=-5



class carre(object):
	def __init__(self,x,y,couleur):
		self.red=couleur[0]
		self.green=couleur[1]
		self.blue=couleur[2]
		self.vertices = [[x,y,0],[x,y+1, 0],[x+1, y+1, 0],[x+1,y, 0]]
	def drawSquare(self):
		glBegin(GL_QUADS)
		glColor3f(self.red, self.green, self.blue)
		for vertex in self.vertices:
			glVertex3f(vertex[0],vertex[1],vertex[2])
		glEnd()


def move():

	threading.Timer(0.5, move).start()
	global i,j,dir,snakeColor,time,grid,taille,foodcoord,momentum,fi,fj
	u=0

	time+=1   #Sert pour ne pas tricher !
			
	if dir == 'm' :
		i+=1			
	if dir == 'k' :
		i-=1
	if dir == 'o' :
		j+=1
	if dir == 'l':
		j-=1

	coord.append([i,j])

	if foodcoord  in coord and momentum!=time :
		while u<=len(snake) : 
			u+=1
			if u>len(snake) :
				snake.insert(0,carre(fi,fj,snakeColor))
				momentum = time
		

	if len(snake)>=taille :
		snake.pop(0)
		coord.pop(0)
	
	coord2 = []
	for item  in coord :
		if item in coord2 :
			snakeColor = [0.2,0.2,0.1]
		else:
			coord2.append(item)
		
	
	snake.append(carre(i,j,snakeColor))


	
	if i in range(0,16) or j in range(0,8) :
		snakeColor=[0.8,0.1,0.1] #rouge
	if i>15 or i<0 or j>0 or j<(-7):
		snakeColor=[0.,0.8,0.1] #vert

def miam() :
	
	global food,foodcoord,fi,fj

	food = carre(fi,fj,[1.,1.,0.])
	foodcoord=[fi,fj]


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
	global window,dir,time,momentum,i,j


	if key == ESCAPE or key == 'q':
		destroy
	if key == 'r' :
		i = 0
		j = 0
	
	if  key == 'm' and dir != 'k' and momentum!=time :
	
		dir = 'm'
		momentum=time

	if  key == 'k' and dir != 'm' and momentum!=time :
		
		dir = 'k'
		momentum=time

	if  key == 'l' and dir != 'o' and momentum!=time :
		
		dir = 'l'
		momentum=time

	
	if  key == 'o' and dir != 'l' and momentum!=time :
		
		dir = 'o'
		momentum=time
			
def main():
	global window
	
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

miam()	
move()
main()	
