#!/bin/bash

source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh
source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate

ln -nfs /afs/cern.ch/eng/acc-models/sps/2021 sps

python3 sq32_260.py
