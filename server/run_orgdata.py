
from configure import *
import glob
import os
from time import sleep
from datetime import datetime, timedelta

def orgnize_data(pin, pout):
    flist = glob.glob(pin+'/*')
    fset =  []
    if len(flist) > 0:
        for x in flist:
            fname = x.split('/')[-1]
            fpre = fname.split('-')[0]
            fset.append(fpre)
    fset = set(fset)
    for x in fset:
        node = x.split('_')[0]
        ss = x.split('_')[1]
        dstr = x.split('_')[2]
        if not os.path.isdir(pout+node): os.system('mkdir '+pout+node)
        if not os.path.isdir(pout+node+'/'+ss): os.system('mkdir '+pout+node+'/'+ss)
        if not os.path.isdir(pout+node+'/'+ss+'/'+dstr): os.system('mkdir '+pout+node+'/'+ss+'/'+dstr)
        cmd = 'mv -f '+pin+x+'* '+pout+node+'/'+ss+'/'+dstr+'/'
        print(cmd)
        os.system(cmd)
    return

def run_orgnize_data(pin, pout):
    while True:
        orgnize_data(pin=pin, pout=pout)
        for i in range(dt_check)[::-1]:
            print('time left for next check: ', i)
            sleep(1)
    return

if __name__=="__main__":
    run_orgnize_data(path_buffer, path_data)


