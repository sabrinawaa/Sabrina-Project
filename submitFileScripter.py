import os
import sys
import shutil

#%%

def main():
    for K3 in ["-2.161_-3.239"]:
    # for K3 in ["-2.082,-3.118"]:
        oct_name = "LOE.12002,LOEN.52002"
        k3= K3
        qx= 26.7495
        startPID = 0
        endPID = 7800#7800
        step = 20
        flavour = "workday"
        # folder = "./submit/1252sq_k3_"+str(k3)+"qx_"+str(qx)
        folder = "submit/1252sq_-2.161,-3.239DQ_3,0.005_cent/"
        # folder = "submit/1252sq_-2.082,-3.118DQ_3,0.005_cent/"
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
                
            shutil.copy("/home/sawang/Desktop/Project/Sabrina-Project/template.py",py_filename)
            # shutil.copy("/Users/sabo4ever/Sabrina/EPFL/Project/template.py",py_filename)
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
        os.chdir('/home/sawang/Desktop/Project/Sabrina-Project/')
        # os.chdir("/Users/sabo4ever/Sabrina/EPFL/Project")
if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()

#%%

def main():
    k31 = [-0.9, -1.2, -1.5, -1.8,-2.1,-2.4] 
    
    k32 = [-0.9, -1.2, -1.5, -1.8,-2.1,-2.4] 
    folder = "./submit/1232Qx_248/"
    flavour = "longlunch"
    os.chdir(folder)
    os.mkdir("out")
    os.mkdir("err")
    os.mkdir("log")
    oct_name = "LOE.12002,LOEN.32002"
    qx= 26.248

    
    oneSubmitFileName = "track.sub"
    with open(oneSubmitFileName, 'w') as ff:
            ff.write("universe = vanilla\n")
            ff.write("executable = $(MYEXE)\n\n")
            ff.write("output = out/$(MYNAME)_$(ClusterId).$(ProcId).out\n")
            ff.write("error = err/$(MYNAME)_$(ClusterId).$(ProcId).err\n")
            ff.write("log = log/$(MYNAME)_$(ClusterId).$(ProcId).log\n\n")
            ff.write("transfer_input_files = $(MYINPUT)\n\n")
            ff.write('+AccountingGroup = "group_u_BE.ABP.normal"\n')
            ff.write('+JobFlavour = "{}"\n\n'.format(flavour))
    
    for idx in range(len(k31)):
        exeFileName = "K3="+str(k31[idx])+'_'+str(k32[idx])+".sh"
        mad_filename = "K3="+str(k31[idx])+'_'+str(k32[idx])+".madx"
        py_filename = "K3="+str(k31[idx])+'_'+str(k32[idx])+".py"
        
        with open(exeFileName, 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write("source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh\n")
            f.write("source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate\n\n")
            f.write("python3 {}\n".format(py_filename))
            #fstring=literal string interpolation, interpolate values inside{}
        
       

        with open(py_filename, 'r') as f:
            content = f.read()
            content = content.replace("job=","job="+"'"+str(mad_filename)+"'")
        with open(py_filename, 'w') as f:     
            f.write(content)
            
        with open(oneSubmitFileName, 'a') as f:
            f.write("MYEXE= {}\n".format(exeFileName))
            f.write("MYNAME = {}\n".format("JOB"+str(idx)))
            f.write("MYINPUT = /afs/cern.ch/work/s/sawang/public/project/macro.madx, /afs/cern.ch/work/s/sawang/public/project/ft_q26.str, /afs/cern.ch/work/s/sawang/public/project/sps1.seq, {},  {}\n".format(mad_filename,py_filename))
            f.write("queue\n\n")
    os.chdir('/home/sawang/Desktop/Project/Sabrina-Project/')
    # os.chdir("/Users/sabo4ever/Sabrina/EPFL/Project")
if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()

