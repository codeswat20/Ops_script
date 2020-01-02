#!/opt/junosvenv/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.start_shell import StartShell
import multiprocessing, subprocess, os, time, yaml
from datetime import datetime
from execute.execute import *
from execute.report import *
from math import *
import re

opf = open('verify.txt','a') #this file contains host IPs with connection status while executing script
opf.write('\nScript started at '+str(datetime.now())+'\n')
opf.close()

def execute(CLIk,dev):
    imodule = os.getcwd().rstrip('lib')+'/module/Juniper.yaml'
    with open(imodule) as jfile:
        for k2,v2 in yaml.load(jfile).items():
            if k2 == CLIk : exec(v2+'(dev)')

def connecthost(host):
    if not host.strip():return
    host = host.strip(os.linesep)
    def process(host):
        opf = open('verify.txt','a')
        try:
            print(host)
            dev.timeout = 120
            print('Connected to {}'.format(dev.facts['hostname']))
            hostn = str(dev.facts['hostname'])
            opf.write('Connected to '+str(host)+' ---> '+str(hostn)+'\n')
            for CLIk in CLI :
                execute(CLIk,dev)
            opf.close()
            dev.close()
        except EOFError:
            pass
        except OSError:
            pass
        except paramiko.ssh_exception.SSHException:
            pass
        except paramiko.ssh_exception.NoValidConnectionsError:
            pass
        except Exception as e:
            print('It didnt work..!')
            print(e)
        dev.close()
    #verify is device is connected or not
    try:
        dev = Device(host=host, user=ID, password=pw, port=22, attempts=3, auto_probe=15)
        print('Opening connection to: ',host)
        dev.open()
        process(host)
    except Exception as err:
        print ('Unable to open connection to {}: {}'.format(host, err))

def start_sc(inpfile):
    #open host file and pass host names to create multiple threads for connection to run parellely
    global ID, pw, hosts, ifile, CLI, module, dev, report
    def run_for_host(hosts):
        with multiprocessing.Pool(processes=NUM_PROCESSES) as process_pool:
            time_start = time.time()
            process_pool.map(connecthost, hosts)
        print("Finished in %f sec."% (time.time() - time_start))  # Total time taken for the script to execute

    inpf = os.getcwd().rstrip('lib')+'/'+inpfile
    if os.path.isfile(inpf):
        with open(inpf) as ifile:
            for k1,v1 in yaml.load(ifile).items():
                if k1 == 'CREDENTIALS': ID,pw = v1['ID'], v1['Password']
                if k1 == 'HOSTS': hosts = v1.split(' ')
                if k1 == 'NUMBER_PROCESSES' : NUM_PROCESSES= int(v1)
                if k1 == 'EXECUTE' : CLI = v1.split(' ')
                if k1 == 'MODULE' : module = v1.split(' ')
        run_for_host(hosts)
        for CLIk in CLI :
            if re.match(r"^generate.*report$",CLIk) : exec(CLIk+'()')
        opf.close()
        ifile.close()

    else : print ("Please enter correct input filename")
