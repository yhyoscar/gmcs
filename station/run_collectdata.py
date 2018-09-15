from configure import *

import os
import glob
import requests
from datetime import datetime, timedelta
from time import sleep


def check_url(url):
    try:
        rtest = requests.head(url)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", url); return False 
    except requests.exceptions.ConnectionError as errc:
        print ("Connecting Error:", url); return False
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", url); return False
    except requests.exceptions.RequestException as err:
        print ("Other Errors:", url); return False

    if requests.head(url).status_code == 200:
        return True
    else:
        return False

def move_csv(pathin, pathout):
    flist = glob.glob(pathin+'*.csv')
    if len(flist) > 0:
        ss = set([x.split('_')[1] for x in flist])
        for s in ss:
            if not os.path.isdir(pathout+s): os.system('mkdir '+pathout+s)
            flist = glob.glob(pathin+'*'+s+'*.csv')
            dstrs = set([x.split('_')[2].split('-')[0] for x in flist])
            for dstr in dstrs:
                if not os.path.isdir(pathout+s+'/'+dstr): os.system('mkdir '+pathout+s+'/'+dstr)
                os.system('mv -f '+pathin+'*'+s+'_'+dstr+'*.csv '+pathout+s+'/'+dstr+'/')
    return

def move_jpg(pathin, pathout):
    flist = glob.glob(pathin+'*.jpg')
    if len(flist) > 0:
        if not os.path.isdir(pathout+'snapshot'): os.system('mkdir '+pathout+'snapshot')
        flist = glob.glob(pathin+'*snapshot*.jpg')
        if len(flist) > 0:
            dstrs = set([x.split('_')[1].split('-')[0] for x in flist])
            for dstr in dstrs:
                if not os.path.isdir(pathout+'snapshot/'+dstr): os.system('mkdir '+pathout+'snapshot/'+dstr)
                os.system('mv -f '+pathin+'*snapshot_'+dstr+'*.jpg '+pathout+'snapshot/'+dstr+'/')
        
        if not os.path.isdir(pathout+'motion'): os.system('mkdir '+pathout+'motion')
        flist = glob.glob(pathin+'*motion*.jpg')
        if len(flist) > 0:
            dstrs = set([x.split('/')[-1].split('-')[0] for x in flist])
            for dstr in dstrs:
                dstr = dstr.strip()
                if not os.path.isdir(pathout+'motion/'+dstr): os.system('mkdir '+pathout+'motion/'+dstr)
                os.system('mv -f '+pathin+'*motion_'+dstr+'*.jpg '+pathout+'motion/'+dstr+'/')
    return


def collect_hist(nodes, display=False):
    for node in nodes:
        url = 'http://'+node_ip[node]+node_datapath
        
        if check_url(url):
            pnode = local_datapath + node +'/'
            if not os.path.isdir(pnode): os.system('mkdir '+pnode)
            if not os.path.isdir('./tmp'): os.system('mkdir ./tmp')
            else: os.system('rm -f ./tmp/*')

            # collect sensor data
            os.system('wget -r -nd --no-parent -R "index.html*" -A "*.csv" --level 3 '+ \
                    url+'sensors/ -P ./tmp')
            move_csv('./tmp/', pnode)

            # collect pictures
            os.system('wget -r -nd --no-parent -R "index.html*" -A "*.jpg" --level 1 '+ \
                    url+'pictures/ -P ./tmp')
            move_jpg('./tmp/', pnode)
    return

# tlast: {node:datetime}
def collect_recent(tlast):
    tnow = {}
    for node in tlast:
        url = 'http://'+node_ip[node]+node_datapath
        if check_url(url):
            tnow[node] = datetime.now()
            pnode = local_datapath + node +'/'
            if not os.path.isdir(pnode): os.system('mkdir '+pnode)
            if not os.path.isdir('./tmp'): os.system('mkdir ./tmp')
            else: os.system('rm -f ./tmp/*')
            
            t = datetime(tlast[node].year, tlast[node].month, tlast[node].day, \
                    hour=tlast[node].hour, minute=tlast[node].minute, second=0)
            while t <= tnow[node]:
                # collect sensor data
                fstr = '*'+t.strftime('%Y%m%d-%H%M')+'*.csv'
                os.system('wget -r -nd --no-parent -R "index.html*" -A "'+fstr+'" --level 3  '+ \
                        url+'sensors/ -P ./tmp')
                move_csv('./tmp/', pnode)
                
                # collect pictures
                fstr = '*'+t.strftime('%Y%m%d-%H%M')+'*.jpg'
                os.system('wget -r -nd --no-parent -R "index.html*" -A "'+fstr+'" --level 1 '+ \
                    url+'pictures/ -P ./tmp')
                move_jpg('./tmp/', pnode)

                t = t + timedelta(seconds=60)
        else:
            tnow[node] = tlast[node]

    return tnow

def run_collect( nodes, tlast_ss=None, tlast_pic=None):

    if tlast_ss

    tlast = {node:datetime.now() for node in nodes}
    collect_hist(nodes)

    while True:
        tlast = collect_recent( tlast = tlast )
        print('------ sleep for next collection ------')
        for i in range(int(dt_collect)):
            print(dt_collect - i)
            sleep(1, end=',')
        print(' ')
