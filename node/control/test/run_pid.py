import subprocess
import os

allpid = subprocess.run(['ps', '-A'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip().split('\n')
for x in allpid:
    if ('motion' in x) or ('python' in x):
        print(x)

