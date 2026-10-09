import LCD
from machine import Pin
from time import ticks_ms, sleep_ms
from random import randint

#colors
grey = LCD.RGB(64, 64, 64)
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0,)
red = LCD.RGB(255, 0, 0)
blue = LCD.RGB(0, 0, 255)

#pins
startPin = Pin(14, Pin.IN, Pin.PULL_UP)
jumpPin = Pin(15, Pin.IN, Pin.PULL_UP)

#interrupts
def jump(jumpPin):
	global jumpFlag
	jumpFlag = 1
	
def start(startPin):
	global startFlag
	startFlag = True

jumpPin.irq(trigger=Pin.IRQ_FALLING, handler=jump)
startPin.irq(trigger=Pin.IRQ_FALLING, handler=start)

#Random number generator
def new_rope():
	global jumpFlag
	length = randint(0, 480)
	LCD.Solid_Box(length, 240, length+10, 250, red)
	count = 0
	for i in range(0, 480):
		if jumpFlag == 1:
			if count == 0:
				LCD.Solid_Box(i, 230, i+10, 240, blue)
				LCD.Solid_Box(i-10, 240, i, 250, grey)
			elif count > 0 and count < 40:
				LCD.Solid_Box(i, 230, i+10, 240, blue)
				LCD.Solid_Box(i-10, 230, i, 240, grey)
			elif count == 40:
				LCD.Solid_Box(i, 240, i+10, 250, blue)
				LCD.Solid_Box(i-10, 230, i, 240, grey)
				jumpFlag = 0
			count += 1
		else:
			LCD.Solid_Box(i, 240, i+10, 250, blue)
			LCD.Solid_Box(i-10, 240, i, 250, grey)
			if i == length:
				return True
		sleep_ms(10)
	jumpFlag = 0

def start_screen():
	LCD.Init()
	LCD.Clear(grey)
	LCD.Text("Press button 14 to begin", 150, 25, white, 3)
	LCD.Text("Score: " + str(score), 200, 100, white, 3)
	LCD.Solid_Box(0, 251, 479, 261, white)

score = 0
jumpFlag = 0
loseFlag = False
startFlag = False
start_screen()
while loseFlag is not True:
	while startFlag is not True:
		pass
	loseFlag = new_rope()
	sleep_ms(1000)
	startFlag = False

	
