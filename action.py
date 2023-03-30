#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:25:58 2023

@author: sabo4ever
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op

import henon_funcs as fn

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def trig_area(x1, y1, x2, y2, x3, y3):
    # calculate the area using the formula above
    area = 0.5 * abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    return area

#%% 4 islands

island=0   # 0=right, 1= bottom, 2=left, 3=top

no_particles=8
no_turns=8192

folder=["Data/right/","Data/bot/","Data/left/","Data/top/","Data/cent/"]
name=["ptc_twiss_right.tfs","ptc_twiss_bot.tfs","ptc_twiss_left.tfs","ptc_twiss_top.tfs","ptc_twiss_cent.tfs"]
name_sum=["ptc_twiss_summ_right.tfs","ptc_twiss_summ_bot.tfs","ptc_twiss_summ_left.tfs","ptc_twiss_summ_top.tfs","ptc_twiss_summ_cent.tfs"]

twiss=pd.read_fwf(name[island],skiprows=88,infer_nrows=3000)
#twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

twiss_sum=pd.read_fwf(name_sum[island],skiprows=6)
twiss_sum=twiss_sum.drop(index=0,columns='*')

actions=[]
tunes=[]
deltas=[]
for i in range (2,no_particles+1):
    if i <10:
        name = folder[island] + "track.obs0001.p000"+str(i)
    else:   
        name = folder[island] + "track.obs0001.p00"+str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float)
  
    
    plt.figure(num='x')
    x4 = np.array(track.X[::4]) - np.float(twiss_sum.ORBIT_X)
    px4 = np.array(track.PX[::4]) - np.float(twiss_sum.ORBIT_PX)
    
    plt.scatter(x4,px4,marker='.',s=0.1)
    
    xn = x4/np.sqrt(twiss.BETX[1])
    pxn = twiss.ALFX[1] * x4/np.sqrt(twiss.BETX[1]) + px4*np.sqrt(twiss.BETX[1])
    
    plt.scatter(xn,pxn,marker='.',s=0.1)
    
    plt.xlabel("X")
    plt.ylabel("p_X")
    plt.show()
    
    r,theta = cart2pol(x4,px4)
    data = {"theta":theta,"r":r}
    polar = pd.DataFrame(data=data)
    polar = polar.sort_values(by="theta")
    
    x_re = polar.r*np.cos(polar.theta)
    px_re = polar.r*np.sin(polar.theta)
    
    area=0
    for j in range (len(r)-1):
        area += trig_area(0, 0, x_re[j], px_re[j], x_re[j+1], px_re[j+1])
    actions.append(area/(2*np.pi))
    
    Qx=fn.fft_tune(x4,px4,twiss.ALFX[1],twiss.BETX[1])
    tunes.append(Qx)
    deltas.append(track.X[1]-np.float(twiss_sum.ORBIT_X))

plt.figure(num='Qx-J')
plt.scatter(actions,tunes,marker='.', linewidths=0.5)
plt.xlabel("J")
plt.ylabel("Q_x")

param=np.polyfit(actions, tunes, 1)
fit=np.poly1d(param)
xx=np.linspace(actions[0],actions[-1],250)
label="  a1="+str(fit[1])+" a0="+str(fit[0])
plt.plot(xx,fit(xx),label=label)
plt.legend()

plt.figure(num='Qx-delta')
plt.scatter(deltas,tunes,marker='.', linewidths=0.5)
plt.xlabel("delta")
plt.ylabel("Q_x")

    
pfit=op.curve_fit(fn.quad_func,deltas,tunes,p0=[-50,0.008])
xx=np.linspace(deltas[0],deltas[-1],250)
fit=fn.quad_func(xx,*pfit[0])
label="  a2="+str(pfit[0][0])+" a0="+str(pfit[0][1])
    
plt.plot(xx,fit,label=label)
plt.legend()  


#%% central
island=0
no_particles=13
no_turns=2048
folder=["Data/cent/"]
# name=["ptc_twiss_cent.tfs"]
# name_sum=["ptc_twiss_summ_cent.tfs"]

# twiss=pd.read_fwf(name[island],skiprows=88,infer_nrows=3000)
# #twiss=pd.read_fwf("sps.tfs",skiprows=50)
# twiss=twiss.drop(index=0)
# twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

# twiss_sum=pd.read_fwf(name_sum[island],skiprows=6)
# twiss_sum=twiss_sum.drop(index=0,columns='*')

twissname=["Data/twiss_csv/cent_twiss.csv"]

twiss=pd.read_csv(twissname[island])
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.reset_index()
twiss_sum = twiss.iloc[1]

actions=[]
tunes=[]
deltas=[]
for i in range (1,no_particles+1):
    # if i <10:
    #     name = folder[island] + "track.obs0001.p000"+str(i)
    # else:   
    #     name = folder[island] + "track.obs0001.p00"+str(i)
    name = "Data/track75C/track.oct=LOE.22002k3=-0.6no=" + str(i)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float)
  
    
    plt.figure(num='x')
    x4 = np.array(track.X) - np.float(twiss_sum.ORBIT_X)
    px4 = np.array(track.PX) - np.float(twiss_sum.ORBIT_PX)
    
    plt.scatter(x4,px4,marker='.',s=0.1)
    
    xn = x4/np.sqrt(twiss.BETX[1])
    pxn = twiss.ALFX[1] * x4/np.sqrt(twiss.BETX[1]) + px4*np.sqrt(twiss.BETX[1])
    
    plt.scatter(xn,pxn,marker='.',s=0.1)
    
    plt.xlabel("X")
    plt.ylabel("p_X")
    plt.show()
    
    r,theta = cart2pol(x4,px4)
    data = {"theta":theta,"r":r}
    polar = pd.DataFrame(data=data)
    polar = polar.sort_values(by="theta")
    
    x_re = polar.r*np.cos(polar.theta)
    px_re = polar.r*np.sin(polar.theta)
    
    area=0
    for j in range (len(r)-1):
        area += trig_area(0, 0, x_re[j], px_re[j], x_re[j+1], px_re[j+1])
    actions.append(area/(2*np.pi))
    
    Qx=fn.fft_tune(x4,px4,twiss.ALFX[1],twiss.BETX[1])
    tunes.append(Qx)
    deltas.append(track.PX[1]-np.float(twiss_sum.ORBIT_PX))

plt.figure(num='Qx-J')
plt.scatter(actions,tunes,marker='.', linewidths=0.5)
plt.xlabel("J")
plt.ylabel("Q_x")

param=np.polyfit(actions, tunes, 1)
fit=np.poly1d(param)
xx=np.linspace(actions[0],actions[-1],250)
label="  a1="+str(fit[1])+" a0="+str(fit[0])
plt.plot(xx,fit(xx),label=label)
plt.legend()

plt.figure(num='Qx-delta')
plt.scatter(deltas,tunes,marker='.', linewidths=0.5)
plt.xlabel("delta")
plt.ylabel("Q_x")

    
pfit=op.curve_fit(fn.quad_func,deltas,tunes,p0=[-50,0.008])
xx=np.linspace(deltas[0],deltas[-1],250)
fit=fn.quad_func(xx,*pfit[0])
label="  a2="+str(pfit[0][0])+" a0="+str(pfit[0][1])
    
plt.plot(xx,fit,label=label)
plt.legend()  
