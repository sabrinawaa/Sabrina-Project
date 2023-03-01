#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 22:02:29 2023

@author: sabo4ever
"""

from cpymad.madx import Madx

import os
mad=Madx()

oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.3,0.1,0.5,0.6,0.7,0.8,0.9]
no_particles=8
no_turns=1024

islands=["top","right","bot","left"]
FP=[[[-0.016,0.0008],[0.025,-0.00049],[0.015,-0.00075],[-0.026,0.0005]],
    [[-0.0028,0.0009],[0.0044,0.0003],[0.029,-0.0009],[-0.008,0.00025]],
    [[-0.017,0.0008],[0.025,-0.0005],[0.014,-0.0008],[-0.026,0.0005]],
    [[-0.017,0.0008],[0.025,-0.0005],[0.014,-0.0008],[-0.026,0.0005]]]


for k in range(len(oct_names)):
    for j in range(len(strengths)):
        for i in range(len(islands)):
            with open('job2.madx', 'r') as file:
                data = file.read()
                data = data.replace("K3=0.1", "K3="+str(strengths[j]))
                data = data.replace("LOF.30802", oct_names[k])
                data = data.replace("x=0.02", FP[k][i][0])
                data = data.replace("px=0.0", FP[k][i][1])
                
            with open('job2.madx', 'w') as file:     
                file.write(data)
                
            mad.call("job2.madx")
            
           
            twiss_newname="twiss.oct="+k+"k3=" +str(strengths[j])+islands[i]+".tfs"
            twissum_newname="twissum.oct="+k+"k3=" +str(strengths[j])+islands[i]+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)
                
            with open('job2.madx', 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(strengths[j]),"K3=0.1")
                data = data.replace(oct_names[k],"LOF.30802")
                data = data.replace(FP[k][i][0],"x=0.02")
                data = data.replace(FP[k][i][1],"px=0.0")
            with open('job2.madx', 'w') as file:     
                file.write(data)
       
        