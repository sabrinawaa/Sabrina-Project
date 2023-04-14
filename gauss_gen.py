#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 11:05:23 2023

@author: sawang
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import shutil
import os
twiss_FP = pd.read_csv("Data/twiss_csv/1252_top.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==-2.2]
twiss_FP = twiss_FP[twiss_FP["Qx"]==26.7485]

# area = 1.24e-6
# std = np.sqrt( area *0.05/ np.pi) /3
std =  0.000613
offset = float(twiss_FP.ORBIT_PX) -0.000065

stds = np.linspace(std*0.25, std*1.75, 10)
offsets = np.linspace(offset - 3.2e-5, offset + 3.2e-5, 10)


std_grid,offs_grid=np.meshgrid(stds,offsets)
std_grid=std_grid.flatten()
offs_grid=offs_grid.flatten()

#%%
twiss_cent = pd.read_csv("Data/twiss_csv/cent_twiss.csv")
twiss_cent = twiss_cent[twiss_cent["k3"]==0.6]
twiss_cent = twiss_cent.iloc[[0]]

# for a in range (len(std_grid)):
foldername = "./submit/1252gauss_scan_-2.2_7485"
# os.mkdir(foldername)
            
gauss2d = np.random.normal(0, std, (3000,2))
xn = np.array(gauss2d[:,0])
pxn = np.array(gauss2d[:,1])

x = np.sqrt(float(twiss_cent.BETX)) * xn +float(twiss_FP.ORBIT_X)
px = float(twiss_FP.ORBIT_PX) - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX))
# only kick the px  to align with that of fixed point, cannot kick x

plt.scatter(x,px, s=1)
plt.scatter(twiss_FP.ORBIT_X, twiss_FP.ORBIT_PX, marker='x', s=10)
#%%

chunk_size=15

k3=[-2.2]#np.arange(4.9,8.41,0.7)
qx=[26.7485]#np.arange(26.729,26.7164,-0.0025)

for idx in range(len(k3)):
    
    with open("sq_template.madx", 'r') as file:
        data = file.read()
        data = data.replace("K3=0.1", "K3="+str(k3[idx]))
        data = data.replace("qx=QX","qx="+ str(qx[idx]))
        
        with open("sq_template.madx", 'w') as file:     
            file.write(data)
    
    
    for i in range(0,len(x),chunk_size):
        mad_filename = foldername+ "/gs32_"+str(i)+".madx"
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
        
        