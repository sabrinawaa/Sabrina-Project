#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 11:52:37 2023

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

# twissname="Data/twiss_csv/1252_748cent.csv"

# twiss=pd.read_csv(twissname)

# twiss=twiss.iloc[[0]]

topdata= pd.read_csv("Data/twiss_csv/1252_-1.08,-0.85DQ_top.csv")
# topdata = topdata[topdata.DQ1<1000]

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001,0,0,0,0]
DQ1_fit = curve_fit(pair_rela,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ1, p0=p0[:6])
DQ2_fit = curve_fit(pair_rela,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ2, p0=p0[:6])
# DQ1_fit = curve_fit(order3,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ1, p0=p0)
# DQ2_fit = curve_fit(order3,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ2, p0=p0)
# top_fit_plane = curve_fit(plane,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ1, p0=[14,-12,-2])

# DQ1_fit = curve_fit(pair_rela,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.ORBIT_X, p0=p0)


dq1s = np.linspace(-4,-0.005,50)
dq2s = dq1s

dq1,dq2 = np.meshgrid(dq1s,dq2s)
dq11 = dq1.flatten()
dq21 = dq2.flatten()

dq1s = np.linspace(0.005,5,50)
dq2s = dq1s

dq1,dq2 = np.meshgrid(dq1s,dq2s)
dq12 = dq1.flatten()
dq22 = dq2.flatten()

dq1 = np.concatenate((dq11,dq12))
dq2 = np.concatenate(((dq21,dq22)))

ax.scatter3D(dq1, dq2,pair_rela([dq1,dq2],*DQ1_fit[0]),label="Island DQ1")
ax.scatter3D(dq1, dq2,pair_rela([dq1,dq2],*DQ2_fit[0]),label="Island DQ2")

# ax.scatter3D(dq1, dq2,order3([dq1,dq2],*DQ1_fit[0]),label="Island DQ1")
# ax.scatter3D(dq1, dq2,order3([dq1,dq2],*DQ2_fit[0]),label="Island DQ2")

ax.scatter3D(dq1, dq2,np.full(len(dq1),0),label="0")
ax.scatter3D(topdata.cent_DQ1, topdata.cent_DQ2,topdata.DQ1)
ax.scatter3D(topdata.cent_DQ1, topdata.cent_DQ2,topdata.DQ2)
ax.set_xlabel('centre DQ1', fontweight ='bold')
ax.set_ylabel('centre DQ2', fontweight ='bold')
ax.set_zlabel('Island DQ', fontweight ='bold')
ax.legend()

