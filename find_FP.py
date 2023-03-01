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

oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.3,0.1,0.5,0.6,0.7,0.8,0.9]
no_particles=8
no_turns=1024


twiss=pd.read_fwf('sps.tfs',skiprows=50,infer_nrows=3000)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)

for k in oct_names:
    for j in strengths:
        for i in range (2,no_particles+1):
            
            name="Data/track301/track.oct="+str(k)+"k3=" +str(j)+"no="+str(i)
            track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
            track = track.drop(index = 0,columns="*")
            track = track.astype(np.float)
            
            plt.figure(num=k)
            plt.scatter(track.X,track.PX,marker='.',s=0.1)
            plt.xlabel("X")
            plt.ylabel("p_X")
           
        
       
        
   