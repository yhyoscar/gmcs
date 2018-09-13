import os
import glob
import Adafruit_DHT
from gpiozero import LineSensor, LightSensor 
from time import strftime, gmtime, sleep
from datetime import datetime, timedelta

pin_airtq = 19
pin_sound = 26
pin_light = 17
pin_soilq = 27
pin_soilt = 4
pout = '/home/pi/Documents/data/sensors/'
node = 'n001001'
timegap = 60  # time gap between files: 60 seconds

# we use DS18B20 to measure soil temperature
def init_soilt():
    # Initialize the GPIO Pins
    os.system('modprobe w1-gpio')  # Turns on the GPIO module
    os.system('modprobe w1-therm') # Turns on the Temperature module

    # Finds the correct device file that holds the temperature data
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    print('find DS18B20 sensor: ', device_file)
    return device_file

# A function that reads the sensors data
def read_temp_raw(fname):
    f = open(fname, 'r') # Opens the temperature device file
    lines = f.readlines() # Returns the text
    f.close()
    return lines

def read_soilt(fname):
    lines = read_temp_raw(fname)    # Read the temperature 'device file'

    # While the first line does not contain 'YES', wait for 0.1s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.1)
        lines = read_temp_raw(fname)

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
    return temp_c

def init_sensor(pin, mode='line'):
    if mode == 'light': 
        return LightSensor(pin)
    if mode == 'line':
        return LineSensor(pin)

def read_digital(ss):
    x = ss.value
    if x is None: x = -999
    return x

def read_airtq(pin):
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    if T is None: T = -999
    if RH is None: RH = -999
    return T, RH

def create_datafile():
    t0 = datetime.now()
    dstr = t0.strftime('%Y%m%d')
    if not os.path.exists(pout+dstr): os.system('mkdir '+pout+dstr)
    fout = node+'_' + t0.strftime('%Y%m%d%H%M%S')+'.csv'
    print('output: '+pout+dstr+'/'+fout)
    fid = open(pout+dstr+'/'+fout,'w')
    fid.write('time,Tair,RHair,sound,light,Tsoil,Hsoil\n')
    return t0, fid

if __name__ == '__main__':
    ss_sound = init_sensor(pin_sound, mode='line')
    ss_light = init_sensor(pin_light, mode='light')
    ss_soilq = init_sensor(pin_soilq, mode='line')
    fn_soilt = init_soilt()
    
    t0, fid = create_datafile()
    while True:
        airt, airq  = read_airtq(pin = pin_airtq)
        sound = read_digital(ss_sound)
        light = read_digital(ss_light)
        soilq = read_digital(ss_soilq)
        soilt = read_soilt(fname = fn_soilt)
        
        strout = strftime('%Y-%m-%d_%H:%M:%S', gmtime())+','+str(round(airt,2))+','+str(round(airq,2)) + \
                ','+str(sound)+','+str(round(light,2))+','+str(round(soilt,2))+','+str(soilq) 
        
        dt = datetime.now() - t0

        if dt.seconds >= timegap:
            fid.close()
            t0, fid = create_datafile()
        
        fid.write(strout+'\n')



