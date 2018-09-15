import time
import os
from datetime import datetime, timedelta

pid = '22908'
timegap = 60

while datetime.now() < datetime(2018,9,14,hour=6):
    time.sleep(timegap)

os.system('sudo kill '+pid)
time.sleep(2)
os.system('sudo motion -c /home/pi/.motion/motion.conf_day &')


