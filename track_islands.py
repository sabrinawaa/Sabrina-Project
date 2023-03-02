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
strengths=[0.3,0.1,0.5,0.6,0.7,0.8,0.9]
no_particles=8
islands=["top","right","bot","left"]

alltwiss=pd.read_csv('islands_twiss.csv').reset_index()
#%%

for k in range(len(oct_names)):
    dataa=alltwiss[alltwiss["name"]==oct_names[k]]
    for j in range(len(strengths)):
        data1=dataa[dataa['k3']==strengths[j]]
        for i in range(len(islands)):
            data2=data1[data1['island']==islands[i]]
            x0=float(data2.ORBIT_X)
            px0=float(data2.ORBIT_PX)
            
           
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
       
            

