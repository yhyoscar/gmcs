import time
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM) # use board numbers
# define input pin
pin = 17
GPIO.setup(pin, GPIO.IN)

while True:
    if GPIO.input(pin) == GPIO.LOW:
        print(datetime.now(), ' low')
    else:
        print(datetime.now(), ' high')

    time.sleep(0.5)
