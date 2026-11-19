#Game of craps
import LCD
from machine import Pin, I2C
from time import sleep_ms
from random import randint

# Colors
grey = LCD.RGB(64, 64, 64)
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0)
red = LCD.RGB(255, 0, 0)
blue = LCD.RGB(0, 0, 255)
green = LCD.RGB(0, 150, 0)
dark_blue = LCD.RGB(0, 0, 150)

# display coordinates
TITLE_X = 170
TITLE_Y = 8

LABEL_X = 25
VALUE_X = 205

BANK_Y = 55
PHASE_Y = 95
POINT_Y = 135
ROLL_Y = 175
BET_Y = 215
BET6_Y = 255
BET8_Y = 295

VALUE_WIDTH = 145
VALUE_HEIGHT = 32

DICE1_X = 365
DICE2_X = 420
DICE_Y = 115

# Global variables
off_phase_flag = False
on_phase_flag = False
place_bet_flag = False

bank = 100
die1 = 0
die2 = 0
roll = 0
phase = "OFF"
point = 0
bet = 0
place_bet_1 = 0
place_bet_2 = 0

def draw_screen():

    # Title
    LCD.Text2("CRAPS", TITLE_X, TITLE_Y, white, black)

    # Labels
    LCD.Text("BANK:", LABEL_X, BANK_Y + 8, white, black)
    LCD.Text("PHASE:", LABEL_X, PHASE_Y + 8, white, black)
    LCD.Text("POINT:", LABEL_X, POINT_Y + 8, white, black)
    LCD.Text("ROLL:", LABEL_X, ROLL_Y + 8, white, black)

    LCD.Text("PASS LINE:", LABEL_X, BET_Y + 8, white, black)
    LCD.Text("PLACE 6:", LABEL_X, BET6_Y + 8, white, black)
    LCD.Text("PLACE 8:", LABEL_X, BET8_Y + 8, white, black)

    # Value boxes
    LCD.Box(190, BANK_Y, 355, BANK_Y + 36, grey)
    LCD.Box(190, PHASE_Y, 355, PHASE_Y + 36, grey)
    LCD.Box(190, POINT_Y, 355, POINT_Y + 36, grey)
    LCD.Box(190, ROLL_Y, 355, ROLL_Y + 36, grey)

    LCD.Box(190, BET_Y, 355, BET_Y + 36, grey)
    LCD.Box(190, BET6_Y, 355, BET6_Y + 36, grey)
    LCD.Box(190, BET8_Y, 355, BET8_Y + 24, grey)

    # Dice labels
    LCD.Text("DICE", 390, 75, white, black)

    # Initial values
    update_bank()
    update_phase()
    update_point()
    update_roll()
    update_bets()

def update_value(value, y, width=VALUE_WIDTH):

    # Erase previous value
    LCD.Solid_Box(
        VALUE_X + 1,
        y + 1,
        VALUE_X + width,
        y + VALUE_HEIGHT,
        black
    )

    # Write new value
    LCD.Text2(str(value), VALUE_X + 5, y + 2, green, black)

def update_bank():
    update_value("{:.1f}".format(bank), BANK_Y)


def update_phase():
    update_value(phase, PHASE_Y)


def update_point():
    if point == 0:
        update_value("--", POINT_Y)
    else:
        update_value(str(point), POINT_Y)


def update_roll():
    update_value(str(roll), ROLL_Y)


def update_bets():
    update_value(str(bet), BET_Y)
    update_value(str(place_bet_1), BET6_Y)
    update_value(str(place_bet_2), BET8_Y)


def update_dice():

    # Draw each die independently
    LCD.Dice(die1, DICE1_X, DICE_Y, white, black)
    LCD.Dice(die2, DICE2_X, DICE_Y, white, black)

def roll_dice():

    global die1, die2, roll

    die1 = randint(1, 6)
    die2 = randint(1, 6)

    roll = die1 + die2

    update_roll()
    update_dice()

    sleep_ms(500)

    return roll

def take_bet():
    global bank
    bet = 0
    #bluetooth get bet (message looks like "b'int\r\n")

    if bet > bank:
        bet = bank
    return bet

def take_bet_1():
    global bank
    bet = 0, 0
    #bluetooth look for bet on 6 (message looks like "b'6bint\r\n")
    #bluetooth look for bet on 8 (message looks like "b'8bint\r\n")
    if bet[0] > bank:
        bet = (bank, bet[1])
    if bet[1] > bank:
        bet = (bet[0], bank)
    return bet


draw_screen()
place_bet_flag = True
while True:

    while off_phase_flag == True:

        phase = "COME OUT"
        update_phase()
    
        while place_bet_flag == True:
            bet = take_bet()
            update_bets()
            place_bet_flag = False

        roll = roll_dice()

        if roll == 7 or roll == 11:
            bank += (bet * 2)
            update_bank()
            print("You rolled a natural")
            off_phase_flag = False
            place_bet_flag = True

        elif roll == 2 or roll == 3 or roll == 12:
            bank -= bet
            print("You rolled craps")
            update_bank()
            off_phase_flag = False

        else:
            point = roll
            print("Your point is: ", point)
            update_point()
            off_phase_flag = False
            place_bet_flag = True
            on_phase_flag = True
            
    while on_phase_flag == True:

        phase = "POINT"
        update_phase()
        
        while place_bet_flag == True:
            temp1, temp2 = take_bet_1()
            place_bet_1 += temp1
            place_bet_2 += temp2
            update_bets()
            place_bet_flag = False
        
        roll = roll_dice()

        if roll == point:
            bank += (bet * 1.2)
            print("You rolled your point")
            update_bank()
            place_bet_flag = True

        elif roll == 6 and place_bet_1 > 0:
            bank += (place_bet_1 * 1.2)
            print("You rolled a 6")
            update_bank()
            place_bet_flag = True

        elif roll == 8 and place_bet_2 > 0:
            bank += (place_bet_2 * 1.2)
            print("You rolled an 8")
            update_bank()
            place_bet_flag = True

        elif roll == 7:
            bank = bank - bet - place_bet_1 - place_bet_2
            print("You rolled a 7")
            update_bank()
            on_phase_flag = False
            off_phase_flag = True
            place_bet_flag = True
            
            # Reset bets for next round
            place_bet_1 = 0
            place_bet_2 = 0
            point = 0

            update_point()
            update_bets()