print("order 2 top rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))
# print("order 3 top rmse =",rmse(order3([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))

#%%
dq11,dq21 = np.meshgrid(np.linspace(-4,-0.005,50),np.linspace(-4,-0.005,50))
dq12,dq22 = np.meshgrid(np.linspace(0.005,5,50),np.linspace(0.005,5,50))

fig = go.Figure(data=[
    go.Surface(z=np.array(pair_rela([dq11,dq21],*DQ1_fit[0])),x=dq11,y=dq21,name='Island DQ1'),
    go.Surface(z=np.array(pair_rela([dq11,dq21],*DQ2_fit[0])),x=dq11,y=dq21,name='Island DQ2'),
    
    go.Surface(z=np.array(pair_rela([dq12,dq22],*DQ1_fit[0])),x=dq12,y=dq22,name='Island DQ1'),
    go.Surface(z=np.array(pair_rela([dq12,dq22],*DQ2_fit[0])),x=dq12,y=dq22,name='Island DQ2'),
    #order3----------------------------------------
    
    # go.Surface(z=np.array(order3([dq11,dq21],*DQ1_fit[0])),x=dq11,y=dq21,name='Island DQ1'),
    # go.Surface(z=np.array(order3([dq11,dq21],*DQ2_fit[0])),x=dq11,y=dq21,name='Island DQ2'),
    
    # go.Surface(z=np.array(order3([dq12,dq22],*DQ1_fit[0])),x=dq12,y=dq22,name='Island DQ1'),
    # go.Surface(z=np.array(order3([dq12,dq22],*DQ2_fit[0])),x=dq12,y=dq22,name='Island DQ2'),
    
    go.Surface(z=np.zeros_like(dq11),x=dq11,y=dq21,name='X=0'),
    go.Surface(z=np.zeros_like(dq12),x=dq12,y=dq22,name='X=0')
               ])

fig.update_layout(title='3D Surface Plot',
                  scene=dict(xaxis_title='centre DQ1', yaxis_title='centre DQ2', zaxis_title='DQ1'),
                  legend=dict(title='Surfaces'))

fig.show()

#%% gamma tr dependency
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
DQ1_fit = curve_fit(pair_rela,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.GAMMA_TR, p0=p0)
# DQ2_fit = curve_fit(pair_rela,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ2, p0=p0)
# top_fit_plane = curve_fit(plane,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.DQ1, p0=[14,-12,-2])

# DQ1_fit = curve_fit(pair_rela,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.ORBIT_X, p0=p0)


dq1s = np.linspace(-4,-0.005,50)
dq2s = dq1s

dq1,dq2 = np.meshgrid(dq1s,dq2s)
dq11 = dq1.flatten()
dq21 = dq2.flatten()

dq1s = np.linspace(0.005,5,50)
dq2s = dq1s

dq1,dq2 = np.meshgrid(dq1s,dq2s)
dq12 = dq1.flatten()
dq22 = dq2.flatten()



dq1 = np.concatenate((dq11,dq12))
dq2 = np.concatenate(((dq21,dq22)))
ax.scatter3D(dq1, dq2,pair_rela([dq1,dq2],*DQ1_fit[0]),label="gamma_Tr")
# ax.scatter3D(dq1, dq2,pair_rela([dq1,dq2],*DQ2_fit[0]),label="Island DQ2")
# ax.scatter3D(dq1, dq2,np.full(len(dq1),0),label="0")
ax.scatter3D(topdata.cent_DQ1, topdata.cent_DQ2,topdata.GAMMA_TR)
# ax.scatter3D(topdata.cent_DQ1, topdata.cent_DQ2,topdata.DQ2)
ax.set_xlabel('centre DQ1', fontweight ='bold')
ax.set_ylabel('centre DQ2', fontweight ='bold')
ax.set_zlabel('Island gamma_tr', fontweight ='bold')
ax.legend()

print("order 2 top rmse =",rmse(pair_rela([topdata.cent_DQ1, topdata.cent_DQ2],*DQ1_fit[0]),topdata.GAMMA_TR))

DQ1_fit = curve_fit(order3,[topdata.cent_DQ1, topdata.cent_DQ2], topdata.GAMMA_TR, p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001,0,0,0,0])
ax.scatter3D(dq1, dq2,order3([dq1,dq2],*DQ1_fit[0]),label="order3")
print("order 3 top rmse =",rmse(order3([topdata.cent_DQ1, topdata.cent_DQ2],*DQ1_fit[0]),topdata.GAMMA_TR))

#%%
DQ1data= topdata[topdata.cent_DQ2==1]
plt.scatter(DQ1data.cent_DQ1,DQ1data.DQ1,label="DQ1",s=5)
plt.scatter(DQ1data.cent_DQ1,DQ1data.DQ2,label="DQ2",s=5)
fit = np.polyfit(DQ1data.cent_DQ1, DQ1data.DQ1,1)
fit2 = np.polyfit(DQ1data.cent_DQ1, DQ1data.DQ2,1)
pfit = np.poly1d(fit)
pfit2 = np.poly1d(fit2)
DQ11 = np.linspace(DQ1data.cent_DQ1.iloc[0],DQ1data.cent_DQ1.iloc[-1],100)
plt.plot(DQ11, pfit(DQ11))
plt.plot(DQ11, pfit2(DQ11))
plt.legend()