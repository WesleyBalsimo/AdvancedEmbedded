#drive a DC motor with a H-bridge
from time import sleep
from machine import Pin


# Define H-bridge pins
pin_positive = Pin(15, Pin.OUT)
pin_negative = Pin(16, Pin.OUT)

while True:
    # Drive motor forward
    pin_positive.on()
    pin_negative.off()
    
    # Wait for a while
    sleep(5)
    
    # Stop the motor
    pin_positive.off()
    pin_negative.off()
    
    # Wait for a while
    sleep(10)
    
    # Drive motor backward
    pin_positive.off()
    pin_negative.on()
    
    # Wait for a while
    sleep(5)
    
    # Stop the motor
    pin_positive.off()
    pin_negative.off()
    
    # Wait for a while
    sleep(10)


#Vm clockwise = 2.64
#Vc clockwise = 3.24

#Vm counterclockwise = 2.67
#Vc counterclockwise = 3.24