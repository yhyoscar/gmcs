import subprocess
import os
from datetime import datetime, timedelta
from time import sleep
import glob

from configure import *

def clean_pid():
    allpid = subprocess.run(['ps', '-A'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip().split('\n')
    pids = []
    for x in allpid:
        if 'motion' in x:
            pid = x.strip().split(' ')[0]
            os.system('sudo kill '+pid)
        if 'python' in x:
            pid = x.strip().split(' ')[0]
            pids.append(pid)
    
    if len(pids) > 1:
        for pid in pids[:-1]:
            os.system('sudo kill '+pid)
    return


def clean_olddata():
    tnow = datetime.now()
    ss = [x.split('/')[-1] for x in glob.glob(path_ssout+'*')]
    for s in ss:
        dstrs = [x.split('/')[-1] for x in glob.glob(path_ssout+s+'/*')]
        for dstr in dstrs:
            if datetime.strptime(dstr, '%Y%m%d') + timedelta(days=keepdays[s]+1) < tnow:
                os.system('sudo rm -rf '+path_ssout+s+'/'+dstr)
    
    dstrs = [(tnow-timedelta(days=keepdays['snapshot']+i+1)).strftime('%Y%m%d') for i in range(2)]
    for dstr in dstrs:
        os.system('sudo rm -f '+path_picout+'*snapshot_'+dstr+'*.jpg')
    
    dstrs = [(tnow-timedelta(days=keepdays['motion']+i+1)).strftime('%Y%m%d') for i in range(2)]
    for dstr in dstrs:
        os.system('sudo rm -f '+path_picout+'*motion_'+dstr+'*.jpg')
    return


def run_ss(codes = ['ss_airtq.py', 'ss_light.py', 'ss_sound.py', 'ss_soilt.py', 'ss_soilq.py']):
    for code in codes:
        os.system('python3 '+code+' &')
    return


def run_motion(fconfigure):
    os.system('sudo motion -c '+fconfigure+' &')
    return


def auto_switch(dt_switch, endtime=datetime(2019,1,1)):
    while datetime.now() < endtime:
        # clean old data at midnight
        if datetime.now().hour == 0:  clean_olddata()
        
        # kill processes of sensors and camera
        clean_pid()

        # restart running sensors and camera
        sleep(10)  # 10 seconds break
        run_ss()
        if daytime[0] < datetime.now().hour < daytime[1]:
            run_motion(motion_conf_day)
        else:
            run_motion(motion_conf_night)
        
        sleep(dt_switch)
    return

if __name__ == '__main__':
    auto_switch(dt_restart, endtime=datetime(2019,1,1))

