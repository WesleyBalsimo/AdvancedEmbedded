#Sequentially turn on leds on gp16-18

from machine import Pin
from time import sleep

led = [Pin(i, Pin.OUT) for i in range(16, 19)]

while True:
    for i in range (3):
        led[i].on()
        sleep(1.0)
        led[i].off()


#VLED is 4.34V
#Vce is 0.533V