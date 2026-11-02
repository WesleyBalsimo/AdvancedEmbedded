# Game of Higher or Lower
# Utilize LCD (480x320) and touch screen to play a game of higher or lower with a deck of cards.
import LCD
from machine import Pin, I2C, Timer
from gt911 import GT911
from random import randint
from time import sleep_ms, ticks_ms, ticks_diff
from math import sqrt

# Constant Definitions
ROUND_LENGTH   = 10 # seconds
TICK_LENGTH    = 100 # ms
TOUCH_DEBOUNCE = 250  # ms
BANK_START     = 100
POT_START      = 1
BUY_IN         = 10
QUIT           = 3
WIN            = True
LOSE           = False
OVER           = 1
UNDER          = 2
TIE            = 3
SECRET         = 4


# Display coordinates
TITLE_X = 100
TITLE_Y = 10

BANK_BOX = (15, 60, 145, 100)
POT_BOX = (15, 110, 145, 150)
LAST_BOX = (15, 160, 145, 215)
CURRENT_BOX = (15, 225, 145, 280)

TIMER_BOX = (210, 65, 240, 270)

OVER_BOX = (310, 65, 465, 115)
UNDER_BOX = (310, 130, 465, 180)
QUIT_BOX = (310, 195, 465, 245)

# Colors
grey = LCD.RGB(64, 64, 64)
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0)
red = LCD.RGB(255, 0, 0)
blue = LCD.RGB(0, 0, 255)
green = LCD.RGB(0, 150, 0)
dark_blue = LCD.RGB(0, 0, 150)

# I/O pins
resetPin = Pin(14, Pin.IN, Pin.PULL_UP)
startPin = Pin(15, Pin.IN, Pin.PULL_UP) 
easterEggLight = Pin(16, Pin.OUT)

rst_pin = Pin(10, Pin.OUT)
irq_pin = Pin(11)
sda_pin = Pin(8)
scl_pin = Pin(9)
touch = GT911(I2C(0, scl=scl_pin, sda=sda_pin, freq=100_000), rst_pin, irq_pin)
touch.init(touch_points=1, refresh_rate=50)

# Globals
tick = 0
startFlag = False
resetFlag = False
timeoutFlag = False
bank = 0
pot = POT_START
deck = 0
round = 0
startRequest = False
lastTick = -1
secretCount = 0
aceFlag = False
lastTouchTime = 0
touchActive = False

# Interrupt definitions
def resetGame(pin):
    global resetFlag
    resetFlag = True
resetPin.irq(trigger=Pin.IRQ_FALLING, handler=resetGame)

def startGame(pin):
    global startRequest
    startRequest = True
startPin.irq(trigger=Pin.IRQ_FALLING, handler=startGame)

def tic(timer):
    global tick, timeoutFlag, startFlag
    if startFlag:
        tick += 1
        if tick >= ROUND_LENGTH * 1000 // TICK_LENGTH:
            tick = ROUND_LENGTH * 1000 // TICK_LENGTH
            timeoutFlag = True
            startFlag = False
timer = Timer(-1)
timer.init(period=TICK_LENGTH, mode=Timer.PERIODIC, callback=tic)

# Function definitions
def read_touch():
    num_points, points_data = touch.read_points()
    msg = ''
    for i in range(num_points):
        msg = str(points_data[i][0]) + ',' + str(points_data[i][1])
    if(num_points > 0):
        print(msg)
        return int(points_data[i][0]), int(points_data[i][1])
    return None, None

