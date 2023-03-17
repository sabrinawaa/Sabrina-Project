#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:18:55 2023

@author: sawang
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op

import henon_funcs as fn

def emittance(x,px):
    x=np.array(x)
    px=np.array(px)
    x_sqmean = np.mean(x**2)
    px_sqmean = np.mean(px**2)
    xpx_sqmean = (np.mean(x * px))**2
    return np.sqrt(x_sqmean * px_sqmean - xpx_sqmean)
#%%
no_particles=3000
no_turns=2048
folder="Data/GAUSS32_1/"
x0=[]
px0=[]
xfin=[]
pxfin=[]
for i in range (1,no_particles):
    name = folder + "32track.no=" + str(i)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    x0.append(track.X[1])
    px0.append(track.PX[1])
    xfin.append(track.X.iloc[-1])
    pxfin.append(track.PX.iloc[-1])
  #%%  

plt.figure(num="Initial Distribution")
plt.scatter(x0,px0,marker='.',s=0.1)

for i in [3253
          ]:
    # if i <10:
    #     name=folder+"track.obs0001.p000"+str(i)
    # elif 9<i<100:   
    #     name=folder+"track.obs0001.p00"+str(i)
    # elif 99<i<1000:
    #     name=folder+"track.obs0001.p0"+str(i)
    # else:
    #     name=folder+"track.obs0001.p"+str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    name =  "Data/SQ32/32track.no=" + str(i+1)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    x4 = np.array(track.X[::4])
    px4 = np.array(track.PX[::4]) 
    
    plt.scatter(x4,px4,marker='.',s=0.1)
    plt.scatter(0,0,marker='x',s=10) 
plt.xlabel("X0")
plt.ylabel("Px0")
print("emittance before=",emittance(x0,px0))

plt.figure(num="Final Dist")
plt.scatter(xfin,pxfin,marker='.',s=0.1)
plt.xlabel("X_fin")
plt.ylabel("Px_fin")
print("emittance before=",emittance(xfin,pxfin))
#%%
