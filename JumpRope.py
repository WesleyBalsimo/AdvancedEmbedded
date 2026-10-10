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
	global time2
	jumpFlag = 1
	time2 = ticks_ms()
	
def start(startPin):
	global startFlag
	startFlag = True

jumpPin.irq(trigger=Pin.IRQ_FALLING, handler=jump)
startPin.irq(trigger=Pin.IRQ_FALLING, handler=start)

#Random number generator
def new_rope():
	global jumpFlag
	global time1
	length = randint(0, 480)
	LCD.Solid_Box(length, 240, length+1, 260, red)
	count = 0
	previous_y = None
	time1 = ticks_ms()
	for i in range(0, 480):
		jumping = jumpFlag == 1
		if jumping:
			count += 1
			box_y = 220
			if count == 30:
				jumpFlag = 0
				count = 0
		else:
			box_y = 240
		if previous_y is not None:
			LCD.Solid_Box(i-1, previous_y, i+2, previous_y+10, grey)
		LCD.Solid_Box(i, box_y, i+3, box_y+10, blue)
		previous_y = box_y
		if not jumping and i == length:
			return True
		sleep_ms(10)
	jumpFlag = 0

def start_screen():
	LCD.Init()
	LCD.Clear(grey)
	LCD.Text("Press button 14 to begin", 150, 25, white, 3)
	LCD.Text("Score: " + str(score), 200, 100, white, 3)
	LCD.Solid_Box(0, 251, 479, 261, white)

def reset_screen():
	LCD.Clear(grey)
	LCD.Text("Score: " + str(score), 200, 100, white, 3)
	LCD.Solid_Box(0, 251, 479, 261, white)

def lose_screen():
	LCD.Clear(grey)
	LCD.Text("You lose!", 200, 100, white, 3)
	LCD.Text("Score: " + str(score), 200, 150, white, 3)

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
	#score is a work in progress, should be higher for getting closer to the rope
	score = (time2 - time1)
	reset_screen()

lose_screen()
