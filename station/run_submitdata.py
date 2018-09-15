from configure import *
from util import *

import os
import glob
import requests
from datetime import datetime, timedelta
from time import sleep
import argparse
import pexpect

password = ''


def scp_pass(var_cmd):
    var_child = pexpect.spawn(var_cmd)
    var_child.delaybeforesend = None
    while flag:
        try:
            i = var_child.expect(["password:", pexpect.EOF])
            flag = False
        except pexpect.TIMEOUT:
            print('try scp again')
            flag = True

    if i==0:
        flag = True
        while flag:
            try: 
                var_child.sendline(password)
                var_child.expect(pexpect.EOF)
                flag = False
            except pexpect.TIMEOUT:
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
            cmd = 'scp -rv '+local_datapath+node+' '+server_ip+':'+server_datapath
            scp_pass(cmd)

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
            
            t = datetime(tlast[node].year, tlast[node].month, tlast[node].day, \
                    hour=tlast[node].hour, minute=tlast[node].minute, second=0)
            while t <= tnow[node]:
                fstr = '*'+t.strftime('%Y%m%d-%H%M')+'*'
                flist = glob.glob(local_datapath+'*/*/*/'+fstr)
                print(flist, len(flist))
                if not os.path.isdir('./tmp'): os.system('mkdir ./tmp')
                else: os.system('rm -f ./tmp/*')
                for x in flist:
                    os.system('cp -f '+x+' ./tmp')
                    #fname = x.split('/')[-1]
                    #dstr  = x.split('/')[-2]
                    #ss    = x.split('/')[-3]
                    #cmd = 'scp '+x+' '+server_ip+':'+server_datapath+node+'/'+ss+'/'+dstr
                    #scp_pass(cmd)
                    #sleep(0.2) # otherwise, it will be blocked

                t = t + timedelta(seconds=60)
        else:
            tnow[node] = tlast[node]

    return tnow


def run_submit(nodes, tin=datetime.now()-timedelta(seconds=dt_submit*2), hist=True):
    
    nodes = ['n001001']
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
        for i in range(int(dt_submit)):
            print(dt_submit - i)
            sleep(1)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", type=str, default='', \
        help="password of server")
    args = parser.parse_args()
    password = args.password.strip()
    
    if len(password) > 0:
        print(password)
        run_submit(['n001001'], hist=True, tin=datetime(2018,9,15,hour=0,minute=30))
    else:
        print('please input password of server: -p password ')

