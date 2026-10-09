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
jump = pin(14, Pin.IN, Pin.PULL_UP)

#interrupts
def IntServe(jump)

#Random number generator
def new_rope()
	length = randint(500_000, 1_500_000)
	return length

def start_screen()
	LCD.Text(Press button 14 to begin, 200, 100, white, 3)
	LCD.Text("Tries: " + str(tries), 200, 100, white, 3)

loseFlag = 0
startFlag = 0
while loseFlag is not true:
	if startFlag is not true:
		
