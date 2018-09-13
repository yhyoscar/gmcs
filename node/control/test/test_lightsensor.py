from gpiozero import LightSensor
from time import sleep, strftime, gmtime


light = LightSensor(17)

while True:
    print(strftime('%Y-%M-%D_%H:%M:%S', gmtime()), light.value )
    sleep(0.5)
