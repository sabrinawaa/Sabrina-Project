import os
import sys

def main():
    oct_name = "LOE.22002,LOE.32002"
    k3= 0.6
    startPID = 0
    endPID = 1000000
    step = 100000
    flavour = "testmatch"

    fileDistName = "mass_track." + oct_name + "k3=" + str(k3)

    oneSubmitFileName = "./mass_track/{}/condor_submit_{}.sh".format(fileDistName, fileDistName)
    with open(oneSubmitFileName, 'w') as ff:
            ff.write("universe = vanilla\n")
            ff.write("executable = $(MYEXE)\n\n")
            ff.write("output = out/$(MYNAME)_$(ClusterId).$(ProcId).out\n")
            ff.write("error = error/$(MYNAME)_$(ClusterId).$(ProcId).err\n")
            ff.write("log = log/$(MYNAME)_$(ClusterId).$(ProcId).log\n\n")
            ff.write('+AccountingGroup = "group_u_BE.ABP.normal"\n')
            ff.write('+JobFlavour = "{}"\n\n'.format(flavour))

    for i in range(startPID, endPID, step):
        fileName = fileDistName + "_{}_{}.hdf5".format(i, i + step - 1)
        exeFileName = "./mass_track/{}/condor_exe_{}.sh".format(fileDistName, fileName[:-5])
        with open(exeFileName, 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_102b/x86_64-centos7-gcc12-dbg/setup.sh\n")
            f.write("source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate\n\n")
            f.write("ln -nfs /afs/cern.ch/eng/acc-models/sps/2021 sps\n\n")
            f.write(f"python3 {filename}\n")
            #fstring=literal string interpolation, interpolate values inside{}
        with open(oneSubmitFileName, 'a') as f:
            f.write("MYEXE=condor_exe_{}.sh\n".format(fileName[:-5]))
            f.write("MYNAME={}\n".format(fileName[:-5]))
            f.write("queue\n\n")

if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()
    

