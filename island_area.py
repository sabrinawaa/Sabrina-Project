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
no_particles=7774
no_turns=2048
folder="Data/SQ32/"
#%%
twissname=["Data/twiss_csv/cent_twiss.csv"]

twiss=pd.read_csv(twissname[island])
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.iloc[[0]]
#%%
xns=[]
tunes=[]
pxns=[]
for i in range (1,no_particles+1):
    # if i <10:
    #     name=folder+"track.obs0001.p000"+str(i)
    # elif 9<i<100:   
    #     name=folder+"track.obs0001.p00"+str(i)
    # elif 99<i<1000:
    #     name=folder+"track.obs0001.p0"+str(i)
    # else:
    #     name=folder+"track.obs0001.p"+str(i)
    name = folder + "32track.no=" + str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)

  
    
    # plt.figure(num='1')
    x4 = np.array(track.X) - np.float64(twiss.ORBIT_X)
    px4 = np.array(track.PX) - np.float64(twiss.ORBIT_PX)
    
    # plt.scatter(x4,px4,marker='.',s=0.1)
    
    
    xns.append(track.X[1])
   
    pxns.append(track.PX[1])
    
    
    
    
    
    Qx=fn.fft_tune(x4,px4,float(twiss.ALFX),float(twiss.BETX))
    tunes.append(Qx)
    
   
    
#%%
fig,ax=plt.subplots()



im=ax.scatter(xns,pxns,c=tunes,s=0.1,cmap=plt.cm.jet) 
plt.xlabel("X0")
plt.ylabel("Px0")

fig.colorbar(im, ax=ax)

#%%
x0i=[]
px0i=[]
tunei=[]
for a in range(len(xns)):
     if abs(tunes[a]-0.75)<1.9571954692570003e-05:
         x0i.append(xns[a])
         px0i.append(pxns[a])
         tunei.append(tunes[a])
         
fig2,ax2=plt.subplots()
for i in range (1,7774,500):
    # if i <10:
    #     name=folder+"track.obs0001.p000"+str(i)
    # elif 9<i<100:   
    #     name=folder+"track.obs0001.p00"+str(i)
    # elif 99<i<1000:
    #     name=folder+"track.obs0001.p0"+str(i)
    # else:
    #     name=folder+"track.obs0001.p"+str(i)    
    name = folder + "32track.no=" + str(i)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    # imm=ax2.scatter(track.X,track.PX,marker='.',s=0.01)
    
im2=ax2.scatter(x0i,px0i,s=1,c=tunei,cmap=plt.cm.jet)

plt.xlabel("X0")
plt.ylabel("Px0")


fig.colorbar(im2, ax=ax2)

#%%
x0is=[]
px0is=[]
tuneis=[]
for b in range (len(x0i)):
    if x0i[b]<0.01444 and x0i[b]>-0.01718:
        x0is.append(x0i[b])
        px0is.append(px0i[b])
        tuneis.append(tunei[b])
        
fig3,ax3=plt.subplots()
im3=ax3.scatter(x0is,px0is,c=tuneis,s=1,cmap=plt.cm.jet)
plt.xlabel("X0")
plt.ylabel("Px0")
fig.colorbar(im3, ax=ax3)     

#%%
xns=np.array(xns)
pxns=np.array(pxns)
xn = xns/np.sqrt(float(twiss.BETX))   
pxn =np.float(twiss.ALFX) * xns/np.sqrt(float(twiss.BETX)) + pxns*np.sqrt(float(twiss.BETX))
plt.scatter(xn,pxn)

print("no of points=",len(x0is))
area_tot=(max(xn)-min(xn))*(max(pxn)-min(pxn))
print("area=",area_tot*(len(x0is))/len(xn))
#%%
area=[]
tol=np.linspace(0.00000,0.001,100)
for t in tol:
    x0i=[]
    px0i=[]
    tunei=[]
    for a in range(len(xns)):
         if abs(tunes[a]-0.75)<t:
             x0i.append(xns[a])
             px0i.append(pxns[a])
             tunei.append(tunes[a])
    x0is=[]
    px0is=[]
    tuneis=[]
    for b in range (len(x0i)):
        if x0i[b]<0.01444 and x0i[b]>-0.01718:
            x0is.append(x0i[b])
            px0is.append(px0i[b])
            tuneis.append(tunei[b])
            
    area.append(area_tot*(len(x0is))/len(xns))
    
plt.scatter(x0is,px0is,c=tuneis,s=5,cmap=plt.cm.jet)
plt.figure()   
plt.scatter(tol,area,marker='x',s=1)        
plt.ylabel('area')
plt.xlabel('tolerance')

 #%% find separatrix
idx=[]
for a in range(len(xns)):
     if abs(tunes[a]-0.75)<0.0000186 and abs(tunes[a]-0.75)>0.0000185:
         idx.append(a)
         
for i in idx:
    # if i <10:
    #     name=folder+"track.obs0001.p000"+str(i)
    # elif 9<i<100:   
    #     name=folder+"track.obs0001.p00"+str(i)
    # elif 99<i<1000:
    #     name=folder+"track.obs0001.p0"+str(i)
    # else:
    #     name=folder+"track.obs0001.p"+str(i) 
    
    name = folder + "32track.no=" + str(i+1)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)        
        
    plt.scatter(track.X,track.PX,marker='.',s=0.1)
    plt.scatter(0,0,marker='x',s=10) 
     


#%%

twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.32002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

for i in [3253
          ]:
    # if i <10:
    #     name=folder+"track.obs0001.p000"+str(i)
    # elif 9<i<100:   
    #     name=folder+"track.obs0001.p00"+str(i)
    # elif 99<i<1000:
    #     name=folder+"track.obs0001.p0"+str(i)
    # else:
    #     name=folder+"track.obs0001.p"+str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    name = folder + "32track.no=" + str(i+1)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)

    x4 = np.array(track.X[::4]) - float(twiss_FP.ORBIT_X)
    px4 = np.array(track.PX[::4]) - float(twiss_FP.ORBIT_PX)
    
    plt.scatter(x4,px4,marker='.',s=0.1)
    plt.scatter(x4[0],px4[0],marker='x',s=10) 
    
    
area2=fn.shape_area(x4, px4)
print("area=",area2)
print("ini cond of separatrix=",track.X[1],track.PX[1])
print("tune=", fn.fft_tune(np.array(track.X), np.array(track.PX), float(twiss.ALFX),float(twiss.BETX)))

#%%
turns=np.arange(1000,20001,1000)
areas=[]
for k in turns:
    name="Data/test_no_turns/32track.turn="+str(k)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    plt.scatter(x0is,px0is,c=tuneis,s=5,cmap=plt.cm.jet)
    x4 = np.array(track.X[::4]) - float(twiss_FP.ORBIT_X)
    px4 = np.array(track.PX[::4]) - float(twiss_FP.ORBIT_PX)
    
    areas.append(fn.shape_area(x4, px4))
    plt.scatter(x4,px4,marker='.',s=0.1)
    plt.scatter(-0.0172,0.000708,marker='x',s=10)

plt.figure()
plt.scatter(turns, areas, s=1, marker='x')    
plt.xlabel("no_turns")
plt.ylabel("Area")