def shuffle_cards():
    x = []
    y = LCD.Shuffle()
    for card_num in y:
        x.append([card_num // 13, card_num % 13])
    return x

def reset_game():
    global tick, round, bank, pot
    global startFlag, timeoutFlag, deck, lastTick
    global secretCount, aceFlag

    tick = 0
    round = 0
    bank = BANK_START
    pot = POT_START

    startFlag = False
    timeoutFlag = False

    secretCount = 0
    aceFlag = False
    easterEggLight.off()

    deck = shuffle_cards()
    lastTick = -1

def draw_button(box, msg, color):
    x0, y0, x1, y1 = box

    LCD.Solid_Box(x0, y0, x1, y1, color)

    # Center text (Text2 has 16x32 characters)
    text_width = len(msg) * 16
    text_x = x0 + (x1 - x0 - text_width) // 2
    text_y = y0 + (y1 - y0 - 32) // 2

    LCD.Text2(msg, text_x, text_y, white, color)

def initialize_display():
    LCD.Init()
    LCD.Clear(grey)

    # Title
    LCD.Text2("HIGHER OR LOWER", TITLE_X, TITLE_Y,
              white, grey)

    # Information boxes
    LCD.Solid_Box(*BANK_BOX, lighter_grey)
    LCD.Solid_Box(*POT_BOX, lighter_grey)
    LCD.Solid_Box(*LAST_BOX, lighter_grey)
    LCD.Solid_Box(*CURRENT_BOX, lighter_grey)

    # Buttons
    draw_button(OVER_BOX, "OVER", green)
    draw_button(UNDER_BOX, "UNDER", dark_blue)
    draw_button(QUIT_BOX, "QUIT", red)

    # Timer background
    LCD.Box(*TIMER_BOX, black)

def display_game():
    global bank, pot, round

    LCD.Solid_Box(*BANK_BOX, lighter_grey)
    LCD.Solid_Box(*POT_BOX, lighter_grey)
    LCD.Solid_Box(*LAST_BOX, lighter_grey)
    LCD.Solid_Box(*CURRENT_BOX, lighter_grey)

    LCD.Text("BANK: $" + str(bank), 20, 75, black, lighter_grey)
    LCD.Text("POT: $" + str(pot), 20, 125, black, lighter_grey)

    LCD.Text("LAST CARD:", 20, 165, black, lighter_grey)
    LCD.Text("CURRENT:", 20, 230, black, lighter_grey)

    if round > 0:
        display_card(deck[round-1], 20, 180)

    display_card(deck[round], 20, 245)

def display_card(card, x, y):
    suits = ["C", "D", "H", "S"]
    ranks = ["A", "2", "3", "4", "5", "6",
             "7", "8", "9", "10", "J", "Q", "K"]

    suit, value = card

    LCD.Text2(ranks[value] + " " + suits[suit],
              x, y, black, lighter_grey)

def display_timer():
    global tick

    x0, y0, x1, y1 = TIMER_BOX

    remaining = max(0, 1 - tick / (ROUND_LENGTH * 1000 // TICK_LENGTH))

    fill_height = int((y1-y0) * remaining)

    # Clear the timer interior
    LCD.Solid_Box(x0+1, y0+1, x1-1, y1-1, black)

    # Draw remaining time from bottom upwards
    if fill_height > 0:
        LCD.Solid_Box(x0+1, y1-fill_height, x1-1, y1-1, red)

    # Draw border
    LCD.Box(x0, y0, x1, y1, white)

def inside_box(x, y, box):
    x0, y0, x1, y1 = box
    return x0 <= x <= x1 and y0 <= y <= y1

def get_ans():
    global touchActive, lastTouchTime
    global secretCount, aceFlag

    num_points, points_data = touch.read_points()

    # Finger released
    if num_points == 0:
        touchActive = False
        return None

    # Ignore continuous contact
    if touchActive:
        return None

    touchActive = True

    # Debounce
    currentTime = ticks_ms()
    if ticks_diff(currentTime, lastTouchTime) < TOUCH_DEBOUNCE:
        return None
    lastTouchTime = currentTime

    x = int(points_data[0][0])
    y = int(points_data[0][1])

    # Secret button
    if inside_box(x, y, CURRENT_BOX):
        secretCount += 1
        if secretCount >= 3:
            secretCount = 0
            aceFlag = True
            if round < 51:
                force_next_ace()
                easterEggLight.on()
        return None
    
    if inside_box(x, y, OVER_BOX):
        return OVER
    if inside_box(x, y, UNDER_BOX):
        return UNDER
    if inside_box(x, y, QUIT_BOX):
        return QUIT
    return None

def check_ans(ans, round):
    global deck

    current_value = deck[round][1]
    next_value = deck[round+1][1]

    if next_value > current_value:
        return WIN if ans == OVER else LOSE
    elif next_value < current_value:
        return WIN if ans == UNDER else LOSE
    else:
        return TIE

def force_next_ace():
    global deck, round

    # Find all remaining aces
    ace_positions = []

    for i in range(round + 1, len(deck)):
        if deck[i][1] == 0:
            ace_positions.append(i)

    if len(ace_positions) > 0:
        # Select a random remaining ace
        ace_index = ace_positions[randint(0, len(ace_positions)-1)]

        # Swap it with the next card
        deck[round+1], deck[ace_index] = deck[ace_index], deck[round+1]

    else:
        # No remaining aces: force the next card to be an ace
        deck[round+1][1] = 0

    print("SECRET ACTIVATED!")

def lose():
    global pot, round, startFlag, tick

    pot = 1
    round = 0
    tick = 0
    startFlag = False

    easterEggLight.off()

    display_game()

def win():
    global pot, round, tick
    global aceFlag
    pot *= 2
    round += 1
    tick = 0

    if aceFlag and deck[round][1] == 0:
        aceFlag = False
        easterEggLight.off()

    display_game()

def tie():
    global round, tick
    global aceFlag
    
    round += 1
    tick = 0

    if aceFlag and deck[round][1] == 0:
            aceFlag = False
            easterEggLight.off()

    display_game()

def quit():
    global bank, pot, round, startFlag, tick
    global aceFlag
    bank = bank + pot
    pot = 1
    round = 0
    startFlag = False
    tick = 0
    aceFlag = False
    easterEggLight.off()
    display_game()


initialize_display()
reset_game()
display_game()

# Main loop
while True:

    # Reset game
    if resetFlag:
        resetFlag = False
        reset_game()
        initialize_display()
        display_game()

    # Start game request
    if startRequest:
        startRequest = False
        deck = shuffle_cards()

        if not startFlag and bank >= BUY_IN:
            bank -= BUY_IN
            pot = POT_START
            round = 0
            tick = 0
            timeoutFlag = False
            startFlag = True
            lastTick = -1

            display_game()

    # Update timer display
    if startFlag and tick != lastTick:
        display_timer()
        lastTick = tick

    # Handle timeout
    if timeoutFlag:
        timeoutFlag = False
        lose()

    # Handle touchscreen input
    if startFlag:
        answer = get_ans()
        print(answer)
        if answer == QUIT:
            quit()
        elif answer is not None:
            result = check_ans(answer, round)
            if result == WIN:
                win()
            elif result == LOSE:
                lose()
            elif result == TIE:
                tie()

            lastTick = -1

            # Check whether the deck has been exhausted (Congratulations)
            if round >= 51 and startFlag:
                bank += pot
                pot = 0
                startFlag = False
                display_game()

    sleep_ms(10)