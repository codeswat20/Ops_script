#!/opt/junosvenv/bin/python

from lib.connectdev import start_sc
import os

if __name__ == "__main__":
    start_sc('inpf.yaml')
    #print(os.path.isdir('inpf.yaml'))
