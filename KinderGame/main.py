import pygame
import math
import socket
import os
import random

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
	import android
except ImportError:
	android = None
	
def FileArray(fname):
	File = open(fname,"r")
	FileContent = File.read()
	File.close()
	FileContent = FileContent.splitlines()
	fl = []
	for l in FileContent:
		fl.append(l.split(" "))
	return fl
	
def LoginInfo():
	os.system("java -cp :assets/postgresql-9.2-1003.jdbc4.jar login ")
	users = FileArray("login.txt")
	return users
			
def PushAnswer(answer):
	s = " "
	os.system("java -cp :assets/postgresql-9.2-1003.jdbc4.jar push "+answer[0]+s+answer[1]+s+answer[2])
		
def PullTest():
	os.system("java -cp :assets/postgresql-9.2-1003.jdbc4.jar pull ")
	testinfo = FileArray("pull.txt")
	return testinfo
		
def Authenticate(user,password,info):
	for i in info:
		if i[0] == user and i[1] == password:
			print "login success"
			return True
	return False
		

#screen width and screen height
SW = 800
SH = 400

#input array
keyUp = 0
keyDown = 1
keyLeft = 2
keyRight = 3
keySpace = 4
keyEnter = 5
keyE = 6
MX = 0
MY = 1
MLC = 2
MRC = 3

Keys = [ False, False, False, False, False, False, False ]
Mouse = [ 0, 0, False, False ]

#game states
StateTitleScreen = 0
StateLoginScreen = 1
StateChooseKid = 2
StateGamePlay = 3
GameState = StateTitleScreen

# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 10

# Color constants.
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PINK = (255,0,255)
PURPLE = (128,0,255)

#initialize pygame
pygame.init()

#set the window title text
pygame.display.set_caption("Kinder Game")

# Set the screen size.
screen = pygame.display.set_mode((SW, SH)) # pygame.NOFRAME)

#pygame.mouse.set_visible(0) 

# Map the back button to the escape key.
if android:
	android.init()
	android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
	android.map_key(android.KEYCODE_A, pygame.K_a)
	android.map_key(android.KEYCODE_B, pygame.K_b)
	android.map_key(android.KEYCODE_C, pygame.K_c)
	android.map_key(android.KEYCODE_D, pygame.K_d)
	android.map_key(android.KEYCODE_E, pygame.K_e)
	android.map_key(android.KEYCODE_F, pygame.K_f)
	android.map_key(android.KEYCODE_G, pygame.K_g)
	android.map_key(android.KEYCODE_H, pygame.K_h)
	android.map_key(android.KEYCODE_I, pygame.K_i)
	android.map_key(android.KEYCODE_J, pygame.K_j)
	android.map_key(android.KEYCODE_K, pygame.K_k)
	android.map_key(android.KEYCODE_L, pygame.K_l)
	android.map_key(android.KEYCODE_M, pygame.K_m)
	android.map_key(android.KEYCODE_N, pygame.K_n)
	android.map_key(android.KEYCODE_O, pygame.K_o)
	android.map_key(android.KEYCODE_P, pygame.K_p)
	android.map_key(android.KEYCODE_Q, pygame.K_q)
	android.map_key(android.KEYCODE_R, pygame.K_r)
	android.map_key(android.KEYCODE_S, pygame.K_s)
	android.map_key(android.KEYCODE_T, pygame.K_t)
	android.map_key(android.KEYCODE_U, pygame.K_u)
	android.map_key(android.KEYCODE_V, pygame.K_v)
	android.map_key(android.KEYCODE_W, pygame.K_w)
	android.map_key(android.KEYCODE_X, pygame.K_x)
	android.map_key(android.KEYCODE_Y, pygame.K_y)
	android.map_key(android.KEYCODE_Z, pygame.K_z)

# Use a timer to control FPS.
pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

#point in rectangle intersection functions
def PointRectIntersection(px,py,rx,ry,rw,rh):
		return (px>rx and px<rx+rw and py>ry and py<ry+rh)
		
def PointRectIntersection2(px,py,r):
		return (px>r[0] and px<r[0]+r[2] and py>r[1] and py<r[1]+r[3])
		
		

#start class Button ===================================================#
class Button:
	def __init__(self,fname,pos):
		self.image = pygame.image.load(fname)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.clicked = False
		
	def HandleInput(self,event):
		if Mouse[MLC] == True or Mouse[MRC] == True:
			if PointRectIntersection2(Mouse[MX],Mouse[MY],self.rect):
				self.clicked = True
				if android:
					android.vibrate(0.04);
				Mouse[MLC] = Mouse[MRC] = False
		else:
			self.clicked = False
		
	def IsClicked(self):
		return self.clicked
		
	def SetImage(self,image):
		self.image = image

	def Draw(self,DisplaySurface):
		DisplaySurface.blit(self.image,self.rect)
#end class Button =====================================================#

