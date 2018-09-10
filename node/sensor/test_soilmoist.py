from gpiozero import LineSensor
import time
from datetime import datetime

sensor = LineSensor(17)

while True:
    print(datetime.now(), sensor.value)
    time.sleep(0.5)


