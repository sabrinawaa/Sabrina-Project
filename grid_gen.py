#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:33:06 2023

@author: sawang
"""
#%%
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

xns=np.linspace(-0.0039,0.0035,120)
pxns=np.linspace(0.0033,0.0116,65)
# pxns=np.linspace(0.0005,0.0048,100)

# xns=np.linspace(-0.0022,-0.0018,18)
# pxns=np.linspace(0.0013,0.0023,15)
# xns=np.linspace(-0.0027,-0.0024,18)
# pxns=np.linspace(0.002,0.003,15) #for 32, qx=0.744, k3=2.1, enough central area.

xn,pxn=np.meshgrid(xns,pxns)
xn=xn.flatten()
pxn=pxn.flatten()


x = np.sqrt(float(twiss_cent.BETX)) * xn 
px = - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX)) 
plt.scatter(xn,pxn,s=5)
#%%
k3=[-2.5]#np.arange(4.9,8.41,0.7)
qx=[26.7485]#np.arange(26.729,26.7164,-0.0025)

for idx in range(len(k3)):
    
    with open("sq_template.madx", 'r') as file:
        data = file.read()
        data = data.replace("K3=0.1", "K3="+str(k3[idx]))
        data = data.replace("qx=QX","qx="+ str(qx[idx]))
        
        with open("sq_template.madx", 'w') as file:     
            file.write(data)
    
            
    
        
    chunk_size=20
    folder = "./submit/1252sq_k3_"+str(k3[idx])+"qx_"+str(qx[idx])+"/"
    os.mkdir(folder)
    
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
            
    with open("sq_template.madx", 'r') as file:
        data = file.read()
        data = data.replace("K3="+str(k3[idx]),"K3=0.1")
        data = data.replace("qx="+ str(qx[idx]),"qx=QX")
    with open("sq_template.madx", 'w') as file:     
        file.write(data)
        
#%%
"sps/toolkit/macro.madx"
chunk_size=20
folders= [8.4,10.5,12.6, 14.7, 16.8, 18.9, 21 , 23.1,25]
for k in folders:
    folder = "./submit/32_k3_"+str(k)+"/"
  
    for i in range(0,len(x),chunk_size):
        
        mad_filename = folder+ "/sq32_"+str(i)+".madx"
        
        with open(mad_filename, 'r') as file:
            data = file.read()
            data = data.replace("sps/toolkit/macro.madx", "macro.madx")

        with open(mad_filename, 'w') as file:     
            file.write(data)
            
                
            
            
            