#start class Font =====================================================#
class Font:
	def __init__(self,fname,size,color):
		self.font = pygame.font.Font(fname,size)
		self.fname = fname
		self.size = size
		self.color = color
		
	def Set(self,fname,size,color):
		self.font = pygame.font.Font(fname,size)
		self.fname = fname
		self.size = size
		self.color = color
	
	def SetFont(self,fname):
		self.fname = fname
		self.font = pygame.font.Font(fname,self.size)
		
	def SetSize(self,size):
		self.fname = fname
		self.font = pygame.font.Font(self.fname,size)
		
	def SetColor(self,color):
		self.color = color
		
	def Draw(self,DisplaySurface, text, x, y):
		surf = self.font.render(text, True, self.color)
		rects = surf.get_rect()
		rects.center = (SW/2,SH/2)
		DisplaySurface.blit(surf,(x,y))
		
	def Draw2(self,DisplaySurface, text, x, y, color):
		surf = self.font.render(text, True, color)
		surf.set_alpha(None)
		surf.set_alpha(100)
		t,t2,w,h = surf.get_rect()
		DisplaySurface.blit(surf,(x,y))
		
	def Draw3(self,DisplaySurface, text, x, y, color):
		semiTransparent = self.font.render(text, True, color)
		newSurf = pygame.Surface(self.font.size(text))
		newSurf.blit(semiTransparent,(0,0))
		newSurf.set_alpha(color[3])
		DisplaySurface.blit(newSurf, (x,y))
		
#end class Font =======================================================#	

#start class TextBox ==================================================#
class TextBox:
	def __init__(self,fname,rect):
		self.clicked = False
		self.edit = False
		self.caps = False
		self.string = ""
		self.font = Font(fname,50,BLACK)
		self.rect = rect
		self.ast = ""
		self.hidden = False
	
	def SetHidden(self,val):
		self.hidden = val
		
	def HandleInput(self,event):
		if self.edit == True: 
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.caps = not self.caps
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				self.edit = False
				self.clicked = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
				self.string = self.string[:-1]
				self.ast = self.ast[:-1]
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				if self.caps == True:
					self.string = self.string + "A"
				else:
					self.string = self.string + "a"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
				if self.caps == True:
					self.string = self.string + "B"
				else:
					self.string = self.string + "b"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				if self.caps == True:
					self.string = self.string + "C"
				else:
					self.string = self.string + "c"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
				if self.caps == True:
					self.string = self.string + "D"
				else:
					self.string = self.string + "d"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
				if self.caps == True:
					self.string = self.string + "E"
				else:
					self.string = self.string + "e"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
				if self.caps == True:
					self.string = self.string + "F"
				else:
					self.string = self.string + "f"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
				if self.caps == True:
					self.string = self.string + "G"
				else:
					self.string = self.string + "g"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
				if self.caps == True:
					self.string = self.string + "H"
				else:
					self.string = self.string + "h"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
				if self.caps == True:
					self.string = self.string + "I"
				else:
					self.string = self.string + "i"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
				if self.caps == True:
					self.string = self.string + "J"
				else:
					self.string = self.string + "j"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
				if self.caps == True:
					self.string = self.string + "K"
				else:
					self.string = self.string + "k"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
				if self.caps == True:
					self.string = self.string + "L"
				else:
					self.string = self.string + "l"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
				if self.caps == True:
					self.string = self.string + "M"
				else:
					self.string = self.string + "m"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				if self.caps == True:
					self.string = self.string + "N"
				else:
					self.string = self.string + "n"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
				if self.caps == True:
					self.string = self.string + "O"
				else:
					self.string = self.string + "o"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				if self.caps == True:
					self.string = self.string + "P"
				else:
					self.string = self.string + "p"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				if self.caps == True:
					self.string = self.string + "Q"
				else:
					self.string = self.string + "q"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				if self.caps == True:
					self.string = self.string + "R"
				else:
					self.string = self.string + "r"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
				if self.caps == True:
					self.string = self.string + "S"
				else:
					self.string = self.string + "s"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				if self.caps == True:
					self.string = self.string + "T"
				else:
					self.string = self.string + "t"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
				if self.caps == True:
					self.string = self.string + "U"
				else:
					self.string = self.string + "u"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
				if self.caps == True:
					self.string = self.string + "V"
				else:
					self.string = self.string + "v"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
				if self.caps == True:
					self.string = self.string + "W"
				else:
					self.string = self.string + "w"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
				if self.caps == True:
					self.string = self.string + "X"
				else:
					self.string = self.string + "x"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:
				if self.caps == True:
					self.string = self.string + "Y"
				else:
					self.string = self.string + "y"
				self.ast = self.ast + "*"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
				if self.caps == True:
					self.string = self.string + "Z"
				else:
					self.string = self.string + "z"
				self.ast = self.ast + "*"

		self.clicked = False
		if Mouse[MLC] == True or Mouse[MRC] == True:
			if PointRectIntersection2(Mouse[MX],Mouse[MY],self.rect) == True:
				self.clicked = self.edit = True
				if android:
					android.vibrate(0.04);
			else:
				self.edit = self.clicked = False
		
	def IsClicked(self):
		return self.clicked
		
	def IsEditing(self):
		return self.edit
		
	def TextChanged(self):
		return self.modified
		
	def SetImage(self,font):
		self.font = font

	def Draw(self,DisplaySurface):
		#DisplaySurface.blit(self.image,self.rect)
		pygame.draw.rect(DisplaySurface, WHITE, self.rect)
		if self.edit == True:
				pygame.draw.rect(DisplaySurface, (210,210,255), self.rect)
		if self.hidden == False:
			self.font.Draw(DisplaySurface, self.string, self.rect[0], self.rect[1])
		else:
			self.font.Draw(DisplaySurface, self.ast, self.rect[0], self.rect[1])
