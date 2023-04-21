#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:44:32 2023

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

twissname="Data/twiss_csv/1252_748cent.csv"

twiss=pd.read_csv(twissname)

twiss=twiss.iloc[[0]]
#%%

botdata= pd.read_csv("Data/twiss_csv/1252_748bot.csv")
topdata= pd.read_csv("Data/twiss_csv/1252_747top.csv")

#%% Island Surface

topdata=topdata.replace(r'^\s*$', np.nan, regex=True)

surfdata = topdata[~topdata["Surface"].isna()]
surfdata['Surface'] = surfdata['Surface'].astype('float64')

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[surfdata.k31, surfdata.k32], surfdata.Surface, p0=p0)


k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(surfdata.k31, surfdata.k32,surfdata.Surface)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Island Surface', fontweight ='bold')
ax.legend()
#%% Mom compaction
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")



p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.ALPHA_C, p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.ALPHA_C, p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,topdata.ALPHA_C)
ax.scatter3D(k31,k32,np.full(len(k31),twiss.ALPHA_C),label='centre')
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Momentum Compaction', fontweight ='bold')
ax.legend()

#%% Transition Energy
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

def energy_tr (gamma_tr):
    gamma_tr = np.array(gamma_tr)
    return 938.2720813*gamma_tr

p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], energy_tr(topdata.GAMMA_TR), p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], energy_tr(botdata.GAMMA_TR), p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
# ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,energy_tr(topdata.GAMMA_TR))
ax.scatter3D(k31,k32,np.full(len(k31),energy_tr(twiss.GAMMA_TR)),label='centre')
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Transition Energy (MeV)', fontweight ='bold')
ax.legend()

#%% alfx
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")



p0= [2.5,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.ALFX, p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.ALFX, p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()

ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,topdata.ALFX)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('ALFX', fontweight ='bold')
ax.legend()


#%%  betx
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")


p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.BETX, p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.BETX, p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,topdata.BETX)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('BETX', fontweight ='bold')
ax.legend()

#%% amplitude
def amp (x,px,alf,beta):
    x = np.array(x)
    px = np.array(px)
    xn,pxn = normalise(x, px, float(alf), float(beta))
    return xn**2 + pxn**2

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")


p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], amp(topdata.ORBIT_X,topdata.ORBIT_PX,twiss.ALFX,twiss.BETX), p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,amp(topdata.ORBIT_X,topdata.ORBIT_PX,twiss.ALFX,twiss.BETX))
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Normalised Amplitude', fontweight ='bold')
ax.legend()

#%% ORBIT_X
k31,k32 = np.meshgrid(k31s,k32s)

fig = go.Figure(data=[
    go.Surface(z=np.array(pair_rela([k31,k32],*top_fit[0])),x=k31,y=k32,name='Top'),
    go.Surface(z=np.array(pair_rela([k31,k32],*bot_fit[0])),x=k31,y=k32,name='Bot'),
    go.Surface(z=np.zeros_like(k31),x=k31,y=k32,name='X=0')
               ])

fig.update_layout(title='3D Surface Plot',
                  scene=dict(xaxis_title='k31', yaxis_title='k32', zaxis_title='ORBIT_X'),
                  legend=dict(title='Surfaces'))

fig.show()
#%% X
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")


p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], np.array(topdata.ORBIT_X), p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], np.array(botdata.ORBIT_X), p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,np.full(len(k31),0.0),label="x=0")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,np.array(topdata.ORBIT_X))
ax.scatter3D(botdata.k31, botdata.k32,np.array(botdata.ORBIT_X))
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('ORBIT_X', fontweight ='bold')
ax.legend()

#%%DQ
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")


p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.DQ2, p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.DQ2, p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="Qx=748")
ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="Qx=747")
ax.scatter3D(topdata.k31, topdata.k32,topdata.DQ2)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('DQ2', fontweight ='bold')
ax.legend()



