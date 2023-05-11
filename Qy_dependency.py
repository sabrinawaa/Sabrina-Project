#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:04:39 2023

@author: sawang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'


def normalise (x,px,alf,beta):
    xn = x/np.sqrt(beta)
    pxn = alf * x/np.sqrt(beta) + px * np.sqrt(beta)
    return xn,pxn

def pair_rela (k3s, a, b1, b2, c11,c12,c22):
    k31 = k3s[0]
    k32 = k3s[1]
    return a + b1* k31 +b2*k32 + c11*k31**2 +c12* k31*k32 + c22* k32**2

def plane (dqs,a,b1,b2):
    dq1 = dqs[0]
    dq2 = dqs[1]
    return a + b1* dq1 +b2*dq2

def order3 (k3s, a, b1, b2, c11,c12,c22,d11,d12,d21,d22):
    k31 = k3s[0]
    k32 = k3s[1]
    return a + b1* k31 +b2*k32 + c11*k31**2 +c12* k31*k32 + c22* k32**2 + d11* k31**3 +d12*k31**2*k32 +d21 + d21*k32**2*k31+d22*k32**3

def rmse(expected,observed):
    expected = np.array(expected)
    observed = np.array(observed)
    diff= observed-expected
    return np.sqrt(np.mean(diff**2))
#%%

topdata= pd.read_csv("Data/twiss_csv/2232_-3,-2DQ_-3.12Qy_top.csv").reset_index()
# centdata=pd.read_csv("Data/twiss_csv/1252_DQ_3.12,2after_cent.csv")
# topdata = topdata.drop(index=2)
# topdata = topdata.drop(index=9)
# topdata = topdata.drop(index=22)

plt.scatter(topdata.Qy,topdata.DQ1,s=5,label="DQ1 island")
plt.scatter(topdata.Qy,topdata.DQ2,s=5,label="DQ2 island")
# plt.scatter(topdata.Qy,topdata.GAMMA_TR,s=5,label="GAMMA_TR")

# plt.scatter(centdata.Qy,centdata.DQ1,s=5,label="DQ1 centre")
# plt.scatter(centdata.Qy,centdata.DQ2,s=5,label="DQ2 centre")

plt.xlabel("Qy")
plt.ylabel("DQ")
plt.legend()

# print("order 2 top rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))
# # print("order 3 top rmse =",rmse(order3([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))

#%%
