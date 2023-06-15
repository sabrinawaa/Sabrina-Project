#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:51:19 2023

@author: sabo4ever
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op

import henon_funcs as fn

#%%
mad=Madx()
mad.call("track.madx")
#%%
twiss=pd.read_fwf("sps.tfs",skiprows=50,infer_nrows=3000,delimiter=" ")
#twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
#%%

L_LOD=0.677
L_LOE=0.74
L_LOF=0.705
L_LOEN=0.656

seq= pd.read_fwf("sps/sps.seq" ,infer_nrows=1912,skiprows=186,delimiter='')
seq=seq.iloc[0:1913]
names=seq.iloc[:,0]
pos=seq.iloc[:,6]
magtype=seq.iloc[:,2]
data={"name":names, "type":magtype, "S":np.array(pos)}
sps=pd.DataFrame(data=data).astype({'S':'float'})
LODs=sps[sps["type"]=="LOD"].reset_index()
LOFs=sps[sps["type"]=="LOF"].reset_index()
LOEs=sps[sps["type"]=="LOE"].reset_index()
LOENs=sps[sps["type"]=="LOEN"].reset_index()

twiss=pd.read_fwf("sps.tfs",skiprows=50,infer_nrows=3000,delimiter=" ")
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)
twiss.S=twiss.S.round(decimals=2)


#%%

LODtwiss=pd.DataFrame(columns=["name"]+list(twiss.columns))
for i in range (len(LODs.S)):
    
    LODtwiss=LODtwiss.append(twiss[twiss.S==round(LODs.S[i]+L_LOD/2,2)])
    LODtwiss=LODtwiss.append(twiss[twiss.S==round(LODs.S[i]+L_LOD/2+0.01,2)])
    LODtwiss=LODtwiss.append(twiss[twiss.S==round(LODs.S[i]+L_LOD/2-0.01,2)])
LODtwiss=LODtwiss.reset_index()
LODtwiss.name=LODs.name
LODtwiss.to_csv("LOD.csv",columns=["name","S","BETX","BETY","DX"])
    
LOEtwiss=pd.DataFrame(columns=["name"]+list(twiss.columns))
for i in range (len(LOEs.S)):
    LOEtwiss=LOEtwiss.append(twiss[twiss.S==round(LOEs.S[i]+L_LOE/2,2)])
LOEtwiss=LOEtwiss.reset_index()
LOEtwiss.name=LOEs.name
LOEtwiss.to_csv("LOE.csv",columns=["name","S","BETX","BETY","DX"])

LOENtwiss=pd.DataFrame(columns=["name"]+list(twiss.columns))
for i in range (len(LOENs.S)):
    LOENtwiss=LOENtwiss.append(twiss[twiss.S==round(LOENs.S[i]+L_LOEN/2,2)])
LOENtwiss=LOENtwiss.reset_index()
LOENtwiss.name=LOENs.name
LOENtwiss.to_csv("LOEN.csv",columns=["name","S","BETX","BETY","DX"])
    
LOFtwiss=pd.DataFrame(columns=["name"]+list(twiss.columns))
for i in range (len(LOFs.S)):
    LOFtwiss=LOFtwiss.append(twiss[twiss.S==round(LOFs.S[i]+L_LOF/2,2)])
    LOFtwiss=LOFtwiss.append(twiss[twiss.S==round(LOFs.S[i]+L_LOF/2+0.01,2)])
    LOFtwiss=LOFtwiss.append(twiss[twiss.S==round(LOFs.S[i]+L_LOF/2-0.01,2)])
LOFtwiss=LOFtwiss.reset_index()
LOFtwiss.name=LOFs.name
LOFtwiss.to_csv("LOF.csv",columns=["name","S","BETX","BETY","DX"])

#%%
Oct=pd.DataFrame(columns=LODtwiss.columns)
Oct=Oct.append(LODtwiss).append(LOEtwiss).append(LOENtwiss).append(LOFtwiss)
Oct = Oct.sort_values(by="S")
plt.plot(Oct.name,Oct.BETX,label="beta_h")
plt.plot(Oct.name,Oct.BETY,label="beta_v")
plt.plot(Oct.name,Oct.DX,label="D_h")
plt.xlabel("Octupoles")
plt.xticks(rotation=60, ha='right',fontsize=6)
plt.legend()
plt.grid()

#%% count sextupoles

seq= pd.read_fwf("sps/sps.seq" ,skiprows=189,delimiter=" ")
seq=seq.iloc[0:1911]
names=seq.iloc[:,0]
pos=seq.iloc[:,6]
magtype=seq.iloc[:,2]
data={"name":names, "type":magtype, "S":np.array(pos)}
sps=pd.DataFrame(data=data).astype({'S':'float'})
LSDs=sps[sps["type"]=="LSD"].reset_index()
LSEs=sps[sps["type"]=="LSE"].reset_index()
LSENs=sps[sps["type"]=="LSEN"].reset_index()
LSFs=sps[sps["type"]=="LSF"].reset_index()
