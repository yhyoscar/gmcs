from datetime import datetime
import os

def create_datafile(path, fpre, display=False):
    t0 = datetime.now()
    dstr = t0.strftime('%Y%m%d')
    if not os.path.exists(path+dstr): os.system('mkdir '+path+dstr)
    fout = fpre+'_' + t0.strftime('%Y%m%d-%H%M%S')+'.csv'
    if display: print('output: '+path+dstr+'/'+fout)
    fid = open('./tmp/'+fout,'w')
    return t0, fid, path+dstr+'/', fout



