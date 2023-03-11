#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:38:11 2023

@author: sawang
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
import henon_funcs as fn
import scipy.optimize as op


mad=Madx()

alltwiss=pd.read_csv('Data/twiss_csv/islands_twiss.csv').reset_index()
alltwiss=alltwiss.loc[:, ~alltwiss.columns.isin(['index', 'Unnamed: 0'])]

#%% single islnads
oct_names=["LOE.32002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
no_particles=8
islands=["top","bot"]#,"right","bot","left"]




for k in oct_names:
    for i in islands:
        datatop=alltwiss[alltwiss["island"]==i].reset_index()
        datatop12=datatop[datatop["name"]==k].reset_index()
        datatop12=datatop12.sort_values(by=["k3"])
        csvname="Data/twiss_csv/75Islandtwiss_csv/"+k+i+"_twiss.csv"
        datatop12.to_csv(csvname)
        plt.figure(num=k+str(1))
        
        fitx=datatop12.k3
        fity=datatop12.ALPHA_C
        plt.scatter(fitx,fity,marker='.',s=10,label=i
                    )
        plt.ylabel("ALPHAC")
        plt.xlabel("k3")
        
        
        
        pfit=np.polyfit(fitx,fity,2)
        xx=np.linspace(fitx[0],fitx.iloc[-1],250)
        fit=np.poly1d(pfit)
        label="  a2="+str(pfit[0])+" a1="+str(pfit[1])+" a0="+str(pfit[2])
            
        plt.plot(xx,fit(xx),label=label)
        plt.legend()  
        
        # plt.figure(num=k+str(1))
        # plt.scatter(datatop12.k3,datatop12.ALPHA_C,marker='.',s=10,label=i+"alpha_c"
        #             )
        # plt.legend()
        # plt.figure(num=k+str(2))
        # plt.scatter(datatop12.k3,datatop12.ALPHA_C_P,marker='.',s=10,label=i+"alpha_c_p"
        #             )
        # plt.legend()
        # plt.figure(num=k+str(3))
        # plt.scatter(datatop12.k3,datatop12.ALPHA_C_P2,marker='.',s=10,label=i+"alpha_c_p2"
        #             )
        # plt.legend()
        # plt.figure(num=k+str(4))
        # plt.scatter(datatop12.k3,datatop12.ALPHA_C_P3,marker='.',s=10,label=i+"alpha_c_p3"
        #             )
        # plt.legend()

#%%pairs
# oct_names=["LOE.12002,LOE.22002","LOE.22002,LOE.32002","LOE.22002,LOE.52002"]#25 config
oct_names=["LOE.12002,LOE.32002","LOE.22002,LOE.32002","LOE.32002,LOE.52002"]#75 config
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
islands=["top","bot"]

for k in oct_names:
    for i in islands:
        datatop=alltwiss[alltwiss["island"]==i].reset_index()
        datatop12=datatop[datatop["name"]==k].reset_index()
        datatop12=datatop12.sort_values(by=["k3"])
        csvname="Data/twiss_csv/75pair_csv/"+k+i+"_twiss.csv"
        datatop12.to_csv(csvname)
        
#%%triplets
oct_names=["LOE.12002,LOE.32002,LOEN.52002","LOE.22002,LOE.32002,LOEN.52002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
islands=["top","bot"]
for k in oct_names:
    for i in islands:
        datatop=alltwiss[alltwiss["island"]==i].reset_index()
        datatop12=datatop[datatop["name"]==k].reset_index()
        datatop12=datatop12.sort_values(by=["k3"])
        csvname="Data/twiss_csv/75triplets_csv/"+k+i+"_twiss.csv"
        datatop12.to_csv(csvname)
        