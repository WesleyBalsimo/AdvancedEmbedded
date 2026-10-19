import LCD
from machine import Pin
from random import randint

#constant definitions
NUM_OF_CLICKS = 5
NUM_OF_INPUTS = 10
MIN_BPM = 40
MAX_BPM = 80

startPin = Pin(14, Pin.OUT, Pin.PULL_UP)
edgePin = Pin(15, Pin.OUT, Pin.PULL_UP)

#two edge interrupts
def startGame():
  global startFlag
  if startFlag == False
    startFlag = True
  
def seeBeat():
  global beatCount
  N += N

#two timer interrupts
def startBeat():
  global timerFlag
  if 

def endGame():
  global startFlag, beatCount
  if beatCount == (NUM_OF_CLICKS + NUM_OF_INPUTS)
    startFlag = False
  
  
time.Init(freq=