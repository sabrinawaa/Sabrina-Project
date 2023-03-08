#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 12:05:16 2023

@author: sawang
"""
from cpymad.madx import Madx

import os
mad=Madx()
#triplets
# 0.75, 25 has no good configs
job='ptctwiss_triplets.madx'
strengths=[0.6]
islands=["top","bot"]
oct_names=[["LOE.12002","LOE.32002","LOEN.52002"],["LOE.22002","LOE.32002","LOEN.52002"]]
FP=[
    [[-0.009,0.000545 ],[0.008, -0.000516]],
    [[-0.002,0.00038 ],[0.001, -0.00035]]
    ]



for k in range(len(oct_names)):
    for j in range(len(strengths)):
        for i in range(len(islands)):
            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3=0.1", "K3="+str(strengths[j]))
                data = data.replace("oct1", oct_names[k][0])
                data = data.replace("oct2",oct_names[k][1])
                data = data.replace("oct3",oct_names[k][2])
                data = data.replace("x=0.02", "x="+str(FP[k][i][0]))
                data = data.replace("px=0.0", "px="+str(FP[k][i][1]))
                
            with open(job, 'w') as file:     
                file.write(data)
                
            mad.call(job)
            
           
            twiss_newname="twiss.oct="+oct_names[k][0]+","+oct_names[k][1]+","+oct_names[k][2]+"k3=" +str(strengths[j])+islands[i]+".tfs"
            twissum_newname="twissum.oct="+oct_names[k][0]+","+oct_names[k][1]+","+oct_names[k][2]+"k3=" +str(strengths[j])+islands[i]+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)
                
            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(strengths[j]),"K3=0.1")
                data = data.replace( oct_names[k][0],"oct1")
                data = data.replace(oct_names[k][1],"oct2")
                data = data.replace(oct_names[k][2],"oct3")
                data = data.replace("x="+str(FP[k][i][0]),"x=0.02")
                data = data.replace("px="+str(FP[k][i][1]),"px=0.0")
            with open(job, 'w') as file:     
                file.write(data)
               