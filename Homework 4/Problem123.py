#drive a servo moter with a pwm
#pwm defined by adc1
#duty cycle is 500_000 to 2_500_000

from machine import ADC, Pin, PWM
from time import sleep_ms

Control = Pin(16, Pin.OUT)
Control = PWM(Pin(16))
Control.freq(50)
a2d1 = ADC(1)
duty = 1_500_000

while(1):
    y = a2d1.read_u16()
    duty = int(y * 30.5 + 500_000)
    Control.duty_ns(duty)
    sleep_ms(50)
    print(duty)