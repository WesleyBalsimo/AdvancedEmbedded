import LCD
from machine import Pin
from time import ticks_us, sleep_us, ticks_diff
from random import randint

# colors
grey = LCD.RGB(64, 64, 64)
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0)
red = LCD.RGB(255, 0, 0)
blue = LCD.RGB(0, 0, 255)

# pins
startPin = Pin(14, Pin.IN, Pin.PULL_UP)
jumpPin = Pin(15, Pin.IN, Pin.PULL_UP)

# interrupts
def jump(jumpPin):
    global jumpFlag, jumpStart, time2

    if jumpFlag == 0:
        jumpStart = ticks_us()
        time2 = jumpStart
        jumpFlag = 1


def start(startPin):
    global startFlag
    startFlag = True


jumpPin.irq(trigger=Pin.IRQ_FALLING, handler=jump)
startPin.irq(trigger=Pin.IRQ_FALLING, handler=start)

# Random number generator
def calc_travel_time_us():
    return randint(500_000, 1_500_000)


SCREEN_WIDTH = 480
JUMP_DURATION_US = 300_000


def new_rope(travel_time_us=calc_travel_time_us()):
    global jumpFlag, time1, time2, jumpStart

    length = SCREEN_WIDTH // 2
    LCD.Solid_Box(length, 240, length + 1, 260, red)

    previous_x = None
    previous_y = None

    # Start the timer immediately before movement
    time1 = ticks_us()

    while True:
        now = ticks_us()
        elapsed = ticks_diff(now, time1)

        # Stop after 1.5 seconds
        if elapsed >= travel_time_us:
            break

        # Calculate position based on elapsed time
        x = elapsed * SCREEN_WIDTH // travel_time_us

        # Determine whether the player is jumping
        jumping = jumpFlag == 1

        if jumping:
            box_y = 220
            if ticks_diff(now, jumpStart) >= JUMP_DURATION_US:
                jumpFlag = 0
                jumping = False
                box_y = 240
        else:
            box_y = 240

        # Erase the previous player position
        if previous_x is not None and previous_y is not None:
            LCD.Solid_Box(
                previous_x, previous_y,
                previous_x + 3, previous_y + 10, grey
            )

        # Draw the player
        LCD.Solid_Box(x, box_y, x + 3, box_y + 10, blue)

        previous_x = x
        previous_y = box_y

        # Check whether the player reaches the rope
        if not jumping and x <= length < x + 4:
            return True, 0

    rope_time = travel_time_us * length // SCREEN_WIDTH
    early_us = rope_time - ticks_diff(time2, time1)
    points = max(0, 100 - early_us // 1000)
    jumpFlag = 0
    return False, points


def start_screen():
    LCD.Init()
    LCD.Clear(grey)
    LCD.Text("Press button 14 to begin", 150, 25, white, 3)
    LCD.Text("Score: " + str(score), 200, 100, white, 3)
    LCD.Solid_Box(0, 251, 479, 261, white)


def reset_screen():
    LCD.Clear(grey)
    LCD.Solid_Box(0, 251, 479, 261, white)
    LCD.Text("Turn: " + str(turn), 200, 25, white, 3)
    LCD.Text("Score: " + str(score), 200, 100, white, 3)
    LCD.Solid_Box(0, 251, 479, 261, white)


def lose_screen():
    LCD.Clear(grey)
    LCD.Text("You lose!", 200, 100, white, 3)
    LCD.Text("Score: " + str(score), 200, 150, white, 3)


score = 0
turn = 1
jumpFlag = 0
loseFlag = False
startFlag = False

start_screen()

while 1:
    while startFlag is not True:
        pass
    reset_screen()
    loseFlag, points = new_rope()
    sleep_us(1_000_000)
    score += points
    turn += 1

    if loseFlag == True:
        lose_screen()
        turn = 1
        startFlag = False
        loseFlag = False
        score = 0
