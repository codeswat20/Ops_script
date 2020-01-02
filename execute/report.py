#!/opt/junosvenv/bin/python

import hashlib, getpass, os, time,re, glob,csv
from datetime import datetime
from collections import Counter
import pandas as pd



def clear_data():
    filelist = [ f for f in os.listdir(dirN) if f.endswith(".txt")]
    for f in filelist: os.remove(os.path.join(dirN, f))
    os.rmdir(dirN)

def generate_sfp_report():
    print('there u r')
    global unique_host, unique_sfp, fdata, filename, dirN
    unique_host = []
    unique_sfp = ['hostname']
    fdata = {}
    filename = 'sfp_report_'+datetime.now().strftime("%d_%m_%Y")
    dirN = 'archive_for_SFP_'+datetime.now().strftime("%d_%m_%Y")
    def generate_report():
        opf = open('%s_sfpdata.csv'%filename,'a')
        opf.write('hostname,sfp_type,count\n')
        filelist = [ f for f in os.listdir(dirN) if f.endswith(".txt")]
        for f in filelist: os.remove(os.path.join(dirN, f))
        for files in os.listdir(dirN):
            if files.endswith(".csv"):
                fname = os.path.join(dirN, files)
                with open(fname) as filedata :
                    fileinfo = filedata.readlines()
                    for line in fileinfo :opf.write(line)
                filedata.close()
        opf.close()
        filelist = [ f for f in os.listdir(dirN) if f.endswith(".csv")]
        for f in filelist: os.remove(os.path.join(dirN, f))

        sfp = pd.read_csv('%s_sfpdata.csv'%filename)
        for i in range (0,len(sfp["hostname"])-1):
            hostn = (sfp["hostname"])[i]
            if hostn not in unique_host:
                unique_host.append(hostn)
                continue
            else: continue

        for i in range (0,len(sfp["sfp_type"])-1):
            sfpv = (sfp["sfp_type"])[i]
            if sfpv not in unique_sfp:
                unique_sfp.append(sfpv)
                continue
            else: continue

        header = ""
        with open('%s_parse.csv'%filename,'a') as finalcsv:
            for s in range(0,len(unique_sfp)) : header = header+unique_sfp[s]+','
            finalcsv.write(header.rstrip(',')+'\n')
            for h in range(0,len(unique_host)): finalcsv.write(unique_host[h]+',\n')
        finalcsv.close()

        sfp = pd.read_csv('%s_sfpdata.csv'%filename)
        finalsfp = pd.read_csv("%s_parse.csv"%filename)
        print(sfp)
        print(finalsfp)
        sfpreport = open('%s_sfp_report.csv'%filename,'a')
        for col in finalsfp.columns:
            print (col)
            sfpreport.write(str(col)+',')
        sfpreport.write('\n')

        print(finalsfp)

        for r in range(0,len(finalsfp['hostname'])):
            host2 = finalsfp['hostname'][r]
            sfpreport.write(host2+',')
            for cl in range(1,len(finalsfp.columns)):
                hdval = finalsfp.columns[cl]
                for m in range(0,len(sfp['hostname'])):
                    host1 = sfp['hostname'][m]
                    if (host1 == host2):
                        sfp1 = sfp['sfp_type'][m]
                        count1 = 0
                        if (sfp1 == hdval) :
                            count1 = sfp['count'][m]
                            break
                #print(sfp1+'------>'+hdval+'------>'+str(count1))
                sfpreport.write(str(count1)+',')
            sfpreport.write('\n')
        sfpreport.close()
        os.remove('%s_sfpdata.csv'%filename)
        os.remove('%s_parse.csv'%filename)

    #this funtion deals with collected data and generate csv report
    def count_sfp():
        filelist = [ f for f in os.listdir(dirN) if f.endswith(".txt")]
        for f in filelist:
            part_type = {}
            pt = {}
            part_number = []
            fname = f.split('_')[0]
            host_data = open(dirN+'/%s_chassis_hardware.txt' % fname ,'r')
            chassis_data = host_data.readlines()
            type = []
            for line in chassis_data :
                if ('10G' in line or '40G' in line) and ('SFP+-' in line or 'QSFP+-' in line or 'XFP-' in line) :
                    val = line.rstrip('\n')
                    print(val)
                    val = re.sub(r'([^ ]) ([^ ])',r'\1\2',val)
                    val = re.sub(r'\s10[G|GE]\s+','10GE',val)
                    val = re.sub(r'\s40[G|GE]\s+','40GE',val)
                    val = val.split()
                    type.append(val[len(val)-1])
                    print(val[len(val)-1])
                    continue
                else : continue
            print(type)
            sfp_dict = {}
            fdata = {}
            counter = Counter(type)
            for v in counter : print(v)
            sfp_dict.update(counter)
            print(sfp_dict)
            fdata.update({fname : sfp_dict})
            print(fdata)

            with open(dirN+'/%s_sfpdata.csv'%fname,'a') as hfile:
                for k, v in fdata.items():
                    for k1, v1 in v.items():
                        hfile.write(k+','+k1+','+str(v1)+'\n')
            hfile.close()
    count_sfp()
    generate_report()
    clear_data()
'''
def generate_dpcmem_report():
    print('there u r')
    global unique_host, unique_sfp, fdata, filename, dirN
    unique_host = []
    unique_sfp = ['hostname']
    fdata = {}
    filename = 'sfp_report'+datetime.now().strftime("%d_%m_%Y")
    dirN = 'archive_for_SFP_'+datetime.now().strftime("%d_%m_%Y")

    count_sfp()
    generate_report()
    clear_data()
'''
