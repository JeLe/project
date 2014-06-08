from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from random import *



class player (object):
    def __init__ (self, Ax, Ay, couleur):
        self.red = couleur[0]
        self.green = couleur[1]
        self.blue = couleur[2]
        self.Ax = Ax
        self.Ay = Ay
    
    def getvertices(self):
        global updown
        self.Ay += updown*0.03
        
        if -2.06<=self.Ay<=-2.:
            self.Ay = -2
        
        if 1.7<=self.Ay<=1.76:
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

class line_runner(object):
    def __init__(self):
        self.score=0
        self.upscore=5
        self.value=10
        self.increment=0.2
        self.pausedIncrement =0
        self.updown = 0
