#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:14:30 2023

@author: sawang
"""
from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op

import henon_funcs as fn


#%%
oct_names=["LOE.12002,LOE.32002,LOEN.52002","LOE.22002,LOE.32002,LOEN.52002"]
island=0
no_particles=1008
no_turns=2048
folder="Data/square22/"
#%%
twissname=["Data/twiss_csv/cent_twiss.csv"]

twiss=pd.read_csv(twissname[island])
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.iloc[[0]]

xns=[]
tunes=[]
pxns=[]
for i in range (1,no_particles):
    if i <10:
        name=folder+"track.obs0001.p000"+str(i)
    elif 9<i<100:   
        name=folder+"track.obs0001.p00"+str(i)
    elif 99<i<1000:
        name=folder+"track.obs0001.p0"+str(i)
    else:
        name=folder+"track.obs0001.p"+str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    # plt.figure(num='1')
    # x4 = np.array(track.X[1])
    # px4 = np.array(track.PX[1])
    
    # plt.scatter(x4,px4,marker='.',s=1)
  
    
    # plt.figure(num='1')
    x4 = np.array(track.X) - np.float64(twiss.ORBIT_X)
    px4 = np.array(track.PX) - np.float64(twiss.ORBIT_PX)
    
    # plt.scatter(x4,px4,marker='.',s=0.1)
    
    xn = x4/np.sqrt(float(twiss.BETX))
    xns.append(track.X[1])
    pxn =float(twiss.ALFX) * x4/np.sqrt(float(twiss.BETX)) + px4*np.sqrt(float(twiss.BETX))
    pxns.append(track.PX[1])
    
    plt.figure(num="5")
    plt.scatter(xn,pxn,marker='.',s=0.1)
    
    plt.xlabel("X-")
    plt.ylabel("p_X")
    
    
    Qx=fn.fft_tune(x4,px4,float(twiss.ALFX),float(twiss.BETX))
    tunes.append(Qx)
#%%
fig,ax=plt.subplots()



im=ax.scatter(xns,pxns,c=tunes,s=0.1,cmap=plt.cm.jet) 
plt.xlabel("X0")
plt.ylabel("Px0")

fig.colorbar(im, ax=ax)

x0i=[]
px0i=[]
tunei=[]
idx=[]
for a in range(len(xns)):
    if abs(tunes[a]-0.75)<0.000001:
        x0i.append(xns[a])
        px0i.append(pxns[a])
        tunei.append(tunes[a])
        idx.append(a)
        
fig2,ax2=plt.subplots()
for i in range (1,1000,20):
    if i <10:
        name=folder+"track.obs0001.p000"+str(i)
    elif 9<i<100:   
        name=folder+"track.obs0001.p00"+str(i)
    elif 99<i<1000:
        name=folder+"track.obs0001.p0"+str(i)
    else:
        name=folder+"track.obs0001.p"+str(i)    
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    imm=ax2.scatter(track.X,track.PX,marker='.',s=0.01)
    
im2=ax2.scatter(x0i,px0i,c=tunei,s=5,cmap=plt.cm.jet)
plt.xlabel("X0")
plt.ylabel("Px0")

fig.colorbar(im2, ax=ax2)
print("no of points=",len(x0i))
area_tot=(max(track.X)-min(track.X))*(max(track.PX)-min(track.PX))
print("area=",area_tot*len(x0i)/len(xns))

#%%

twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.22002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

for i in [107]:
    if i <10:
        name=folder+"track.obs0001.p000"+str(i)
    elif 9<i<100:   
        name=folder+"track.obs0001.p00"+str(i)
    elif 99<i<1000:
        name=folder+"track.obs0001.p0"+str(i)
    else:
        name=folder+"track.obs0001.p"+str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    x4=track.X[::4]
    px4=track.PX[::4]
    plt.scatter(x4,px4,marker='.',s=0.1)
    plt.scatter(twiss_FP.ORBIT_X,twiss_FP.ORBIT_PX,marker='x',s=10)
    
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def trig_area(x1, y1, x2, y2, x3, y3):
    # calculate the area using the formula above
    area = 0.5 * abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    return area


r,theta = cart2pol(x4,px4)
data = {"theta":theta,"r":r}
polar = pd.DataFrame(data=data)
polar = polar.sort_values(by="theta")

x_re = list(polar.r*np.cos(polar.theta))
px_re = list(polar.r*np.sin(polar.theta))

area=0
trigs=[]
for j in range (len(r)-1):
    area += trig_area(twiss_FP.ORBIT_X,twiss_FP.ORBIT_PX, x_re[j], px_re[j], x_re[j+1], px_re[j+1])
    trigs.append(trig_area(twiss_FP.ORBIT_X,twiss_FP.ORBIT_PX, x_re[j], px_re[j], x_re[j+1], px_re[j+1]))   
    
    
area2=fn.shape_area(twiss_FP.ORBIT_X,twiss_FP.ORBIT_PX, x4, px4)
print("area=",area)
    