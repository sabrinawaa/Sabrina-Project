#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 10:58:38 2023

@author: sawang
"""

from cpymad.madx import Madx
import os
mad=Madx()

oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
no_particles=1

for k in oct_names:
    for j in range(len(strengths)):
        with open('job2.madx', 'r') as file:
            data = file.read()
            data = data.replace("K3=0.1", "K3="+str(strengths[j]))
            data = data.replace("LOF.30802", k)
            
            
        with open('job2.madx', 'w') as file:     
            file.write(data)
            
        mad.call("job2.madx")
        
        
        twiss_newname="twiss.oct="+k+"k3=" +str(strengths[j])+".tfs"
        twissum_newname="twissum.oct="+k+"k3=" +str(strengths[j])+".tfs"
        os.rename("ptc_twiss.tfs", twiss_newname)
        os.rename("ptc_twiss_summ.tfs", twissum_newname)
            
        with open('job2.madx', 'r') as file:
            data = file.read()
            data = data.replace("K3="+str(strengths[j]),"K3=0.1")
            data = data.replace(k,"LOF.30802")
        with open('job2.madx', 'w') as file:     
            file.write(data)
            
        print('-----------finished running strength=',strengths[j],"---------------")