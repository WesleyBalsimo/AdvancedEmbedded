#combination lock using buttons on the raspberry pi pico

from machine import Pin
from time import sleep

button1, button2  = Pin(0, Pin.IN, Pin.PULL_UP), Pin(1, Pin.IN, Pin.PULL_UP)
button3, button4 = Pin(2, Pin.IN, Pin.PULL_UP), Pin(3, Pin.IN, Pin.PULL_UP)

delete, enter = Pin(14, Pin.IN, Pin.PULL_UP), Pin(15, Pin.IN, Pin.PULL_UP)

buzzer = Pin(13, Pin.OUT)
led1, led2 = Pin(16, Pin.OUT), Pin(17, Pin.OUT)

Combination = [1, 2, 3, 4]
input_combination = []
num_incorrect = 0

while True:
    print("Enter the combination")
    while enter.value() == 1:
        if button1.value() == 0:
            input_combination.append(1)
            print("input_combination:", input_combination)
            while button1.value() == 0:
                pass
        elif button2.value() == 0:
            input_combination.append(2)
            print("input_combination:", input_combination)
            while button2.value() == 0:
                pass
        elif button3.value() == 0:
            input_combination.append(3)
            print("input_combination:", input_combination)
            while button3.value() == 0:
                 pass
        elif button4.value() == 0:
            input_combination.append(4)
            print("input_combination:", input_combination)
            while button4.value() == 0:
                pass
        elif delete.value() == 0:
            if len(input_combination) > 0:
                input_combination.pop()
                print("input_combination:", input_combination)
                while delete.value() == 0:
                    pass
    if input_combination == Combination:
        print("Combination correct!")
        led2.value(1)
        sleep(1)
        led2.value(0)
        num_incorrect = 0  # Reset incorrect attempts
    else:
        print("Combination incorrect!")
        led1.value(1)
        sleep(1)
        led1.value(0)
        num_incorrect += 1
    if num_incorrect >= 3:
        buzzer.value(1)
        sleep(1)
        buzzer.value(0)
    input_combination = []
