from configure import *
from util import *

import os
import glob
from datetime import datetime, timedelta
from time import sleep


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
    for fstr in ['snapshot', 'motion']:
        if not os.path.isdir(pathout+fstr): os.system('mkdir '+pathout+fstr)
        flist = glob.glob(pathin+'*'+fstr+'*.jpg')
        print(flist)
        if len(flist) > 0:
            dstrs = set([x.split('/')[-1].split('_')[2].split('-')[0] for x in flist])
            for dstr in dstrs:
                dstr = dstr.strip()
                if not os.path.isdir(pathout+fstr+'/'+dstr): os.system('mkdir '+pathout+fstr+'/'+dstr)
                os.system('mv -f '+pathin+'*'+fstr+'_'+dstr+'*.jpg '+pathout+fstr+'/'+dstr+'/')
    return


def collect_hist(nodes, display=False, ss=True, pic=True):
    for node in nodes:
        url = 'http://'+node_ip[node]+node_datapath
        
        if check_url(url):
            pnode = local_datapath + node +'/'
            if not os.path.isdir(pnode): os.system('mkdir '+pnode)
            if not os.path.isdir('./tmp'): os.system('mkdir ./tmp')
            else: os.system('rm -f ./tmp/*')

            if ss:
                # collect sensor data
                os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "*.csv" --level 3 '+ \
                        url+'sensors/ -P ./tmp')
                move_csv('./tmp/', pnode)

            if pic:
                # collect pictures
                os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "*.jpg" --level 1 '+ \
                        url+'pictures/ -P ./tmp')
                move_jpg('./tmp/', pnode)
    return

# tlast: {node:datetime}
def collect_recent(tlast, ss=True, pic=True):
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
                if ss:
                    # collect sensor data
                    fstr = '*'+t.strftime('%Y%m%d-%H%M')+'*.csv'
                    os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "'+fstr+'" --level 3  '+ \
                            url+'sensors/ -P ./tmp')
                    move_csv('./tmp/', pnode)
                
                if pic:
                    # collect pictures
                    fstr = '*'+t.strftime('%Y%m%d-%H%M')+'*.jpg'
                    os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "'+fstr+'" --level 1 '+ \
                        url+'pictures/ -P ./tmp')
                    move_jpg('./tmp/', pnode)

                t = t + timedelta(seconds=60)
        else:
            tnow[node] = tlast[node]

    return tnow



def run_collect( nodes, ss=True, pic=True, hist=True, tlast=datetime(2018,9,15)):

    if hist:
        tlast = {node:datetime.now() for node in nodes}
        collect_hist(nodes, ss=ss, pic=pic)
    else:
        tlast = {node:tlast for node in nodes}

    while True:
        tlast = collect_recent( tlast = tlast , ss=ss, pic=pic)
        print('------ sleep for next collection ------')
        for i in range(int(dt_collect)):
            print(dt_collect - i)
            sleep(1)
        print(' ')


if __name__ == '__main__':
    #run_collect(['n001001'], ss=True, pic=True, hist=False, tlast=datetime(2018,9,15,hour=17,minute=30))
    run_collect(['n001001'], ss=True, pic=True, hist=True)

