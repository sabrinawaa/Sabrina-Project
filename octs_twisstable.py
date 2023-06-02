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

oct_names=["LOE.12002,LOE.22002","LOE.22002,LOE.32002","LOE.12002,LOE.32002","LOE.22002,LOEN.52002","LOE.32002,LOEN.52002"]
strengths=[-1.8, 1.8]
Qx=[26.747]
islands=["cent"]#,"bot"]

alldata=pd.DataFrame(columns=['name', 'island','k3', 'Qx','max_X','BETX', 'ALFX', 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P', 'ALPHA_C_P2',
        'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])
for k in oct_names:
    for qx in Qx:
            for j in range(len(strengths)):
                for i in range(len(islands)):
                    twiss_name="Data/pair_twiss_cent/twiss.oct="+k+"k3=" +str(strengths[j])+"Qx="+str(qx)+islands[i]+".tfs"
                    twissum_name="Data/pair_twiss_cent/twissum.oct="+k+"k3=" +str(strengths[j])+"Qx="+str(qx)+islands[i]+".tfs"
                    
                    twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                    twiss=twiss.drop(index=0)
                    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                    
                    twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                    twiss_sum=twiss_sum.drop(index=0,columns='*')
                    
                    data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
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

#%%empty dataframe
alldata=pd.DataFrame(columns=['name', 'island','k31','k32', 'Qx','max_X','BETX', 'ALFX', 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P', 'ALPHA_C_P2',
        'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])

#%%read in existing csv
alldata= pd.read_csv("Data/twiss_csv/1252_csv/1252Qx_26.7495_DQ_3,0.005top.csv")
alldata = alldata.loc[:, ~alldata.columns.isin(['Unnamed: 0'])]
# alldata1=alldata1.iloc[37:]
#%%
alldata=alldata.drop(index=38)
alldata=alldata.drop(index=42)
#%%
oct_names=["LOE.12002,LOEN.52002"]

# k31=[-2.6,-2.7,-2.8,-2.9,-3.0 , -3.1, -3.2, -3.3,-3.4,-3.9,-4]
# k32 = [-2.4, -2.3, -2.2, -2.1, -2.0 , -1.9,-1.8, -1.7,-1.6,-1.1,-1]
# Qx=[26.748]
Qx = [26.749]
k31 = [ 0.0 ,  0.0,  0.0 ,  0.0 ,  0.0 , -2.0 , -2.1, -2.2, -2.3, -2.4,-2.6, -2.7, -2.8, -2.9, -3.0,  
-3.1, -3.2, -3.3, -3.4, -3.9, -4,-2.1, -0.9, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

k32 = [-2.0 , -2.1, -2.2, -2.3, -2.4,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0,-2.4, -2.3, -2.2, -2.1, -2.0 , 
           -1.9, -1.8, -1.7, -1.6, -1.1, -1, -0.4,-0.9, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

islands=["top"]#,"cent"]

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
            
#%%select if in right island
# alldata= alldata[alldata.ORBIT_PX>0.0]
alldata= alldata[abs(alldata.ORBIT_X)<0.011]
alldata= alldata[abs(alldata.ORBIT_PX)>1e-10]
# alldata1 = alldata

#%%
# alldata.to_csv("Data/twiss_csv/1252_csv/1252_Qx_26.7495_DQ_-2,-0.005top.csv")
alldata.to_csv("Data/twiss_csv/fin_config.csv")
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

#%%DQ changing
# alldata=pd.DataFrame(columns=['name', 'island','k31','k32','cent_DQ1','cent_DQ2','Qx','max_X','BETX', 'ALFX', 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P', 'ALPHA_C_P2',
#         'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])

oct_names=["LOE.12002,LOEN.52002"]





Qx = [26.747]

k31=[    -1.957]
k32=[     -2.918]  

# k31 = [  -0.4, -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7]
  

# k32 = [ -0.4, -0.7, -0.7, -0.7, -0.7, -0.7, -0.7, 
#         -1.1, -1.1, -1.1, -1.1, -1.1, -1.1, 
#         -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, 
#         -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, 
#         -2.3, -2.3, -2.3, -2.3, -2.3, -2.3, 
#         -2.7, -2.7, -2.7, -2.7, -2.7, -2.7]
# k31 = [-0.4, -0.7, -1. , -1.3, -1.6, -1.9, -2.2, -0.4, -0.7, -1. , -1.3,
#         -1.6, -1.9, -2.2, -0.4, -0.7, -1. , -1.3, -1.6, -1.9, -2.2, -0.4,
#         -0.7, -1. , -1.3, -1.6, -1.9, -2.2, -0.4, -0.7, -1. , -1.3, -1.6,
#         -1.9, -2.2, -0.4, -0.7, -1. , -1.3, -1.6, -1.9, -2.2, -0.4, -0.7,
#         -1. , -1.3, -1.6, -1.9, -2.2]

# k32 = [-0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.7, -0.7, -0.7, -0.7,
#         -0.7, -0.7, -0.7, -1. , -1. , -1. , -1. , -1. , -1. , -1. , -1.3,
#         -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.6, -1.6, -1.6, -1.6, -1.6,
#         -1.6, -1.6, -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, -2.2, -2.2,
#         -2.2, -2.2, -2.2, -2.2, -2.2]

# k31 = [0.4, 0.7, 1. , 1.3, 1.6, 1.9, 2.2, 0.4, 0.7, 1. , 1.3, 1.6, 1.9,
#        2.2, 0.4, 0.7, 1. , 1.3, 1.6, 1.9, 2.2, 0.4, 0.7, 1. , 1.3, 1.6,
#        1.9, 2.2, 0.4, 0.7, 1. , 1.3, 1.6, 1.9, 2.2, 0.4, 0.7, 1. , 1.3,
#        1.6, 1.9, 2.2, 0.4, 0.7, 1. , 1.3, 1.6, 1.9, 2.2]

# k32 = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7,
#        0.7, 1. , 1. , 1. , 1. , 1. , 1. , 1. , 1.3, 1.3, 1.3, 1.3, 1.3,
#        1.3, 1.3, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.9, 1.9, 1.9, 1.9,
#        1.9, 1.9, 1.9, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2]



# DQ1 = [1, 1, 1, 1, 1, 1, 1, 1]
# DQ2 = [ 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]

#[-2.0 , -2.1, -2.2, -2.3, -2.4,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0,2.4, -2.3, -2.2, -2.1, -2.0 , 
# -1.9, -1.8, -1.7, -1.6, -1.1, -1, -1.3, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

DQ1 = [3]#[1,2,3,4,5,1,1,1,1,-1,-2,-3,-4,-1,-1,-1,2,3,4,-2,-3,-4,0.3]
DQ2 = [0.005]#[1,1,1,1,1,2,3,4,5,-1,-1,-1,-1,-2,-3,-4,2,3,4,-2,-3,-4,0.1]

islands=["top"]#,"cent"]
folder="./"
# folder = "Data/1252DQ_"+str(DQ1[0])+","+str(DQ2[0])+"_twiss/"


#
for k in oct_names:
    for qx in Qx:
            for j in range(len(k31)):
                for dq_idx in range (len(DQ1)):
                    for i in range(len(islands)):
                        twiss_name=folder+"twiss.oct="+k+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(qx)+"DQ="+str(DQ1[dq_idx])+','+str(DQ2[dq_idx])+islands[i]+".tfs"
                        twissum_name=folder+"twissum.oct="+k+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(qx)+"DQ="+str(DQ1[dq_idx])+','+str(DQ2[dq_idx])+islands[i]+".tfs"
                        
                        twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                        twiss=twiss.drop(index=0)
                        twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                        
                        twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                        twiss_sum=twiss_sum.drop(index=0,columns='*')
                        
                        data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
                        data.insert(0,"name",k)
                        data.insert(1,"k31",k31[j])
                        data.insert(2,"k32",k32[j])
                        data.insert(2,"cent_DQ1",DQ1[dq_idx])
                        data.insert(2,"cent_DQ2",DQ2[dq_idx])
                        data.insert(2,"Qx",qx)
                        data.insert(3,"island",islands[i])
                        data.insert(4,"ALFX",twiss.ALFX[1])
                        data.insert(4,"BETX",twiss.BETX[1])
                        data.insert(4,"max_X",max(twiss.X))
                        
                        alldata=alldata.append(data)
                        
#%%CHANGE qy
# alldata=pd.DataFrame(columns=['name', 'island','k31','k32','cent_DQ1','cent_DQ2','Qx',"Qy",'max_X','BETX', 'ALFX', 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P', 'ALPHA_C_P2',
#         'ALPHA_C_P3', 'DQ1', 'DQ2','ORBIT_X','ORBIT_PX'])

oct_names=["LOE.22002,LOE.32002"]
Qx = [26.7495]

k31 = [-3] 


k32 = [-2] 

DQ1 = [-3.12]#[1,2,3,4,5,1,1,1,1,-1,-2,-3,-4,-1,-1,-1,2,3,4,-2,-3,-4]
DQ2 = [-3.12]#[1,1,1,1,1,2,3,4,5,-1,-1,-1,-1,-2,-3,-4,2,3,4,-2,-3,-4]
oct1="LOE.22002"
oct2="LOE.32002"
Qy = [26.81,26.82,26.83,26.84]

islands=["top"]#,"cent"]

#
for k in oct_names:
    for qx in Qx:
        for qy in Qy:
            for j in range(len(k31)):
                for dq_idx in range (len(DQ1)):
                    for i in range(len(islands)):
                        twiss_name="Data/2232_twiss_Qy/twiss.oct="+k+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(qx)+"Qy="+str(qy)+"DQ="+str(DQ1[dq_idx])+','+str(DQ2[dq_idx])+islands[i]+".tfs"
                        twissum_name="Data/2232_twiss_Qy/twissum.oct="+k+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(qx)+"Qy="+str(qy)+"DQ="+str(DQ1[dq_idx])+','+str(DQ2[dq_idx])+islands[i]+".tfs"
                        
                        twiss=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
                        twiss=twiss.drop(index=0)
                        twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
                        
                        twiss_sum=pd.read_fwf(twissum_name,skiprows=6)
                        twiss_sum=twiss_sum.drop(index=0,columns='*')
                        
                        data=twiss_sum.loc[:,twiss_sum.columns.isin([ 'ALPHA_C','GAMMA_TR', 'ALPHA_C_P','ALPHA_C_P2','ALPHA_C_P3','DQ1','DQ2','ORBIT_X','ORBIT_PX'])].astype(np.float64)
                        data.insert(0,"name",k)
                        data.insert(1,"k31",k31[j])
                        data.insert(2,"k32",k32[j])
                        data.insert(2,"cent_DQ1",DQ1[dq_idx])
                        data.insert(2,"cent_DQ2",DQ2[dq_idx])
                        data.insert(2,"Qx",qx)
                        data.insert(2,"Qy",qy)
                        data.insert(3,"island",islands[i])
                        data.insert(4,"ALFX",twiss.ALFX[1])
                        data.insert(4,"BETX",twiss.BETX[1])
                        data.insert(4,"max_X",max(twiss.X))
                        
                        alldata=alldata.append(data)
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