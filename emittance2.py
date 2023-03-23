#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:33:41 2023

@author: sawang
"""
from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op
from numba import njit
from scipy.integrate import dblquad
from scipy.integrate import trapezoid


import henon_funcs as fn


def emittance(x,px, w=1):

    w = np.array(w)
    
    mux= np.average(x,weights= w)
    mupx=np.average(px,weights= w)
    
    x_sqmean = np.power(x-mux,2).dot(w) /sum(w)
    px_sqmean = np.power(px-mupx,2).dot(w) /sum(w)
    
    xpx_sqmean = ((x-mux).dot(w)*(px-mupx).dot(w)/sum(w))**2
    return np.sqrt(x_sqmean * px_sqmean -xpx_sqmean)



#weight=1 is unweighted 

@njit
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))) / (sig * np.sqrt(2*np.pi))

twissname="Data/twiss_csv/cent_twiss.csv"

twiss=pd.read_csv(twissname)
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.iloc[[0]]

twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.32002top_twiss.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

area = 1.24e-6
std = np.sqrt( area *0.05/ np.pi) /3
offset = 0.003

#%% using square gridsqmean * px_sqmean -xpx_sqmean)
no_particles=7774
no_turns=2048
folder="Data/SQ32/"
stds = np.linspace(std*0.25, std*1.75, 50)
offsets = np.linspace(offset - 0.0005, offset + 0.0003, 50)

std_grid,offs_grid=np.meshgrid(stds,offsets)
std_grid=std_grid.flatten()
offs_grid=offs_grid.flatten()
#%%

x0s=[]
px0s=[]
x_fins=[]
px_fins=[]
for i in range (1,no_particles+1):

    name = folder + "32track.no=" + str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    x0s.append(track.X[1])
    px0s.append(track.PX[1])
    
    x_fins.append(track.X.iloc[-1])
    px_fins.append(track.PX.iloc[-1])
#%%
delta_xn = 1.7726e-5
delta_pxn = 9.58e-5
emm_grid = []

emm_inis =[]
xn0 = np.array(x0s)/np.sqrt(float(twiss.BETX))
pxn0 = float(twiss.ALFX) * np.array(x0s) /np.sqrt(float(twiss.BETX)) + np.array(px0s)*np.sqrt(float(twiss.BETX))

xn_fin = np.array(x_fins)/np.sqrt(float(twiss.BETX))
pxn_fin = float(twiss.ALFX) * np.array(x_fins)/np.sqrt(float(twiss.BETX)) + np.array(px_fins)*np.sqrt(float(twiss.BETX))

for i in range (len(std_grid)):
    weights = []
    for j in range (len(xn0)):
        # gauss_func = lambda xn, pxn: (np.exp(-xn**2/(2*std_grid[i]**2)) 
        #                * np.exp(-(pxn-offs_grid[i])**2/(2*std_grid[i]**2)) 
        #                /(std_grid[i]**2 * 2* np.pi))
        # weighti = dblquad(gauss_func, pxn0[j]-delta_pxn/2, pxn0[j]+delta_pxn/2, 
                         # xn0[j]-delta_xn/2, xn0[j]+delta_pxn/2)
        weighti = gaussian(xn0[j],0,std_grid[i]) * delta_xn * gaussian (pxn0[j],offs_grid[i],std_grid[i]) * delta_pxn

    
        weights.append(weighti)
        
    emm_ini =  emittance(np.array(xn0), np.array(pxn0),weights)
    emm_fin = emittance(np.array(xn_fin), np.array(pxn_fin),weights)
    emm_grid.append(emm_fin)
    emm_inis.append(emm_ini)
    print(i)
#%%        
plt.scatter(std_grid,offs_grid,c=emm_grid,s=10,cmap=plt.cm.jet)
plt.colorbar(label="final emittance")
plt.xlabel("sigma")
plt.ylabel("momentum offset")
#%%
plt.scatter(std_grid,offs_grid,c=emm_inis,s=10,cmap=plt.cm.jet)
plt.colorbar(label="initial emittance")
plt.xlabel("sigma")
plt.ylabel("momentum offset")

#%%
emm_inc = (np.array(emm_grid)-np.array(emm_inis))/np.array(emm_inis)
plt.scatter(std_grid,offs_grid,c=emm_inc,s=10,cmap=plt.cm.jet)
plt.colorbar(label="emittance growth")
plt.xlabel("sigma")
plt.ylabel("momentum offset")
#%%
plt.scatter(xn_fin,pxn_fin,c=weighti,s=5,cmap=plt.cm.jet)
plt.colorbar(label="weights")
plt.xlabel("xn")
plt.ylabel("pxn")

#%%
plt.scatter(std_grid, emm_inis,s=1)
plt.xlabel("sigma")
plt.ylabel("emmittance")
#%%
plt.scatter(xn0,delta_xn*gaussian(xn0,0,std_grid[i]))
plt.xlabel("xn0")
plt.ylabel("x_weights")
plt.figure()
plt.scatter(pxn0, delta_pxn*gaussian(pxn0,offs_grid[i],std_grid[i]))
plt.xlabel("pxn0")
plt.ylabel("px_weights")
#%%
weight = np.array(weights)

x = np.array(xn0) 
px = np.array(pxn0)

mux= np.average(xn0,weights= weights)
muy=np.average(pxn0,weights= weights)

x_sqmean = np.power(x-mux,2).dot(weights) /sum(weights)
px_sqmean = np.power(px-muy,2).dot(weights)  /sum(weight)

xpx_sqmean = (np.sum(x * px * weights) /sum(weights))**2

#%%
xtrial=np.linspace(-3, 3, 100)
ytrial= gaussian (xtrial,0,0.1)
weight =ytrial*(xtrial[1]-xtrial[0])
print(np.sqrt(sum(xtrial**2*weight)))

#%%
aa=np.array([1,2,3])
aa*aa*aa

                   # standard deviation
