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

def normalise (x,px,alf,beta):
    xn = np.array(x)/np.sqrt(beta)
    pxn = alf * np.array(x)/np.sqrt(beta) + np.array(px) * np.sqrt(beta)
    return xn,pxn
beta= 64.33992636
alfa = 1.728756478
#%%single
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]

strengths=[-0.6]
no_particles=8
no_turns=2048
colors= ['r','g','b']

twiss=pd.read_fwf('sps.tfs',skiprows=50,infer_nrows=3000)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)


for k in oct_names:
    for j in range(len(strengths)):
        for i in range (1,no_particles+1):
            
            name="Data/75island_k3/track.oct="+str(k)+"k3=" +str(strengths[j])+"no="+str(i)
          
            plt.figure(num=k)
            track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
            track = track.drop(index = 0,columns="*")
            track = track.astype(float)
            
            xnn,pxnn = normalise(track.X, track.PX, alfa, beta)
            
            
            plt.scatter(track.X,track.PX,marker='.',s=0.1,label= "k3="+str(strengths[j]))
            # plt.scatter(xnn,pxnn,marker='.',s=0.1)
            plt.xlabel("x (m)")
            plt.ylabel("$p_x $ (rad)")
            # plt.legend()
            
#%%pairs
oct_names=["LOE.32002","LOEN.52002"]
strengths=[0.6]#,-0.9,-1.2,-1.5,-1.8,-2.1]
no_particles=8
no_turns=2048
for a in range (len(oct_names)):
    for k in range (len(oct_names)):
        if a>k:
            print (oct_names[k],oct_names[a])
            for j in range(len(strengths)):
                for i in range (1,no_particles+1):
                    # name="Data/75pairs/track.oct="+oct_names[k]+","+oct_names[a]+"k3=" +str(strengths[j])+','+ str(strengths[j])+"no="+str(i)
                    name="Data/75_pair3252/track.oct="+oct_names[k]+","+oct_names[a]+"k3=" + str(strengths[j])+"no="+str(i)
                    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
                    track = track.drop(index = 0,columns="*")
                    track = track.astype(np.float64)
                    
                    plt.figure(num=oct_names[k]+oct_names[a])
                    plt.scatter(track.X,track.PX,marker='.',s=0.1)
                    plt.xlabel("x (m)")
                    plt.ylabel("$p_x $(rad)")
#%% triplets       
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[-0.9]
no_particles=16
no_turns=2048
for b in range (len(oct_names)):
    for a in range (len(oct_names)):
        if b>a:
            for k in range (len(oct_names)):
                if a>k:
                    print (oct_names[k],oct_names[a],oct_names[b])
                    for j in range(len(strengths)):
                        for i in range (1,no_particles+1):
                            # name="Data/25_123252_negk3/track.oct="+oct_names[k]+","+oct_names[a]+","+oct_names[b]+"k3=" +str(strengths[j])+"no="+str(i)
                            # name="Data/25DQ_-3.12trackpairs,triplets/track.oct="+oct_names[k]+","+oct_names[a]+","+oct_names[b]+"k3=" +str(strengths[j])+','+ str(strengths[j])+"no="+str(i)
                            
                            name="Data/75DQ_-3.12trackpairs,triplets/track.oct="+oct_names[k]+","+oct_names[a]+","+oct_names[b]+"k3=" +str(strengths[j])+"no="+str(i)
                            track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
                            track = track.drop(index = 0,columns="*")
                            track = track.astype(np.float64)
                            
                            plt.figure(num=oct_names[k]+oct_names[a]+oct_names[b])
                            # plt.figure(num=str(j))
                            plt.scatter(track.X,track.PX,marker='.',s=0.1)
                            plt.xlabel("x (m)")
                            plt.ylabel("$p_x $(rad)")
#%%all4
no_particles=8
for i in range (1,no_particles+1):
    # if i <10:
    #     name="Data/75triplets/track.obs0001.p000"+str(i)
    # else:   
    #     name="Data/75triplets/track.obs0001.p00"+str(i)
    name = "Data/all4/track.oct=all4k3=-0.6no="+str(i)
   
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    
    plt.scatter(track.X,track.PX,marker='.',s=0.1)
    plt.xlabel("X")
    plt.ylabel("p_X")
   
    #%%747
plt.scatter(-0.003791943669, 0.000779672626, marker='x', s=30,c='orange')
plt.scatter(-0.005054382282, 0.0009536294541 , marker='x', s=30,c='orange')
plt.scatter(-0.006786209248, 0.001178558315, marker='x', s=30,c='orange')
#%%748
plt.scatter(-0.003970787959, 0.0008080053465 , marker='x', s=30,c='red')
plt.scatter(-0.005750759367, 0.00105059112, marker='x', s=30,c='red')

