import subprocess
import os
from datetime import datetime, timedelta
from time import sleep

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

def run_ss(codes = ['ss_airtq.py', 'ss_light.py', 'ss_sound.py', 'ss_soilt.py', 'ss_soilq.py']):
    for code in codes:
        os.system('python3 '+code+' &')
    return

def run_motion(fconfigure):
    os.system('sudo motion -c '+fconfigure+' &')
    return

def auto_switch(dt_switch, endtime=datetime(2019,1,1)):
    while datetime.now() < endtime:
        clean_pid()
        run_ss()
        if daytime[0] < datetime.now().hour < daytime[1]:
            run_motion(motion_conf_day)
        else:
            run_motion(motion_conf_night)
        sleep(dt_switch)
    return

if __name__ == '__main__':
    clean_pid()
    auto_switch(dt_restart, endtime=datetime(2019,1,1))
