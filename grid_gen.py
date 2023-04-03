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
import shutil
import os
#%%

no_turns = 2048


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
    
    
# twiss_cent = pd.read_csv("Data/twiss_csv/cent_twiss.csv")
# twiss_cent = twiss_cent.iloc[[0]]


twiss_cent = pd.DataFrame(data= [[64.33992636,1.728756478]],columns=["BETX","ALFX"])
twiss_cent.BETX = 64.33992636
twiss_cent.ALFX = 1.728756478

xns=np.linspace(-0.0023,0.0022,120)
pxns=np.linspace(0.00175,0.0035,65)
# pxns=np.linspace(0.0005,0.0048,100)

# xns=np.linspace(-0.0022,-0.0018,18)
# pxns=np.linspace(0.0013,0.0023,15)
xns=np.linspace(-0.0027,-0.0024,18)
pxns=np.linspace(0.002,0.003,15)
xn,pxn=np.meshgrid(xns,pxns)
xn=xn.flatten()
pxn=pxn.flatten()


x = np.sqrt(float(twiss_cent.BETX)) * xn 
px = - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX)) 
plt.scatter(x,px,s=5)
#%%
chunk_size=20
folder = "./submit/32_k3_6.3/"
# os.mkdir(folder)

for i in range(0,len(x),chunk_size):
    
    mad_filename = folder+ "/sq32_"+str(i)+".madx"
    shutil.copy("sq_template.madx",mad_filename)
        
    xchunk = x[i:i + chunk_size]
    pxchunk = px[i:i + chunk_size]
    value = []
    
    for j in range (len(xchunk)):
        value.append(f"ptc_start, x={xchunk[j]} , px={pxchunk[j]}, y= 0, py=0;\n")
    

    with open(mad_filename, "r") as f:
        contents = f.readlines()
    if contents[55].strip()=="":
        contents[55:55]=value
    else:
        print("ini pos already filled")

    with open(mad_filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)
            
            
            
            