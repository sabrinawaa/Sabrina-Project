#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:18:55 2023

@author: sawang
"""
#%%
from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op
from numba import njit
from scipy.integrate import dblquad


import henon_funcs as fn


# def emittance(x,px, w=1):

#     w = np.full(len(x),1)
    
#     mux= np.average(x,weights= w)
#     mupx=np.average(px,weights= w)
    
#     x_sqmean = sum((x-mux)**2*w) /sum(w)
#     px_sqmean = sum((px-mupx)**2 *w) /sum(w)
    
#     xpx_sqmean = ((x-mux).dot(w)*(px-mupx).dot(w)/sum(w))**2
#     return np.sqrt(x_sqmean * px_sqmean -xpx_sqmean)

def emittance_simp(x,px):
    x = x - np.mean(x)
    px = px - np.mean(px)
    x_sqmean = np.mean(x**2) 
    px_sqmean = np.mean(px**2) 
    xpx_sqmean = (np.mean(x * px ))**2
    return np.sqrt(x_sqmean * px_sqmean - xpx_sqmean)
#weight=1 is unweighted 

#%%
twissname="Data/twiss_csv/cent_twiss.csv"

twiss=pd.read_csv(twissname)
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.iloc[[0]]

# twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.32002top_twiss.csv")
# twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]
twiss = pd.DataFrame()
twiss.BETX = 64.33992636
twiss.ALFX = 1.728756478

#%%
no_particles=3000
no_turns=2048
folder="submit/1252gauss_scan_-2.1_747/"
x0=[]
px0=[]
xfin=[]
pxfin=[]
for i in range (1,no_particles):
    name = folder + "track.no=" + str(i)
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    x0.append(track.X[1])
    px0.append(track.PX[1])
    xfin.append(track.X.iloc[-1])
    pxfin.append(track.PX.iloc[-1])
  #%%  
# plt.figure(num="Emittance")
plt.scatter(x0,px0,marker='.',s=0.1, label="initial dist")

# for i in [3253
#           ]:
#     # if i <10:
#     #     name=folder+"track.obs0001.p000"+str(i)
#     # elif 9<i<100:   
#     #     name=folder+"track.obs0001.p00"+str(i)
#     # elif 99<i<1000:
#     #     name=folder+"track.obs0001.p0"+str(i)
#     # else:
#     #     name=folder+"track.obs0001.p"+str(i)
#     # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
#     name =  "Data/SQ32/32track.no=" + str(i+1)
#     track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
#     track = track.drop(index = 0,columns="*")
#     track = track.astype(np.float64)
#     x4 = np.array(track.X[::4])
#     px4 = np.array(track.PX[::4]) 
    
# plt.scatter(x4,px4,marker='.',s=0.1)

plt.xlabel("X0")
plt.ylabel("Px0")
print("emittance before=",emittance_simp(np.array(x0),np.array(px0)))
#%%
plt.figure(num="Emittance")
plt.scatter(xfin,pxfin,marker='.',s=0.1,label="final dist")
# plt.scatter(x4,px4,marker='.',s=0.1)
plt.xlabel("X_fin")
plt.ylabel("Px_fin")
plt.legend()
print("emittance after=",emittance_simp(xfin,pxfin))
#%%

area = 1.24e-6
std = np.sqrt( area *0.05/ np.pi) /3
offset = float(twiss_FP.ORBIT_PX) -0.000065


#%% with huge data set
no_particles = 3000
stds = np.linspace(std*0.25, std*1.75, 10)
offsets = np.linspace(offset - 3.1e-5, offset + 3.1e-5, 10)

std_grid,offs_grid=np.meshgrid(stds,offsets)
std_grid=std_grid.flatten()
offs_grid=offs_grid.flatten()


em_fin=[]
em_increase=[]
idx=[]
std_grid1=[]
offs_grid1=[]
for a in range (len(std_grid)):
    if offs_grid[a] < 0.00038 and offs_grid[a]> 0.00035:
        idx.append(a)
        std_grid1.append(std_grid[a])
        offs_grid1.append(offs_grid[a])
        x0s=[]
        px0s=[]
        x_fins=[]
        px_fins=[]
        foldername = "./submit/32gauss_scan_"+ str(a)
        for i in range (1,no_particles+1):
            name = foldername + "/32track.no=" + str(i)
          
            track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
            track = track.drop(index = 0,columns="*")
            track = track.astype(np.float64)
            
            x0s.append(track.X[1])
            px0s.append(track.PX[1])
            
            x_fins.append(track.X.iloc[-1])
            px_fins.append(track.PX.iloc[-1])
            
        emm_ini= emittance_simp(x0s,px0s)
        emm_fin= emittance_simp(x_fins,px_fins)
        em_fin.append(emm_fin)
        em_increase.append((emm_fin-emm_ini)/emm_ini)

#%%
fig,ax=plt.subplots()

    
    
im=ax.scatter(std_grid1,offs_grid1,c=em_fin,s=10,cmap=plt.cm.jet) 
plt.xlabel("sigma")
plt.ylabel("momentum offset")

fig.colorbar(im, ax=ax, label="final emittance")
#%%
fig2,ax2=plt.subplots()

im2=ax2.scatter(std_grid1,offs_grid1,c=em_increase,s=10,cmap=plt.cm.jet) 
plt.xlabel("sigma")
plt.ylabel("momentum offset")

fig2.colorbar(im2, ax=ax2, label="emittance increase")
        