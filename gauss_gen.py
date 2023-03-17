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

area = 1.24e-6
std = np.sqrt( area *0.5/ np.pi) /3
twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.32002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

twiss_cent = pd.read_csv("Data/twiss_csv/cent_twiss.csv")
twiss_cent = twiss_cent[twiss_cent["k3"]==0.6]
twiss_cent = twiss_cent.iloc[[0]]

 
gauss2d = np.random.normal(0, std, (3000,2))
xn = np.array(gauss2d[:,0])
pxn = np.array(gauss2d[:,1])

x = np.sqrt(float(twiss_cent.BETX)) * xn 
px = - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX)) + float(twiss_FP.ORBIT_PX)
# only kick the px  to align with that of fixed point, cannot kick x
plt.scatter(x,px)

#%%
chunk_size=30

for i in range(0,len(x),chunk_size):
    mad_filename = "./submit/32gauss_submit1/gs32_"+str(i)+".madx"
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