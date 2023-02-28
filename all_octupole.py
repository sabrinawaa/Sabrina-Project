#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:51:19 2023

@author: sabo4ever
"""

# from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op

import henon_funcs as fn
from math import log10, floor
def round_sig(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

L_LOD=0.677
L_LOE=0.74
L_LOF=0.705

seq= pd.read_fwf("sps/sps.seq" ,skiprows=188,delimiter=" ")
seq=seq.iloc[0:1912]
names=seq.iloc[:,0]
pos=seq.iloc[:,6]
magtype=seq.iloc[:,2]
data={"name":names, "type":magtype, "S":np.array(pos)}
sps=pd.DataFrame(data=data).astype({'S':'float'})
LODs=sps[sps["type"]=="LOD"].reset_index()
LOFs=sps[sps["type"]=="LOF"].reset_index()
LOEs=sps[sps["type"]=="LOE"].reset_index()

twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)
twiss.S=twiss.S.round(decimals=4)
plt.plot(twiss.S,twiss.DY)

#%%
LODtwiss=pd.DataFrame(columns=twiss.columns)
for i in range (len(LODs.S)):
    if twiss[twiss.S==round(LODs.S[i]+L_LOD/2,4):
            print(twiss.S)
             
    # LODtwiss=LODtwiss.append(twiss[twiss.S==round(LODs.S[i]+L_LOD/2,4)])

#%%
# a=round(LODs.S[3]+L_LOD/2,4)