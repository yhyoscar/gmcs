from gpiozero import PWMOutputDevice
from time import sleep
import numpy as np

a = PWMOutputDevice(27)

a.value = 0.0

pmin = 0.05
pmax = 0.255
t = 0.0
dt = 0.01
period = 4.0

while True:
    t += dt
    a.value = (np.sin(t/period*2*np.pi)+1.0)/2.0 * (pmax-pmin) + pmin
    sleep(dt)

