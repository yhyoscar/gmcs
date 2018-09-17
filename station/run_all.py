from configure import *
from run_collectdata import *
from run_submitdata import *

from datetime import datetime, timedelta
from time import sleep
import numpy as np
import copy

password_node = ''
password_server = ''

def run_collect_submit(tlast):
    if len(password_node)>0 and len(password_server)>0:
        k = 0
        tlast_submit = copy.copy(tlast)
        while True:
            print('------------- collect data --------------')
            tlast = collect_recent(tlast, password=password_node)
            print('time break of collecting data (seconds): ', format(dt_collect), '...')
            sleep(dt_collect)

            if k % ncollect_per_submit == 0:
                print('========= submit data ==============')
                tlast_submit = submit_recent(tlast_submit, password=password_server)
            k += 1

    else:
        print('Error: please input passwords of nodes and server')
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pn", "--password_node", type=str, default='', \
        help="password of server")
    parser.add_argument("-ps", "--password_server", type=str, default='', \
        help="password of server")
    args = parser.parse_args()
    password_node = args.password_node.strip()
    password_server = args.password_server.strip()

    run_collect_submit( tlast = {node:datetime(2018,9,16,hour=13,minute=10) for node in ['n001001']})


