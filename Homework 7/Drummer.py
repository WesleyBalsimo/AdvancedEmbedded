import LCD
from machine import Pin, Timer
from random import randint
from time import sleep_ms, ticks_ms, ticks_diff
from math import sqrt

#constant definitions
NUM_OF_CLICKS = 8
NUM_OF_INPUTS = 16
MIN_BPM       = 80
MAX_BPM       = 120
FLASH_SIZE    = 5

TEXT_X_PLACE  = 130
TEXT_Y_START  = 10
DATA_OFFSET   = 100

# colors
grey = LCD.RGB(64, 64, 64)
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0)
red = LCD.RGB(255, 0, 0)
blue = LCD.RGB(0, 0, 255)

#I/O pins
startPin = Pin(14, Pin.IN, Pin.PULL_UP)
edgePin = Pin(15, Pin.IN, Pin.PULL_UP)

ledPin = Pin(16, Pin.OUT)
ledPin2 = Pin(17, Pin.OUT)
buzzer = Pin(13, Pin.OUT)

#globals
human_time = []
expected_time = []
errors = []
hits = 0
N = 0
flashCount = 0
processedBeats = 0
processed_frames = 0
displayed_frames = 0

#edge interrupts
def startGame(startPin):
    global startFlag
    if startFlag == False:
        startFlag = True
startPin.irq(trigger=Pin.IRQ_FALLING, handler=startGame)


def hit(edgePin):
    global hits, N, data, hitFlag
    if N >= NUM_OF_CLICKS and hits < NUM_OF_INPUTS:
        human_time.append(ticks_ms())
        hits += 1
edgePin.irq(trigger=Pin.IRQ_FALLING, handler=hit)

#timer interrupts
def tic(timer):
    global N
    N += 1
timer = Timer(-1)

#draw the start screen
def initScreen():
    LCD.Init()
    LCD.Clear(grey)
    text = ["Press button 14 to begin", "BPM", "# Beats", "Error", "Mean", "St Dev"]
    for i in range(6):
        LCD.Text(text[i], TEXT_X_PLACE, TEXT_Y_START+(20*i-1), white, 3)

def flashOutput(output):
    output.toggle()
    sleep_ms(FLASH_SIZE)
    output.toggle()

def calculateExpectedTime(bpm, start_ms):
    global expected_time

    expected_time = []
    beat_period_ms = 60000 // bpm

    for i in range(NUM_OF_INPUTS):
        expected_time.append(start_ms + beat_period_ms * (i + 1))

def processInformation():
    global errors
     # Index of the click that was just recorded
    i = processed_frames - 1

    # Calculate timing error in milliseconds
    error = ticks_diff(human_time[i], expected_time[i])
    errors.append(error)

    # Number of clicks processed so far
    num_beats = len(errors)

    # Mean signed timing error
    mean_error = sum(errors) / num_beats

    # Sample standard deviation of timing errors
    if num_beats > 1:
        variance = sum((e - mean_error)**2 for e in errors) / (num_beats - 1)
        std_dev = sqrt(variance)
    else:
        std_dev = 0


    # Display the current statistics
    LCD.Text(str(num_beats), TEXT_X_PLACE + DATA_OFFSET, TEXT_Y_START + 40, white, 3)

    LCD.Text(str(error),TEXT_X_PLACE + DATA_OFFSET, TEXT_Y_START + 60, white, 3)

    LCD.Text(str(mean_error),TEXT_X_PLACE + DATA_OFFSET, TEXT_Y_START + 80, white, 3)

    LCD.Text(str(std_dev),TEXT_X_PLACE + DATA_OFFSET, TEXT_Y_START + 100, white, 3)

def countOff():
    global N, flashCount, processedBeats

    N = 0
    flashCount = 0
    processedBeats = 0

    bpm = randint(MIN_BPM, MAX_BPM)
    beat_period_ms = 60000 // bpm
    LCD.Text(str(bpm), TEXT_X_PLACE + DATA_OFFSET, TEXT_Y_START+ 20, white, 3)

    try:
        timer.init(period=beat_period_ms, mode=Timer.PERIODIC, callback=tic)

        while flashCount < NUM_OF_CLICKS:
            if N > processedBeats:
                processedBeats += 1
                flashOutput(buzzer)
                flashCount += 1
    finally:
        timer.deinit()
        ledPin2.off()
    return bpm, ticks_ms()

startFlag = False
initScreen()
while 1:
    if startFlag == True:
        human_time = []
        expected_time = []
        errors = []
        hits = 0
        processed_frames = 0
        displayed_frames = 0

        flashOutput(ledPin)
        bpm, ticks = countOff()

        calculateExpectedTime(bpm, ticks)

        while displayed_frames <= NUM_OF_INPUTS:
            if hits > processed_frames:
                processed_frames += 1
                processInformation()
                displayed_frames += 1
        startFlag = False