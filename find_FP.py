#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:18:04 2023

@author: sawang
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op

import henon_funcs as fn
import os
mad=Madx()

oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.6]
no_particles=8
no_turns=1024
#%%single

twiss=pd.read_fwf('sps.tfs',skiprows=50,infer_nrows=3000)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)

for k in oct_names:
    for j in strengths:
        for i in range (1,no_particles+1):
            
            name="Data/track752/track.oct="+str(k)+"k3=" +str(j)+"no="+str(i)
            track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
            track = track.drop(index = 0,columns="*")
            track = track.astype(np.float)
            
            plt.figure(num=k)
            plt.scatter(track.X,track.PX,marker='.',s=0.1)
            plt.xlabel("X")
            plt.ylabel("p_X")
            
#%%pairs
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.6]
no_particles=7
for a in range (len(oct_names)):
    for k in range (len(oct_names)):
        if a>k:
            print (oct_names[k],oct_names[a])
            for j in range(len(strengths)):
                for i in range (1,no_particles+1):
                    name="Data/pairs/track.oct="+oct_names[k]+","+oct_names[a]+"k3=" +str(strengths[j])+"no="+str(i)
                    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
                    track = track.drop(index = 0,columns="*")
                    track = track.astype(np.float64)
                    
                    plt.figure(num=oct_names[k]+oct_names[a])
                    plt.scatter(track.X,track.PX,marker='.',s=0.1)
                    plt.xlabel("X")
                    plt.ylabel("p_X")
#%% triplets       
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.6]
no_particles=8
for b in range (len(oct_names)):
    for a in range (len(oct_names)):
        if b>a:
            for k in range (len(oct_names)):
                if a>k:
                    print (oct_names[k],oct_names[a],oct_names[b])
                    for j in range(len(strengths)):
                        for i in range (1,no_particles+1):
                            name="Data/75triplets/track.oct="+oct_names[k]+","+oct_names[a]+","+oct_names[b]+"k3=" +str(strengths[j])+"no="+str(i)
                            track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
                            track = track.drop(index = 0,columns="*")
                            track = track.astype(np.float64)
                            
                            plt.figure(num=oct_names[k]+oct_names[a]+oct_names[b])
                            plt.scatter(track.X,track.PX,marker='.',s=0.1)
                            plt.xlabel("X")
                            plt.ylabel("p_X")
#%%all4
no_particles=6
for i in range (6,no_particles+1):
    if i <10:
        name="Data/75triplets/track.obs0001.p000"+str(i)
    else:   
        name="Data/75triplets/track.obs0001.p00"+str(i)
   
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    
    plt.scatter(track.X,track.PX,marker='.',s=0.1)
    plt.xlabel("X")
    plt.ylabel("p_X")
   