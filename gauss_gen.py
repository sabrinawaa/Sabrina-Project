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
twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.32002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

area = 1.24e-6
std = np.sqrt( area *0.05/ np.pi) /3
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

for a in range (len(std_grid)):
    foldername = "submit/32gauss_scan_"+str(a)
    # os.mkdir()
                
    gauss2d = np.random.normal(0, std_grid[a], (3000,2))
    xn = np.array(gauss2d[:,0])
    pxn = np.array(gauss2d[:,1])
    
    x = np.sqrt(float(twiss_cent.BETX)) * xn 
    px = offs_grid[a] - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX))
    # only kick the px  to align with that of fixed point, cannot kick x

    
    chunk_size=15
    
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