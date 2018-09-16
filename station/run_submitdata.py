from configure import *
from util import *

import os
import glob
import requests
from datetime import datetime, timedelta
from time import sleep
import argparse
import pexpect
import numpy as np

password = ''


def scp_pass(var_cmd):
    var_child = pexpect.spawn(var_cmd)
    var_child.delaybeforesend = None
    sleep(1.0)
    flag = True
    while flag:
        try:
            i = var_child.expect(["password:", pexpect.EOF])
            flag = False
        except pexpect.TIMEOUT:
            sleep(1.0)
            print('try scp again')
            flag = True

    if i==0:
        flag = True
        while flag:
            try: 
                var_child.sendline(password)
                sleep(1.0)
                var_child.expect(pexpect.EOF)
                flag = False
                sleep(1.0)
            except pexpect.TIMEOUT:
                sleep(1.0)
                print('send password timeout, try again')
                flag = True
    else:
        print('... scp timeout ...')
    return


# submit historical data
def submit_hist(nodes, display=False):
    for node in nodes:
        url = 'http://'+server_ip.split('@')[1]
        if check_url(url):
            print('server: ',url)
            #cmd = 'scp -rv '+local_datapath+node+' '+server_ip+':'+server_datapath
            #scp_pass(cmd)
            
            cmd = 'sshpass -p "'+password+'" scp -r '+local_datapath+node+' '+server_ip+':'+server_datapath
            print(cmd)
            os.system(cmd)
            
            # random break
            for i in range(int(np.random.rand()*50+10))[::-1]:
                print('random break: ', i)
                sleep(1) # don't submit data too frequently, otherwise your IP will be blocked

    return

# tlast: {node:datetime}
def submit_recent(tlast):
    tnow = {}
    for node in tlast:
        url = 'http://'+server_ip.split('@')[1]
        print(url)
        if check_url(url):
            print('server: ', url)
            tnow[node] = datetime.now()
            pnode = local_datapath + node +'/'
            
            if not os.path.isdir('./tmp_submit'): os.system('mkdir ./tmp_submit')
            else: os.system('rm -f ./tmp_submit/*')
            
            t = datetime(tlast[node].year, tlast[node].month, tlast[node].day, \
                    hour=tlast[node].hour, minute=tlast[node].minute, second=0)
            while t <= tnow[node]:
                fstr = '*'+t.strftime('%Y%m%d-%H%M')+'*'
                flist = glob.glob(pnode+'/*/*/'+fstr)
                if len(flist) > 0:
                    print(flist, len(flist))
                    for x in flist:
                        os.system('cp -f '+x+' ./tmp_submit/')
                    #cmd = 'scp -r ./tmp_submit '+server_ip+':'+server_datapath+'/'
                    #scp_pass(cmd)
                    
                    #cmd = 'sshpass -p "'+password+'" scp -r ./tmp_submit '+server_ip+':'+server_datapath
                    #print(cmd)
                    #os.system(cmd)
                t = t + timedelta(seconds=60)
            
            # submit data to server
            cmd = 'sshpass -p "'+password+'" scp -r ./tmp_submit '+server_ip+':'+server_datapath
            print(cmd)
            print('how many files: ', len(glob.glob('./tmp_submit/*')))
            os.system(cmd)
           
            # random break
            for i in range(int(np.random.rand()*50+10))[::-1]:
                print('random break: ', i)
                sleep(1) # don't submit data too frequently, otherwise your IP will be blocked
        else:
            tnow[node] = tlast[node]

    return tnow


def run_submit(nodes, tin=datetime(2018,9,15), hist=True):
    
    if len(password) == 0:
        print('please input password of server: -p password ')
    else: 
        if hist:
            print('submit historical data')
            tlast = {node:datetime.now() for node in nodes}
            submit_hist(nodes)

        else:
            tlast = {node:tin for node in nodes}
        
        while True:
            print('submit recent data')
            tlast = submit_recent( tlast = tlast )
            print('------ sleep for next collection ------')
            for i in range(int(dt_submit))[::-1]:
                print('time left for next submit: ', i)
                sleep(1)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", type=str, default='', \
        help="password of server")
    args = parser.parse_args()
    password = args.password.strip()
    
    # run 
    run_submit(['n001001'], hist=False, tin=datetime(2018,9,15, hour=18, minute=10))

