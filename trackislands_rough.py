#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:48:57 2023
checked works with current setting
@author: sawang
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
mad=Madx()


oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
no_particles=8
islands=["top"]#,"right","bot","left"]

FP=[[[-0.016,0.0008],[0.025,-0.00049],[0.015,-0.00075],[-0.026,0.0005]],
    [[-0.028,0.0009],[0.0044,0.0003],[0.029,-0.0009],[-0.008,0.00025]],
    [[-0.017,0.0008],[0.025,-0.0005],[0.014,-0.0008],[-0.026,0.0005]],
    [[-0.017,0.0008],[0.025,-0.0005],[0.014,-0.0008],[-0.026,0.0005]]]

# FP=[[[-0.0155,0.00069],[0.021,-0.00043],[0.016,-0.00069],[-0.021,0.00044]],
#     [[-0.008,0.0006],[0.0223,-0.0005],[0.0007,-0.00054],[-0.0225,0.0005]],
#     [[-0.002,0.0004],[0.023,-0.0006],[0.0,-0.00037],[-0.024,0.00065]],
#     [[-0.022,0.00076],[0.009,0.0001],[0.023,-0.00075],[-0.011,-4e-5]]]

for k in range(len(oct_names)):
    for j in range(len(strengths)):
        for i in range(len(islands)):
            x0=FP[k][i][0]
            px0=FP[k][i][1]
            
           
            with open('track_island.madx', 'r') as file:
                data = file.read()
                data = data.replace("K3=0.1", "K3="+str(strengths[j]))
                data = data.replace("LOF.30802", oct_names[k])
                data = data.replace("x=0.02", "x="+str(x0)+"+n")
                data = data.replace("px=0.0", "px="+str(px0))
                
            with open('track_island.madx', 'w') as file:     
                file.write(data)
                
            mad.call("track_island.madx")
            
            for n in range (1,no_particles+1):
                if i <10:
                    name="track.obs0001.p000"+str(n)
                else:   
                    name="track.obs0001.p00"+str(n)
                    
                newname="track.oct="+oct_names[k]+"k3=" +str(strengths[j])+islands[i]+"no="+str(n)
                os.rename(name, newname)
                
                
            with open('track_island.madx', 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(strengths[j]),"K3=0.1")
                data = data.replace(oct_names[k],"LOF.30802")
                data = data.replace("x="+str(x0)+"+n","x=0.02")
                data = data.replace("px="+str(px0),"px=0.0")
            with open('track_island.madx', 'w') as file:     
                file.write(data)
       
            

