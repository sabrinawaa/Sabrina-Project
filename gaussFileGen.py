#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:44:16 2023

@author: sawang
"""

import os
import sys
import shutil

def main():
    oct_name = "LOE.32002"
    k3= 0.6
    startPID = 0
    endPID = 3000
    step = 15
    flavour = "workday"
    
    for i in range (100):
        folder = "./submit/32gauss_scan_"+ str(i)
        os.chdir(folder)
        # os.mkdir("out")
        # os.mkdir("err")
        # os.mkdir("log")
        oneSubmitFileName = "gauss_track." + oct_name + "k3_" + str(k3) + ".sub"
        with open(oneSubmitFileName, 'w') as ff:
                ff.write("universe = vanilla\n")
                ff.write("executable = $(MYEXE)\n\n")
                ff.write("output = out/$(MYNAME)_$(ClusterId).$(ProcId).out\n")
                ff.write("error = err/$(MYNAME)_$(ClusterId).$(ProcId).err\n")
                ff.write("log = log/$(MYNAME)_$(ClusterId).$(ProcId).log\n\n")
                ff.write("transfer_input_files = $(MYINPUT)\n\n")
                ff.write('+AccountingGroup = "group_u_BE.ABP.normal"\n')
                ff.write('+JobFlavour = "{}"\n\n'.format(flavour))
    
        for i in range(startPID, endPID, step):
            exeFileName = "gs32_{}.sh".format(str(i))
            mad_filename = "gs32_{}.madx".format(str(i))
            py_filename = "gs32_{}.py".format(str(i))
            with open(exeFileName, 'w') as f:
                f.write("#!/bin/bash\n\n")
                f.write("source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh\n")
                f.write("source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate\n\n")
                f.write("ln -nfs /afs/cern.ch/eng/acc-models/sps/2021 sps\n\n")
                f.write("python3 {}\n".format(py_filename))
                #fstring=literal string interpolation, interpolate values inside{}
                
            shutil.copy("/home/sawang/Desktop/Project/Sabrina-Project/template.py",py_filename)
            with open(py_filename, 'r') as f:
                content = f.read()
                content = content.replace("job=","job="+"'"+str(mad_filename)+"'")
                content = content.replace("chunk=","chunk="+str(i))
            with open(py_filename, 'w') as f:     
                f.write(content)
                
            with open(oneSubmitFileName, 'a') as f:
                f.write("MYEXE= {}\n".format(exeFileName))
                f.write("MYNAME = {}\n".format("gs32_"+str(i)))
                f.write("MYINPUT = sps1.seq, {},  {}\n".format(mad_filename,py_filename))
                f.write("queue\n\n")
                
        os.chdir('/home/sawang/Desktop/Project/Sabrina-Project/')

if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()
    

