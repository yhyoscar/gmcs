import os
import glob
import argparse
from datetime import datetime, timedelta
import time
import pexpect

node = 'n001001'
timegap = 60

path_node    = '/home/pi/Documents/data/'
path_station = '/disk2/yhy/Work/farm/data/'
ip_station = 'oscar@129.49.67.246'

def scp_pass(var_cmd, password):
    var_child = pexpect.spawn(var_cmd)
    var_child.delaybeforesend = None
    i = var_child.expect(["password:", pexpect.EOF])
    if i==0: 
        var_child.sendline(password)
        var_child.expect(pexpect.EOF)
    else:
        print('... scp timeout ...')
    return 

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", type=str, default="./", \
        help="password of station")
    args = parser.parse_args()

    password = args.password.strip()

    dstr = datetime.now().strftime('%Y%m%d')
    fsslist = glob.glob(path_node+'sensors/'+dstr+'/*.csv')
    nss = len(fsslist)
    fpiclist = glob.glob(path_node+'pictures/*'+dstr+'*.jpg')
    npic = len(fpiclist)
    
    if nss > 0:
        for fss in sorted(fsslist, key=os.path.basename)[:-1]:
            var_cmd = 'scp '+fss+' '+ip_station+':'+path_station+dstr+'/'+node+'/sensors/'
            print(var_cmd)
            scp_pass(var_cmd, password)
    
    if npic > 0:
        for fpic in sorted(fpiclist, key=os.path.basename)[:-1]:
            var_cmd = 'scp '+fpic+' '+ip_station+':'+path_station+dstr+'/'+node+'/pictures/'
            print(var_cmd)
            scp_pass(var_cmd, password)


    while True:
        fsslist  = sorted(glob.glob(path_node+'sensors/'+dstr+'/*.csv'), key=os.path.basename)[::-1]
        fpiclist = sorted(glob.glob(path_node+'pictures/*'+dstr+'*.jpg'), key=os.path.basename)[::-1]
        if len(fsslist) > nss and nss > 0:
            for i in range(len(fsslist)-nss):
                var_cmd = 'scp -v '+fsslist[i+1]+' '+ip_station+':'+path_station+dstr+'/'+node+'/sensors/'
                print(var_cmd)
                scp_pass(var_cmd, password)
            nss = len(fsslist)

        if len(fpiclist) > npic and npic > 1:
            for i in range(len(fpiclist)-npic):
                var_cmd = 'scp -v '+fpiclist[i+1]+' '+ip_station+':'+path_station+dstr+'/'+node+'/pictures/'
                print(var_cmd)
                scp_pass(var_cmd, password)
            npic = len(fpiclist)

        time.sleep(timegap)

