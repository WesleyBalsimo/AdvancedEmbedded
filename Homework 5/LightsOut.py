#Lights out game

import LCD
from machine import Pin, I2C
from gt911 import GT911
from time import sleep_ms
from random import randint

rst_pin = Pin(10, Pin.OUT)
irq_pin = Pin(11)
sda_pin = Pin(8)
scl_pin = Pin(9)

touch = GT911(I2C(0, scl=scl_pin, sda=sda_pin, freq=100_000), rst_pin, irq_pin)
touch.init(touch_points=1, refresh_rate=50)

grey = LCD.RGB(64, 64, 64)
black = LCD.RGB(0, 0, 0,)
red = LCD.RGB(255, 0, 0)

x_pixel_max = 480
y_pixel_max = 320
boxes = []

# initialize the LCD
LCD.Init()
LCD.Clear(grey)

# make 8 randomly red boxes
size = 40
padding = 18

for i in range(1, 9):
    rand = randint(0, 1)
    if rand == 1:
        color = red
    else:
        color = black
    xmin, ymin = (size*(i-1))+padding*i, padding
    xmax, ymax = (size*(i))+padding*(i), size+padding

    boxes.append([xmin, ymin, xmax, ymax, color])
    LCD.Solid_Box(xmin, ymin, xmax, ymax, color)

