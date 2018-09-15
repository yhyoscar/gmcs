from gpiozero import LightSensor
import time

sensor = LightSensor(27)

while True:
    print(sensor.value)
    time.sleep(0.1)


