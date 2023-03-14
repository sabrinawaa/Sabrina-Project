#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:33:06 2023

@author: sawang
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
no_particles = 1008
no_turns = 2048
folder =" Data/square22/"
job = "square.madx"

# for i in range (1,no_particles+1):
#     if i <10:
#         name=folder+"track.obs0001.p000"+str(i)
#     elif 9<i<100:   
#         name=folder+"track.obs0001.p00"+str(i)
#     elif 99<i<1000:
#         name=folder+"track.obs0001.p0"+str(i)
#     else:
#         name=folder+"track.obs0001.p"+str(i)    
    
#     track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
#     track = track.drop(index = 0,columns="*")
#     track = track.astype(np.float64)
#     plt.scatter(track.X,track.PX,marker='.',s=0.01)
    
    
twiss_cent = pd.read_csv("Data/twiss_csv/cent_twiss.csv")
twiss_cent = twiss_cent.iloc[[0]]

twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.22002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

xns=np.arange(-0.0029,0.0024,1.7726e-5)
pxns=np.arange(0.0012,0.0036,9.58e-5)
xn,pxn=np.meshgrid(xns,pxns)



x = np.sqrt(float(twiss_cent.BETX)) * xn 
px = - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX)) 
plt.scatter(x,px,s=0.1)
# value=[]
# for i in range(len(x)):
#     value.append(f"ptc_start, x={x} , px={px}, y= 0, py=0;\n")


# with open(job, "r") as f:
#     contents = f.readlines()

# contents.insert(60, value)

# with open(job, "w") as f:
#     contents = "".join(contents)
#     f.write(contents)