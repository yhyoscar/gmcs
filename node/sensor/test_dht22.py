import Adafruit_DHT
import time

while True:
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17) 
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),', T =', T, ', RH =', RH)
    time.sleep(0.5)

