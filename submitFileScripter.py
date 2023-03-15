import os
import sys
import shutil

def main():
    oct_name = "LOE.32002"
    k3= 0.6
    startPID = 0
    endPID = 7774
    step = 100
    flavour = "workday"
    folder = "32square_submit"
    
   
    oneSubmitFileName = "mass_track." + oct_name + "k3_" + str(k3) + ".sub"
    with open(oneSubmitFileName, 'w') as ff:
            ff.write("universe = vanilla\n")
            ff.write("executable = $(MYEXE)\n\n")
            ff.write("output = out/$(MYNAME)_$(ClusterId).$(ProcId).out\n")
            ff.write("error = error/$(MYNAME)_$(ClusterId).$(ProcId).err\n")
            ff.write("log = log/$(MYNAME)_$(ClusterId).$(ProcId).log\n\n")
            ff.write("transfer_input_files = $(MYINPUT)\n\n")
            ff.write('+AccountingGroup = "group_u_BE.ABP.normal"\n')
            ff.write('+JobFlavour = "{}"\n\n'.format(flavour))

    for i in range(startPID, endPID, step):
        exeFileName = "sq32_{}.sh".format(str(i))
        mad_filename = "sq32_{}.madx".format(folder,str(i))
        py_filename = "sq32_{}.py".format(str(i))
        with open(exeFileName, 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_102b/x86_64-centos7-gcc12-dbg/setup.sh\n")
            f.write("source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate\n\n")
            f.write("ln -nfs /afs/cern.ch/eng/acc-models/sps/2021 sps\n\n")
            f.write("python3 {}\n".format(mad_filename))
            #fstring=literal string interpolation, interpolate values inside{}
            
        shutil.copy("template.py",py_filename)
        with open(py_filename, 'r') as f:
            content = f.read()
            content = content.replace("job=","job="+"'"+str(mad_filename)+"'")
            content = content.replace("chunk=","chunk="+str(i))
        with open(py_filename, 'w') as f:     
            f.write(content)
            
        with open(oneSubmitFileName, 'a') as f:
            f.write("MYEXE= {}\n".format(exeFileName))
            f.write("MYNAME = {}\n".format("sq32_"+str(i)))
            f.write("MYINPUT = sps1.seq, {},  {}\n".format(mad_filename,py_filename))
            f.write("queue\n\n")

if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()
    

