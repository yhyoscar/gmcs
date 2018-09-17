from configure import *
from util import *

import argparse
import os
import glob
from datetime import datetime, timedelta
from time import sleep

password = ''

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
        if len(flist) > 0:
            dstrs = set([x.split('/')[-1].split('_')[2].split('-')[0] for x in flist])
            for dstr in dstrs:
                dstr = dstr.strip()
                if not os.path.isdir(pathout+fstr+'/'+dstr): os.system('mkdir '+pathout+fstr+'/'+dstr)
                os.system('mv -f '+pathin+'*'+fstr+'_'+dstr+'*.jpg '+pathout+fstr+'/'+dstr+'/')
    return


def collect_hist(nodes, display=False, ss=True, pic=True, scp=True, password=password):
    for node in nodes:
        url = 'http://'+node_ip[node]+node_datapath
        
        if check_url(url):
            pnode = local_datapath + node +'/'
            if not os.path.isdir(pnode): os.system('mkdir '+pnode)
            if not os.path.isdir('./tmp'): os.system('mkdir ./tmp')
            else: os.system('rm -f ./tmp/*')

            if ss:
                # collect sensor data
                if not scp:
                    os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "*.csv" --level 3 '+ \
                        url+'sensors/ -P ./tmp')
                    move_csv('./tmp/', pnode)
                else:
                    cmd = 'sshpass -p "'+password+'" scp -r pi@'+node_ip[node]+':'+node_scppath+'sensors/* '+pnode
                    print(cmd)
                    #os.system(cmd)

            if pic:
                # collect pictures
                if not scp:
                    os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "*.jpg" --level 1 '+ \
                        url+'pictures/ -P ./tmp')
                    move_jpg('./tmp/', pnode)
                else:
                    cmd = 'sshpass -p "'+password+'" scp pi@'+node_ip[node]+':'+node_scppath+'pictures/*.jpg ./tmp/'
                    print(cmd)
                    #os.system(cmd)
                    #move_jpg('./tmp/', pnode)
    return

# tlast: {node:datetime}
def collect_recent(tlast, ss=True, pic=True, scp=True, password=password):
    tnow = {}
    for node in tlast:
        url = 'http://'+node_ip[node]+node_datapath
        print('try collect data from node: ', url)
        if check_url(url):
            print('successfully log in node:', url)
            tnow[node] = datetime.now()
            pnode = local_datapath + node +'/'
            if not os.path.isdir(pnode): os.system('mkdir '+pnode)
            if not os.path.isdir('./tmp'): os.system('mkdir ./tmp')
            else: os.system('rm -f ./tmp/*')
            
            t = datetime(tlast[node].year, tlast[node].month, tlast[node].day, \
                    hour=tlast[node].hour, minute=tlast[node].minute, second=0) - timedelta(60)
            while t <= tnow[node]:
                if t + timedelta(seconds=3600) < tnow[node]:
                    tstr = t.strftime('%Y%m%d-%H')
                    dtloop = 3600
                else:
                    tstr = t.strftime('%Y%m%d-%H%M')
                    dtloop = 60

                if ss:
                    # collect sensor data
                    fstr = '*'+tstr+'*.csv'
                    if not scp:
                        os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "'+fstr+'" --level 3  '+ \
                            url+'sensors/ -P ./tmp')
                    else:
                        cmd = 'sshpass -p "'+password+'" scp pi@'+node_ip[node]+':'+node_scppath+'sensors/*/*/'+fstr+' ./tmp/'
                        print(cmd)
                        os.system(cmd)
                    flist = sorted(glob.glob('./tmp/*'), key=os.path.basename)
                    print(flist, len(flist))
                    move_csv('./tmp/', pnode)

                if pic:
                    # collect pictures
                    fstr = '*'+tstr+'*.jpg'
                    if not scp:
                        os.system('wget --progress=bar:force -r -nd --no-parent -R "index.html*" -A "'+fstr+'" --level 1 '+ \
                            url+'pictures/ -P ./tmp')
                    else:
                        cmd = 'sshpass -p "'+password+'" scp pi@'+node_ip[node]+':'+node_scppath+'pictures/'+fstr+' ./tmp/'
                        print(cmd)
                        os.system(cmd)
                    flist = sorted(glob.glob('./tmp/*'), key=os.path.basename)
                    print(flist, len(flist))
                    move_jpg('./tmp/', pnode)

                t = t + timedelta(seconds=dtloop)
        else:
            print('invalid node:', url)
            tnow[node] = tlast[node]

    return tnow



def run_collect( nodes, ss=True, pic=True, hist=True, tlast=datetime(2018,9,15), scp=True):
    if len(password) == 0 and scp:
        print('ERROR: please input password')
    else:
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
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", type=str, default='', \
        help="password of server")
    args = parser.parse_args()
    password = args.password.strip()
    
    run_collect(['n001001'], ss=True, pic=True, hist=False, tlast=datetime(2018,9,16,hour=11,minute=15))
    #run_collect(['n001001'], ss=True, pic=True, hist=True)

