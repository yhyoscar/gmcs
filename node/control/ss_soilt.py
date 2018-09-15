import os
import glob
from time import sleep
from datetime import datetime, timedelta

from configure import *
from util import *

# we use DS18B20 to measure soil temperature
def init_soilt():
    # Initialize the GPIO Pins
    os.system('modprobe w1-gpio')  # Turns on the GPIO module
    os.system('modprobe w1-therm') # Turns on the Temperature module

    # Finds the correct device file that holds the temperature data
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    #print('find DS18B20 sensor: ', device_file)
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

def run_ss_soilt(pin, pathout, dt_file, endtime, dt_sample=0.1, display=False):
    fname = init_soilt()
    while datetime.now() < endtime:
        t0, fid = create_datafile(pathout, node+'_soilt', display=display)
        fid.write('time,soilt\n')
        while (datetime.now()-t0).seconds < dt_file: 
            temp = read_soilt(fname)
            strout = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+','+str(round(temp, 2))
            fid.write(strout+'\n')
            sleep(dt_sample)
        fid.close()
    return

if __name__ == '__main__':
    run_ss_soilt(pin=pin_soilt, pathout=path_ssout+'soilt/', endtime=datetime(2019,1,1), \
            dt_file=filetimegap, dt_sample=1.0, display=False)



