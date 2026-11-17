from machine import Pin
from neopixel import NeoPixel
from time import sleep
N = 8
p = Pin(19)
np = NeoPixel(p,N,bpp=3,timing=1)
n = 0
dn = 1
while(1):
 if(n == 7):
    dn = -1
 if(n == 0):
    dn = +1
 n += dn
 np.fill([0,0,0])
 np[n] = (50,0,0)
 np.write()
 sleep(0.1)