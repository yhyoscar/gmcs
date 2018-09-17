from time import sleep
from datetime import datetime, timedelta
from gpiozero import LightSensor
import os

from configure import *
from util import *


def run_ss_light(pin, pathout, dt_file, endtime, dt_sample=0.1, display=False):
    ss = LightSensor(pin)
    while datetime.now() < endtime:
        t0, fid, pout, fout = create_datafile(pathout, node+'_light', display=display)
        fid.write('time,light\n')
        while (datetime.now()-t0).seconds < dt_file: 
            strout = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+','+str(round(ss.value,2))
            fid.write(strout+'\n')
            sleep(dt_sample)
        fid.close()
        os.system('mv -f ./tmp/'+fout+' '+pout)
    return

if __name__ == '__main__':
    run_ss_light(pin=pin_sound, pathout=path_ssout+'light/', endtime=datetime(2019,1,1), \
            dt_file=filetimegap, dt_sample=1.0, display=False)

