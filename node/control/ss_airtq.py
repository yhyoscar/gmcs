import Adafruit_DHT
from time import sleep
from datetime import datetime, timedelta
import os

from configure import *
from util import *

def read_airtq(pin):
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    if T is None: T = -999
    if RH is None: RH = -999
    return T, RH

def run_ss_airtq(pin, pathout, dt_file, endtime, dt_sample=0.1, display=False):
    while datetime.now() < endtime:
        t0, fid, pout, fout = create_datafile(pathout, node+'_airtq', display=display)
        fid.write('time,Tair,RHair\n')
        while (datetime.now()-t0).seconds < dt_file: 
            airt, airq = read_airtq(pin)
            strout = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+','+str(round(airt,2))+','+str(round(airq,2))
            fid.write(strout+'\n')
            sleep(dt_sample)
        fid.close()
        os.system('mv -f ./tmp/'+fout+' '+pout)

    return

if __name__ == '__main__':
    run_ss_airtq(pin=pin_airtq, pathout=path_ssout+'airtq/', endtime=datetime(2019,1,1), \
            dt_file=filetimegap, dt_sample=1.0, display=False)

