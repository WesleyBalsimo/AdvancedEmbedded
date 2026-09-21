#drive a servo moter with a pwm
#pwm defined by adc1
#duty cycle is 500_000 to 2_500_000

from machine import ADC, Pin, PWM
from time import sleep

Control = Pin(16, Pin.OUT)
Control = PWM(Pin(16))
Control.freq(50)
a2d1 = ADC(1)
duty = 1_500_000
dt = 0.01
y = 0
kx = 100 / 65535

while(1):
    x = kx * a2d1.read_u16()
    dy = -y + x
    y += dy * dt
    duty = int(y * 20_000 + 500_000)
    Control.duty_ns(duty)
    print(y)
    sleep(dt)
    duty_previous = duty