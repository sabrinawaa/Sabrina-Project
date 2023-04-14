import os
import sys
import shutil

def main():
    for K3 in [-2.2]:
        oct_name = "LOE.12002,LOEN.52002"
        k3= K3
        qx= 26.7485
        startPID = 0
        endPID = 7800
        step = 20
        flavour = "workday"
        folder = "./submit/1252sq_k3_"+str(k3)+"qx_"+str(qx)
        os.chdir(folder)
        os.mkdir("out")
        os.mkdir("err")
        os.mkdir("log")
        oneSubmitFileName = "mass_track." + oct_name + "k3_" + str(k3) + ".sub"
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
            exeFileName = "sq32_{}.sh".format(str(i))
            mad_filename = "sq32_{}.madx".format(str(i))
            py_filename = "sq32_{}.py".format(str(i))
            with open(exeFileName, 'w') as f:
                f.write("#!/bin/bash\n\n")
                f.write("source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh\n")
                f.write("source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate\n\n")
                f.write("python3 {}\n".format(py_filename))
                #fstring=literal string interpolation, interpolate values inside{}
                
            # shutil.copy("/home/sawang/Desktop/Project/Sabrina-Project/template.py",py_filename)
            shutil.copy("/Users/sabo4ever/Sabrina/EPFL/Project/template.py",py_filename)
            with open(py_filename, 'r') as f:
                content = f.read()
                content = content.replace("job=","job="+"'"+str(mad_filename)+"'")
                content = content.replace("chunk=","chunk="+str(i))
            with open(py_filename, 'w') as f:     
                f.write(content)
                
            with open(oneSubmitFileName, 'a') as f:
                f.write("MYEXE= {}\n".format(exeFileName))
                f.write("MYNAME = {}\n".format("sq32_"+str(i)))
                f.write("MYINPUT = /afs/cern.ch/work/s/sawang/public/project/macro.madx, /afs/cern.ch/work/s/sawang/public/project/ft_q26.str, /afs/cern.ch/work/s/sawang/public/project/sps1.seq, {},  {}\n".format(mad_filename,py_filename))
                f.write("queue\n\n")
        # os.chdir('/home/sawang/Desktop/Project/Sabrina-Project/')
        os.chdir("/Users/sabo4ever/Sabrina/EPFL/Project")
if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()
    

