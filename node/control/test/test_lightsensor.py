from gpiozero import LightSensor
from time import sleep, strftime, gmtime


light = LightSensor(17)

while True:
    print( light.value )
    sleep(0.1)