#end class TextBox ====================================================#

#start class TitleScreen ==============================================#
class TitleScreen:
	def __init__(self):
		self.image = pygame.image.load("assets/titleScreen.png").convert()
		self.start = pygame.image.load("assets/start.png")
		self.button = Button("assets/start.png",(SW/2 + 125, SH*0.75))
		self.val = 0
		
	def HandleInput(self,event):
		self.button.HandleInput(event)
	
	def Update(self):
		self.val = (self.val + 1) % 37
		if self.button.IsClicked():
			global GameState
			global StateLoginScreen
			GameState = StateLoginScreen
			
	def Draw(self, DisplaySurface):
		DisplaySurface.blit(self.image,(0,0))
		if self.val > 5:
			self.button.Draw(DisplaySurface)
#end cass TitleScreen =================================================#

#start class LoginScreen ==============================================#
class LoginScreen:
	def __init__(self):
		self.username = TextBox("assets/font0.ttf",(100,15,600,40))
		self.password = TextBox("assets/font0.ttf",(100,75,600,40))
		self.password.SetHidden(True)
		self.button = Button("assets/start.png",(SW/2, 150))
		self.info = LoginInfo()
		
	def HandleInput(self,event):
		self.username.HandleInput(event)
		self.password.HandleInput(event)
		self.button.HandleInput(event)
		
	def Update(self):
		if self.button.IsClicked():
			if Authenticate(self.username.string,self.password.string,self.info) == True:
				global GameState
				global StateGamePlay
				GameState = StateGamePlay
			
	def Draw(self, DisplaySurface):
		DisplaySurface.fill((75,75,255))
		self.username.Draw(DisplaySurface)
		self.password.Draw(DisplaySurface)
		self.button.Draw(DisplaySurface)
#end cass LoginScreen =================================================#

#start class GamePlay =================================================#
class GamePlay:
	def __init__(self):
		self.images = [] #load game images here
		self.background = pygame.image.load("assets/gamebg.png")
		self.buttons = []
		self.test = PullTest()
		for i in range(0,5):
			self.buttons.append(Button("assets/vocal%s.png" % str(i),((i+1)*120+30,325)))
			self.images.append(pygame.image.load("assets/image%s.png" % str(i)))
		self.questionIndex = 0
		
			
	def HandleInput(self,event):
		for b in self.buttons:
			b.HandleInput(event)
			if b.IsClicked() == True:
				#if android: android.show_keyboard()
				#self.currentImage = self.buttons.index(b)
				
				self.questionIndex = self.questionIndex + 1
				
	def Update(self):
		if self.questionIndex > 4:
			self.done == True
		
	def Draw(self, DisplaySurface):
		DisplaySurface.blit(self.background, (0,0))
		DisplaySurface.blit(self.images[self.currentImage], (275,90))
		for b in self.buttons:
			b.Draw(DisplaySurface)
		
#end cass GamePlay ====================================================#

#declare game components
screens = [ TitleScreen(), LoginScreen(), "choose kid", GamePlay()]

#start main game loop =================================================#
while True:
	ev = pygame.event.wait()

	# Android-specific:
	if android:
		if android.check_pause():
			android.wait_for_resume()
	
	# Draw the screen based on the timer ==============================#
	if ev.type == TIMEREVENT:
		screen.fill(BLACK)
		screens[GameState].Draw(screen)
		pygame.display.flip()
	# end Drawing stuff ===============================================#

	#start Recieving input ============================================#
	elif ev.type == pygame.QUIT:
		break
	elif ev.type == pygame.KEYDOWN:
		if ev.key == pygame.K_ESCAPE:
			break
	elif ev.type == pygame.MOUSEMOTION:
		Mouse[MX], Mouse[MY] = ev.pos
	elif ev.type == pygame.MOUSEBUTTONUP:
		Mouse[MLC] = Mouse[MRC] = False
	elif ev.type == pygame.MOUSEBUTTONDOWN:
		Mouse[MLC] = Mouse[MRC] = True
		Mouse[MX], Mouse[MY] = ev.pos
	#end Recieving input ==============================================#
			
	#start Handling input and updating stuff ==========================#
	screens[GameState].HandleInput(ev)
	screens[GameState].Update()
	#end Handling input and updating stuff ============================#

#end main game loop ===================================================#
