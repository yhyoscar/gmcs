from time import sleep
from datetime import datetime, timedelta
from gpiozero import LightSensor

from configure import *
from util import *


def run_ss_sound(pin, pathout, dt_file, endtime, dt_sample=0.1, display=False, analog=True):
    if analog:
        ss = MCP3008(pin)
    else:
        ss = LightSensor(pin)
    while datetime.now() < endtime:
        t0, fid, pout, fout = create_datafile(pathout, node+'_sound', display=display)
        fid.write('time,sound\n')
        while (datetime.now()-t0).seconds < dt_file: 
            strout = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+','+str(round(ss.value,2))
            fid.write(strout+'\n')
            sleep(dt_sample)
        fid.close()
        os.system('mv -f ./tmp/'+fout+' '+pout)
    return

if __name__ == '__main__':
    if analog: pin = channel_sound
    else: pin = pin_sound
    run_ss_sound(pin, pathout=path_ssout+'sound/', endtime=datetime(2019,1,1), \
            dt_file=filetimegap, dt_sample=1.0, display=False, analog=analog)

