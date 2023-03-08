#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:17:16 2023

@author: sawang
make tables of twiss results: alfc, alf
"""
#centre
from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op
import os
import henon_funcs as fn
#%%centre
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
no_particles=1

alldata=pd.DataFrame(columns=['name', 'k3', 'BETX', 'ALFX', 'ALPHA_C', 'ALPHA_C_P', 'ALPHA_C_P2',
       'ALPHA_C_P3', 'DQ1', 'DQ2'])

for k in oct_names:
    for j in strengths:
        twiss_name="Data/octtwiss/twiss.oct="+str(k)+"k3=" +str(j)+".tfs"
        twissum_name="Data/octtwiss/twissum.oct="+str(k)+"k3=" +str(j)+".tfs"
        
        twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
        twiss=twiss.drop(index=0)
        twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
        
        twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
        twiss_sum=twiss_sum.drop(index=0,columns='*')
        
        data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
        data.insert(0,"name",k)
        data.insert(1,"k3",j)
        data.insert(2,"ALFX",twiss.ALFX[1])
        data.insert(2,"BETX",twiss.BETX[1])
        
        alldata=alldata.append(data)
alldata.to_csv("cent_twiss.csv")        
        #%%islands
oct_names=["LOE.22002"]
strengths=[0.3,0.1,0.5,0.6,0.7,0.8,0.9]
islands=["top","bot"]
no_particles=1

alldata=pd.DataFrame(columns=['name', 'island','k3', 'max_X','BETX', 'ALFX', 'ALPHA_C', 'ALPHA_C_P', 'ALPHA_C_P2',
       'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])

for k in oct_names:
    for j in strengths:
        for i in range(len(islands)):
            twiss_name="Data/25_twiss_island/twiss.oct="+str(k)+"k3=" +str(j)+islands[i]+".tfs"
            twissum_name="Data/25_twiss_island/twissum.oct="+str(k)+"k3=" +str(j)+islands[i]+".tfs"
            
            twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
            twiss=twiss.drop(index=0)
            twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
            
            twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
            twiss_sum=twiss_sum.drop(index=0,columns='*')
            
            data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
            data.insert(0,"name",k)
            data.insert(1,"k3",j)
            data.insert(2,"island",islands[i])
            data.insert(3,"ALFX",twiss.ALFX[1])
            data.insert(3,"BETX",twiss.BETX[1])
            data.insert(3,"max_X",max(twiss.X))
            
            alldata=alldata.append(data)
            
# ,"LOE.32002","LOEN.52002"
alldata.to_csv("islands_twiss.csv")

#%%pairs
oct_names=["LOE.12002,LOE.22002","LOE.22002,LOE.32002","LOE.22002,LOE.52002"]
strengths=[0.6]
islands=["top","bot"]

alldata=pd.DataFrame(columns=['name', 'island','k3', 'max_X','BETX', 'ALFX', 'ALPHA_C', 'ALPHA_C_P', 'ALPHA_C_P2',
       'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])
for k in oct_names:
            for j in range(len(strengths)):
                for i in range(len(islands)):
                    twiss_name="Data/25twiss_pairs/twiss.oct="+k+"k3=" +str(strengths[j])+islands[i]+".tfs"
                    twissum_name="Data/25twiss_pairs/twissum.oct="+k+"k3=" +str(strengths[j])+islands[i]+".tfs"
                    
                    twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                    twiss=twiss.drop(index=0)
                    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                    
                    twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                    twiss_sum=twiss_sum.drop(index=0,columns='*')
                    
                    data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
                    data.insert(0,"name",k)
                    data.insert(1,"k3",strengths[j])
                    data.insert(2,"island",islands[i])
                    data.insert(3,"ALFX",twiss.ALFX[1])
                    data.insert(3,"BETX",twiss.BETX[1])
                    data.insert(3,"max_X",max(twiss.X))
                    
                    alldata=alldata.append(data)
            
# ,"LOE.32002","LOEN.52002"
alldata.to_csv("islands_twiss.csv")

#%% triplets
oct_names=["LOE.12002,LOE.32002,LOEN.52002","LOE.22002,LOE.32002,LOEN.52002"]
strengths=[0.6]
islands=["top","bot"]

alldata=pd.DataFrame(columns=['name', 'island','k3', 'max_X','BETX', 'ALFX', 'ALPHA_C', 'ALPHA_C_P', 'ALPHA_C_P2',
       'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])
for k in oct_names:
            for j in range(len(strengths)):
                for i in range(len(islands)):
                    twiss_name="Data/75twiss_triplets/twiss.oct="+k+"k3=" +str(strengths[j])+islands[i]+".tfs"
                    twissum_name="Data/75twiss_triplets/twissum.oct="+k+"k3=" +str(strengths[j])+islands[i]+".tfs"
                    
                    twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                    twiss=twiss.drop(index=0)
                    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                    
                    twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                    twiss_sum=twiss_sum.drop(index=0,columns='*')
                    
                    data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
                    data.insert(0,"name",k)
                    data.insert(1,"k3",strengths[j])
                    data.insert(2,"island",islands[i])
                    data.insert(3,"ALFX",twiss.ALFX[1])
                    data.insert(3,"BETX",twiss.BETX[1])
                    data.insert(3,"max_X",max(twiss.X))
                    
                    alldata=alldata.append(data)
            
# ,"LOE.32002","LOEN.52002"
alldata.to_csv("islands_twiss.csv")