from gpiozero import LightSensor
from time import sleep

lss = LightSensor(17)

while True:
    print(lss.value)
    sleep(0.1)



