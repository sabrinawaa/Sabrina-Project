#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
32 top island find separatrix
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op
import os

import henon_funcs as fn
mad = Madx()
job = "turns.madx"

tune_tol = 0.0001
seg_tol = 1e-12

orbit_x = -0.002211155106
orbit_px = 0.000432587081
alfx = 1.728756
betx = 64.339926

# px_out = 0.0005# pick ini point outside island
# px_in = orbit_px

# px_tr = px_out

px_out= 0.0005
px_in=  0.00045
seg_len = abs(px_in - px_out)

i = 0
while seg_len > seg_tol:
    px_tr= (px_out+px_in)/2
    with open(job, 'r') as file:
        data = file.read()
        data = data.replace("px=PX", "px="+str(px_tr))
        data = data.replace("turns=t", "turns="+str(2048))
    with open(job, 'w') as file:     
        file.write(data)
        
    mad.call(job)
    
    name="track.obs0001.p0001"
            
    newname="iterate"+str(i)
    os.rename(name, newname)
        
    with open(job, 'r') as file:
        data = file.read()
        data = data.replace("px="+str(px_tr),"px=PX")
        data = data.replace("turns="+str(2048),"turns=t")
    with open(job, 'w') as file:     
        file.write(data)
                    
    track = pd.read_fwf(newname, skiprows=6,infer_nrows=2048)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)   
    x = np.array(track.X)
    px = np.array(track.PX)
    Qx = fn.fft_tune(x, px, float(alfx),float(betx))
    
    if abs(Qx-0.75) < tune_tol: #inside island
        px_in = px_tr

    else:   # outside island
        px_out = px_tr

        
    seg_len = abs(px_in - px_out)
    i += 1
    
    print("tr:",px_tr,"\n out:", px_out,"\n in", px_in)
    
#%%
plt.scatter(track.X,track.PX,marker='.',s=1)
#%%    
#final long run of good params
with open(job, 'r') as file:
    data = file.read()
    data = data.replace("px=PX", "px="+str(px_tr))
    data = data.replace("turns=t", "turns="+str(15000))
with open(job, 'w') as file:     
    file.write(data)
    
mad.call(job)

name="track.obs0001.p0001"

newname="32_separatrix"
os.rename(name, newname)
    
    
with open(job, 'r') as file:
    data = file.read()
    data = data.replace("px="+str(px_tr),"px=PX")
    data = data.replace("turns="+str(15000),"turns=t")
with open(job, 'w') as file:     
    file.write(data)

#%%
x0=[]
for i in range (26):
    newname="iterate"+str(i)
    track = pd.read_fwf(newname, skiprows=6,infer_nrows=1024)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)  
    # plt.scatter(track.X[1],track.PX[1],s=1,label=str(i))
    plt.scatter(track.X,track.PX,marker='.',s=1,label=str(i))

    
    plt.legend()
    x0.append(track.PX[1])
    
    if track.PX[1]==0.0004710540841574097:
        plt.figure()
        plt.scatter(track.X,track.PX,marker='.',s=10)
 