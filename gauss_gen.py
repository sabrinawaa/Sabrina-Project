#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 11:05:23 2023

@author: sawang
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.22002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

twiss_cent = pd.read_csv("Data/twiss_csv/cent_twiss.csv")
twiss_cent = twiss_cent[twiss_cent["k3"]==0.6]
twiss_cent = twiss_cent.iloc[[0]]

 
gauss2d = np.random.normal(0, 0.001, (1000,2))
xn = np.array(gauss2d[:,0])
pxn = np.array(gauss2d[:,1])

x = np.sqrt(float(twiss_cent.BETX)) * xn + float(twiss_FP.ORBIT_X)
px = - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX)) + float(twiss_FP.ORBIT_PX)
plt.scatter(x,px)