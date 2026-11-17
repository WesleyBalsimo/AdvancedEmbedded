from machine import Pin, ADC
from time import sleep, sleep_ms
import LCD

# LCD initialization
LCD.Init()
Black = LCD.RGB(0, 0, 0)
White = LCD.RGB(250, 250, 250)
Grey = LCD.RGB(100, 100, 100)
Yellow = LCD.RGB(250, 250, 0)


def New_Screen():
    LCD.Clear(Black)
    LCD.Box(0, 0, 479, 319, White)
    LCD.Title('Pulse Sensor', White, Black)

Line_Black = bytearray(402)
Line_Grey = bytearray(402)
Line = bytearray(402)
for i in range(0, 5):
    Line_Black[i * 100] = Grey >> 8
    Line_Black[i * 100 + 1] = Grey & 0xFF
for i in range(0, 201):
    Line_Grey[i * 2] = Grey >> 8
    Line_Grey[i * 2 + 1] = Grey & 0xFF


def Display(x, y):
    global Line, Line_Grey, Line_Black
    x += 1
    y = round(y)
    y = max(-100, min(100, y))

    LCD.Address_Set(x, 100, x, 300)
    LCD.StartWrite()
    LCD.dc.value(1)
    LCD.cs.value(0)

    if (x % 50) == 0:
        Line = Line_Grey
    else:
        Line = Line_Black

    ah = Line[200 - 2 * y]
    al = Line[201 - 2 * y]

    Line[200 - 2 * y] = Yellow >> 8
    Line[201 - 2 * y] = Yellow & 0xFF

    LCD.spi.write(Line)
    Line[200 - 2 * y] = ah
    Line[201 - 2 * y] = al


LCD.Init()
New_Screen()
x = 0
LED = Pin(16, Pin.OUT)
a2d = ADC(2)
k = 1 / 64
while (1):
    x = (x + 1) % 460
    y = round(k * (a2d.read_u16() - 0x8000))
    Display(x, y)
    sleep_ms(5)
