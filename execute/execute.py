#!/opt/junosvenv/bin/python
from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.start_shell import StartShell
import hashlib,  os, time,re, glob,csv
from datetime import datetime
from collections import Counter
import pandas as pd

def get_version(dev):
    op = dev.cli('show version')
    return op

def get_hostname(dev):
    print('Hostname is {}'.format(dev.facts['hostname']))

def sfp_data(dev):
    global dirN
    dirN = 'archive_for_SFP_'+datetime.now().strftime("%d_%m_%Y")
    if os.path.isdir(dirN) == False : os.mkdir(dirN)
    hostn = str(dev.facts['hostname'])
    with StartShell(dev) as ss:
        b = ss.run("awk -F'|' ' { for (i = 1; i <= NF; ++i) print i, $i; exit } ' | cli show chassis hardware ")
        with open(dirN+'/%s_chassis_hardware.txt' % hostn ,'w') as hf:
            hf.write("\n"+b[1])
        hf.close()

def dpc_mem(dev):
    with StartShell(dev) as ss:
        #b = ss.run("cli show chassis hardware models | grep FPC |grep DPCE| awk '{ print $2}'",this='%',timeout=10)
        CLI_1 = ss.run("cli show chassis hardware models| grep FPC |grep DPCE",timeout=10)
        if (CLI_1[0] == True) :
            head = CLI_1[1].split('\r\n')
            a = head[1].split(' ')[1]
            CLI_2 = ss.run("cli  request pfe execute target fpc%s command 'show jtree %s memory' | awk '{ print $1}'" % (a, a),timeout=10)
            time.sleep(2)
            if CLI_2[0] == True :
                ok = CLI_2[1].split('\r\n')
                list_of_yay = []
                for tup in ok:
                    list_of_yay.append(tup)
                seg0_total,seg0_used,seg1_total,seg1_used= list_of_yay[7], list_of_yay[8],list_of_yay[20], list_of_yay[21]
                percentage_seg0 = str((float(seg0_used) / float(seg0_total)) * 100)[:4] + '%'
                percentage_seg1 = str((float(seg1_used) / float(seg1_total)) * 100)[:4] + '%'
                #print ("Segment 0 memory used = ", (dev.facts['hostname']), percentage_seg0)
                #print ("Segment 1 memory used = ", (dev.facts['hostname']), percentage_seg1)
                with open('DPC-memory.csv', mode='a') as csv_file:
                    row_values = [(dev.facts['hostname']),percentage_seg0,percentage_seg1]
                    writer = csv.DictWriter(csv_file,fieldnames=row_values)
                    writer.writeheader()
                csv_file.close()
