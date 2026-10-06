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
lighter_grey = LCD.RGB(100, 100, 100)
white = LCD.RGB(255, 255, 255)
black = LCD.RGB(0, 0, 0,)
red = LCD.RGB(255, 0, 0)

def read_touch():
    num_points, points_data = touch.read_points()
    msg = ''
    for i in range(num_points):
        msg = str(points_data[i][0]) + ',' + str(points_data[i][1])
    if(num_points > 0):
        print(msg)
        return int(points_data[i][0]), int(points_data[i][1])
    return None, None

def check_touch(x, y):
    for i in range(len(boxes)):
        if boxes[i][0] <= x <= boxes[i][2] and boxes[i][1] <= y <= boxes[i][3]:
            return i
    return None

def toggle_color(box_index):
    if boxes[box_index][4] == red:
        boxes[box_index][4] = black
    else:
        boxes[box_index][4] = red
    LCD.Solid_Box(boxes[box_index][0], boxes[box_index][1], boxes[box_index][2], boxes[box_index][3], boxes[box_index][4])

def check_win():
    for i in range(len(boxes)):
        if boxes[i][4] != red:
            return False
    return True

def check_secret(x, y):
    if x is None or y is None:
        return False
    if x_pixel_max-40 <= x <= x_pixel_max and y_pixel_max-40 <= y <= y_pixel_max:
        return True

# initialize the LCD
LCD.Init()
LCD.Clear(grey)

# make 8 randomly red boxes
size = 40
padding = 18
x_pixel_max = 480
y_pixel_max = 320
boxes = []

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

#secret 3rd option (win flag turns true) (not implemented yet)
LCD.Solid_Box(x_pixel_max-40, y_pixel_max-40, x_pixel_max, y_pixel_max, lighter_grey)

x = y = tries = 0
x_last = y_last = None
win_flag = False
while not win_flag:
    x, y = read_touch()
    if x is not None and y is not None and x is not x_last and y is not y_last:
        tries += 1
        box_index = check_touch(x, y)
        if box_index is not None:
            if box_index > 0:
                toggle_color(box_index - 1)
            toggle_color(box_index)
            if box_index < len(boxes) - 1:
                toggle_color(box_index + 1)
    
    win_flag = check_win() or check_secret(x, y)
    LCD.Text("Tries: " + str(tries), 200, 100, white, 3)
    x_last, y_last = x, y
    sleep_ms(250)

LCD.Clear(grey)
LCD.Text("You Win!", 200, 150, white, 3)
LCD.Text("Tries: " + str(tries), 200, 180, white, 3)
