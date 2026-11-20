# Game of craps
import LCD
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
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
off_phase_flag = True
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

# Buffer for incoming Bluetooth data
rx_buffer = bytearray()

def on_rx(data):
    global rx_buffer

    rx_buffer.extend(data)




# functions ---
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

def receive_integer():
    global rx_buffer

    print("Waiting for Bluetooth input...")

    while True:
        if b'\n' in rx_buffer:
            index = rx_buffer.index(b'\n')
            message = rx_buffer[:index]
            rx_buffer = rx_buffer[index + 1:]

            print("Received:", message)

            try:
                value = int(message.strip())
                print("Bet:", value)
                return value

            except ValueError:
                print("Invalid bet received")

        sleep_ms(20)

def take_bet():
    # Wait for Bluetooth input
    sp.send(b"Enter pass line bet:\n")
    bet = receive_integer()
    # Limit bet to available bank
    if bet > bank:
        bet = bank

    return bet

def take_bet_1():
    # Get bet for 6
    sp.send(b"Enter place 6 bet:\n")
    bet6 = receive_integer()
    if bet6 > bank:
        bet6 = bank
    # Get bet for 8
    sp.send(b"Enter place 8 bet:\n")
    bet8 = receive_integer()
    if bet8 > bank:
        bet8 = bank
    return bet6, bet8

LCD.Init()
draw_screen()
print("Screen initialized")

# Bluetooth initialization ---
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)
sp.on_write(on_rx)
print("Bluetooth initialized")

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

            off_phase_flag = True
            place_bet_flag = True

        elif roll == 2 or roll == 3 or roll == 12:
            bank -= bet
            update_bank()
            print("You rolled craps")

            off_phase_flag = True
            place_bet_flag = True

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

