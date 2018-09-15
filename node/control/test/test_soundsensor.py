import time
from gpiozero import LightSensor
from datetime import datetime

ss=LightSensor(26)
while True:
    print(ss.value)
    time.sleep(0.1)


