import LCD
from machine import pin
from time import ticks_us
from random import randint

#colors
grey = LCD.RGB(64, 64, 64)
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0,)
red = LCD.RGB(255, 0, 0)

#pins
startPin = pin(15, Pin.IN, Pin.PULL_UP)
jumpPin = pin(14, Pin.IN, Pin.PULL_UP)

jumpFlag = 0
#interrupts
def jump(jumpPin)
	global jumpFlag
	jumpFlag = 1
	
def start(startPin)
	global startFlag
	startFlag = 0

#Random number generator
def new_rope()
	length = randint(500_000, 1_500_000)
	return length
	
def start_screen()
	LCD.Text(Press button 14 to begin, 200, 25, white, 3)
	LCD.Text("Tries: " + str(tries), 200, 100, white, 3)
	startFlag = True

loseFlag = 0
while loseFlag is not true:
	if startFlag is not true:
		start_screen()
	new_rope()
	
	
