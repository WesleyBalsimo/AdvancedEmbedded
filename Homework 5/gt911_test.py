from time import sleep_ms
from machine import Pin, I2C
from gt911 import GT911

rst_pin = Pin(10, Pin.OUT)
irq_pin = Pin(11)
sda_pin = Pin(8)
scl_pin = Pin(9)

touch = GT911(
    I2C(0, scl=scl_pin, sda=sda_pin, freq=100_000),
    rst_pin,
    irq_pin
)

touch.init(touch_points=4, refresh_rate=50)

while True:
    num_points, points_data = touch.read_points()
    msg = ''
    for i in range(num_points):
        msg = msg + str(i) + ': ('  + str(points_data[i][0]) + ',' + str(points_data[i][1]) + ')  '
    if(num_points > 0):
        print(msg)