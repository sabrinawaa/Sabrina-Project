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
alldata.to_csv("data/twiss_csv/cent_twiss.csv")        
        #%%islands
oct_names=["LOE.22002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
islands=["top","bot"]
no_particles=1

alldata=pd.DataFrame(columns=['name', 'island','k3', 'max_X','BETX', 'ALFX', 'ALPHA_C', 'ALPHA_C_P', 'ALPHA_C_P2',
       'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])

for k in oct_names:
    for j in strengths:
        for i in range(len(islands)):
            twiss_name="Data/75_twiss_island/twiss.oct="+str(k)+"k3=" +str(j)+islands[i]+".tfs"
            twissum_name="Data/75_twiss_island/twissum.oct="+str(k)+"k3=" +str(j)+islands[i]+".tfs"
            
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
alldata.to_csv("Data/twiss_csv/islands_twiss.csv")

#%%pairs
# oct_names=["LOE.12002,LOE.22002","LOE.12002,LOE.32002","LOE.22002,LOE.32002"]#25 config
# oct_names=["LOE.22002,LOEN.52002","LOE.32002,LOEN.52002"]#75 config
oct_names=["LOE.12002,LOEN.52002"]

strengths=[-2.5]
Qx=[26.7485]
islands=["top"]#,"bot"]

alldata=pd.DataFrame(columns=['name', 'island','k3', 'Qx','max_X','BETX', 'ALFX', 'ALPHA_C', 'ALPHA_C_P', 'ALPHA_C_P2',
        'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])
for k in oct_names:
    for qx in Qx:
            for j in range(len(strengths)):
                for i in range(len(islands)):
                    twiss_name="Data/1252_negk3_twiss/twiss.oct="+k+"k3=" +str(strengths[j])+"Qx="+str(qx)+islands[i]+".tfs"
                    twissum_name="Data/1252_negk3_twiss/twissum.oct="+k+"k3=" +str(strengths[j])+"Qx="+str(qx)+islands[i]+".tfs"
                    
                    twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                    twiss=twiss.drop(index=0)
                    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                    
                    twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                    twiss_sum=twiss_sum.drop(index=0,columns='*')
                    
                    data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
                    data.insert(0,"name",k)
                    data.insert(1,"k3",strengths[j])
                    data.insert(2,"Qx",qx)
                    data.insert(3,"island",islands[i])
                    data.insert(4,"ALFX",twiss.ALFX[1])
                    data.insert(4,"BETX",twiss.BETX[1])
                    data.insert(4,"max_X",max(twiss.X))
                    
                    alldata=alldata.append(data)
            
# ,"LOE.32002","LOEN.52002"
# alldata.to_csv("Data/twiss_csv/1252_748top.csv")

#%%1252 pairs
alldata=pd.DataFrame(columns=['name', 'island','k31','k32', 'Qx','max_X','BETX', 'ALFX', 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P', 'ALPHA_C_P2',
        'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])

#%%
alldata= pd.read_csv("Data/twiss_csv/1252_748top.csv")
alldata = alldata.loc[:, ~alldata.columns.isin(['Unnamed: 0'])]
#%%
oct_names=["LOE.12002,LOEN.52002"]

# k31=[-2.6,-2.7,-2.8,-2.9,-3.0 , -3.1, -3.2, -3.3,-3.4,-3.9,-4]
# k32 = [-2.4, -2.3, -2.2, -2.1, -2.0 , -1.9,-1.8, -1.7,-1.6,-1.1,-1]
# Qx=[26.748]
Qx = [26.747]
k31 = [ 0.0 ,  0.0,  0.0 ,  0.0 ,  0.0 , -2.0 , -2.1, -2.2, -2.3, -2.4, -2.6,
       -2.7, -2.8, -2.9, -3.0 ,-3.1, -3.2, -3.3, -3.4, -3.9, -4,-2.1, -0.9, 
       -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

k32 = [-2.0 , -2.1, -2.2, -2.3, -2.4,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0, -2.4,
       -2.3, -2.2, -2.1, -2.0 , -1.9, -1.8, -1.7, -1.6, -1.1, -1, -0.4, -0.9, 
       -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

islands=["bot"]#,"cent"]

#
for k in oct_names:
    for qx in Qx:
            for j in range(len(k31)):
                for i in range(len(islands)):
                    twiss_name="Data/1252_negk3_twiss/twiss.oct="+k+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(qx)+islands[i]+".tfs"
                    twissum_name="Data/1252_negk3_twiss/twissum.oct="+k+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(qx)+islands[i]+".tfs"
                    
                    twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                    twiss=twiss.drop(index=0)
                    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                    
                    twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                    twiss_sum=twiss_sum.drop(index=0,columns='*')
                    
                    data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
                    data.insert(0,"name",k)
                    data.insert(1,"k31",k31[j])
                    data.insert(2,"k32",k32[j])
                    data.insert(2,"Qx",qx)
                    data.insert(3,"island",islands[i])
                    data.insert(4,"ALFX",twiss.ALFX[1])
                    data.insert(4,"BETX",twiss.BETX[1])
                    data.insert(4,"max_X",max(twiss.X))
                    
                    alldata=alldata.append(data)
            
#%%
alldata.to_csv("Data/twiss_csv/1252_747bot.csv")
#%%
Qx = [26.747, 26.748, 26.7485, 26.749, 26.7495]
for qx in Qx:
    smalldata=alldata[alldata["Qx"]==qx]
    plt.scatter(smalldata.ORBIT_X, smalldata.ORBIT_PX)
    fit = np.polyfit(smalldata.ORBIT_X, smalldata.ORBIT_PX,2)
    pfit = np.poly1d(fit)
    plt.plot(smalldata.ORBIT_X, pfit(smalldata.ORBIT_X), label="Qx="+str(qx))
plt.xlabel("FP X")
plt.ylabel("FP PX")
plt.legend()
#%% triplets
oct_names=["LOE.12002,LOE.32002,LOEN.52002","LOE.22002,LOE.32002,LOEN.52002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
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
alldata.to_csv("data/twiss_csv/islands_twiss.csv")