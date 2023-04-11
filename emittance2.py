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
# from scipy.integrate import trapezoid


import henon_funcs as fn


def emittance(x,px, w=1):

    w = np.array(w)
    
    mux= np.average(x,weights= w)
    mupx=np.average(px,weights= w)
    
    x_sqmean = sum((x-mux)**2*w) /sum(w)
    px_sqmean = sum((px-mupx)**2 *w) /sum(w)
    
    xpx_sqmean = ((x-mux).dot(w)*(px-mupx).dot(w)/sum(w))**2
    return np.sqrt(x_sqmean * px_sqmean -xpx_sqmean)



#weight=1 is unweighted 

@njit
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))) / (sig * np.sqrt(2*np.pi))
#%%
twissname="Data/twiss_csv/cent_twiss.csv"

twiss=pd.read_csv(twissname)
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.iloc[[0]]

# twiss_FP = pd.read_csv("Data/twiss_csv/75Islandtwiss_csv/LOE.32002top_twiss.csv")
# twiss_FP = twiss_FP[twiss_FP["k3"]==0.6]

# twiss = pd.DataFrame(data= [[64.33992636,1.728756478]],columns=["BETX","ALFX"])
# twiss.BETX = 64.33992636
# twiss.ALFX = 1.728756478

twiss_FP = pd.DataFrame(data= [[64.22611778,1.941697691,-0.006786209248, 0.001178558315]],columns=["BETX","ALFX","ORBIT_X", "ORBIT_PX"])


# area = 1.24e-6
# std = np.sqrt( area *0.05/ np.pi) /3
std =  0.000937
# std = 0.0002
offset = 0.0065

#%% using square gridsqmean * px_sqmean -xpx_sqmean)
no_particles=7800 #7774
no_turns=2048
folder="submit/1252sq_k3_-2.1/"
stds = np.linspace(std*0.5, std*1.5, 50)
offsets = np.linspace(offset*0.75, offset *1.25, 50)

std_grid,offs_grid=np.meshgrid(std,offsets)
std_grid=std_grid.flatten()
offs_grid=offs_grid.flatten()
#%%

x0s=[]
px0s=[]
x_fins=[]
px_fins=[]
for i in range (1,no_particles+1):

    name = folder + "track.no=" + str(i)
    # name=folder[island]+"track.oct="+oct_names[0]+"k3=0.6no="+str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    x0s.append(track.X[1])
    px0s.append(track.PX[1])
    
    x_fins.append(track.X.iloc[-1])
    px_fins.append(track.PX.iloc[-1])

#%%
plt.scatter(x_fins,px_fins,s=0.1)


xn0 = np.array(x0s)/np.sqrt(float(twiss.BETX))
pxn0 = float(twiss.ALFX) * np.array(x0s) /np.sqrt(float(twiss.BETX)) + np.array(px0s)*np.sqrt(float(twiss.BETX))

xn_fin = np.array(x_fins)/np.sqrt(float(twiss.BETX))
pxn_fin = float(twiss.ALFX) * np.array(x_fins)/np.sqrt(float(twiss.BETX)) + np.array(px_fins)*np.sqrt(float(twiss.BETX))


delta_xn = xn0[1]-xn0[0] #1.7726e-5 for 7774 case, but doesn't matter
delta_pxn = 2.7343750000000024e-05#9.58e-5 for 7774 case
#%%
emm_grid = []
emm_inis =[]
for i in range (len(std_grid)):
    weights = []
    wx =[]
    wpx=[]
    for j in range (len(xn0)):
        # gauss_func = lambda xn, pxn: (np.exp(-xn**2/(2*std_grid[i]**2)) 
        #                * np.exp(-(pxn-offs_grid[i])**2/(2*std_grid[i]**2)) 
        #                /(std_grid[i]**2 * 2* np.pi))
        # weighti = dblquad(gauss_func, pxn0[j]-delta_pxn/2, pxn0[j]+delta_pxn/2, 
                         # xn0[j]-delta_xn/2, xn0[j]+delta_pxn/2)
        weighti = gaussian(xn0[j],0,std_grid[i]) * delta_xn *gaussian (pxn0[j],offs_grid[i],std_grid[i]) * delta_pxn

        weights.append(weighti)

        
    emm_ini =  emittance(np.array(xn0), np.array(pxn0),weights)
    emm_fin = emittance(np.array(xn_fin), np.array(pxn_fin),weights)
    emm_grid.append(emm_fin)
    emm_inis.append(emm_ini)
    print(i)
#%%    
i=np.argmin(emm_inc)
weights=[]
for j in range (len(xn0)):
      
        weighti = gaussian(xn0[j],0,std_grid[i]) * delta_xn *gaussian (pxn0[j],offs_grid[i],std_grid[i]) * delta_pxn

        weights.append(weighti)
  
#%%
plt.figure()
plt.scatter(std_grid,offs_grid,c=emm_grid,s=10,cmap=plt.cm.jet)
plt.colorbar(label="final emittance [m rad]")
plt.xlabel("initial std [m]")
plt.ylabel("momentum offset")
#%%
gamma = float((1+twiss.ALFX**2)/twiss.BETX)
emm_norm_fin = float(twiss.BETX) * gamma * np.array(emm_grid)
emm_norm_ini = float(twiss.BETX) * gamma * np.array(emm_inis)

plt.scatter(emm_norm_ini,offs_grid,c=emm_norm_fin,s=10,cmap=plt.cm.jet)
plt.colorbar(label="final normalised emittance [m rad]")
plt.xlabel("initial normalised emittance [m rad]")
plt.ylabel("momentum offset")
#%%
plt.figure()
plt.scatter(std_grid,offs_grid,c=emm_inis,s=10,cmap=plt.cm.jet)
plt.colorbar(label="initial emittance")
plt.xlabel("sigma")
plt.ylabel("momentum offset")

#%%
plt.figure()
emm_inc = np.array(emm_grid)/np.array(emm_inis)
plt.scatter(emm_inis,offs_grid,c=emm_inc,s=10,cmap=plt.cm.jet)
plt.colorbar(label="emm_fin / emm_ini")
plt.xlabel("initial emittance [m rad]")
plt.ylabel("momentum offset")
#%%

plt.scatter(xn_fin,pxn_fin,c=weights,s=1,cmap=plt.cm.jet)
plt.colorbar(label="weights")
plt.xlabel("xn")
plt.ylabel("pxn")
#%%
xx = np.sqrt(float(twiss.BETX)) * xn_fin
pxx = - float(twiss.ALFX) * xn_fin / np.sqrt(float(twiss.BETX)) + pxn_fin / np.sqrt(float(twiss.BETX)) 
plt.scatter(xx,pxx,c=weights,s=5,cmap=plt.cm.jet)
plt.colorbar(label="weights")
#%%
plt.scatter(std_grid, emm_inis,s=1)
plt.xlabel("sigma")
plt.ylabel("initial emmittance")
#%%
plt.scatter(offs_grid, emm_inc,s=1)
plt.xlabel("mom offset")
plt.ylabel("emittance increase")
#%%
plt.scatter(xn0,delta_xn*gaussian(xn0,0,std_grid[i]))
plt.xlabel("xn0")
plt.ylabel("x_weights")
plt.figure()
plt.scatter(pxn0, delta_pxn*gaussian(pxn0,offs_grid[i],std_grid[i]))
plt.xlabel("pxn0")
plt.ylabel("px_weights")
#%%
emit_table= pd.DataFrame(data={"sigma": std_grid, "offset": offs_grid,
                                "emit_fin":emm_grid, "emit_ini": emm_inis,
                                "emit_inc":emm_inc})
min_idx=np.argmin(emm_inc)
min_emit= emit_table[emit_table["sigma"]==std_grid[1550]]

plt.scatter(min_emit.offset,min_emit.emit_inc)

param=np.polyfit(min_emit.offset, min_emit.emit_inc, 2)
fit=np.poly1d(param)
xx=np.linspace(min_emit.offset[0],min_emit.offset.iloc[-1],250)
label="  a1="+str(fit[1])+" a0="+str(fit[0])
plt.plot(xx,fit(xx),label=label)
plt.xlabel("Momentum Offset")
plt.ylabel("Emittance Increase")
plt.legend()
#%%
xtrial=np.linspace(-3, 3, 100)
ytrial= gaussian (xtrial,0,0.1)
weight =ytrial*(xtrial[1]-xtrial[0])
print(np.sqrt(sum(xtrial**2*weight)))

#%%
def focusing_error (alf_nom, alf_fp,beta_nom, beta_fp):
    return 0.5* (beta_nom/beta_fp + beta_fp/beta_nom
                 +(alf_nom-alf_fp * beta_nom/beta_fp)**2*beta_fp/beta_nom)

def normalise (x,px,alf,beta):
    xn = np.array(x)/np.sqrt(beta)
    pxn = alf * np.array(x)/np.sqrt(beta) + np.array(px) * np.sqrt(beta)
    return xn,pxn
                 
def steering_error (xn,pxn,x_fp,px_fp,alf,beta,w):

    xn_fp, pxn_fp = normalise(x_fp,px_fp,alf,beta)
    
    w = np.array(w)
    
    muxn= np.average(xn,weights= w)
    mupxn=np.average(pxn,weights= w)
    
    xn_std = np.sqrt(sum((xn-muxn)**2*w) /sum(w))
    pxn_std= np.sqrt(sum((pxn-mupxn)**2 *w) /sum(w))
    
    delta_xn = abs(muxn - xn_fp) 
    delta_pxn = abs(mupxn - pxn_fp)    
    
    delta_r = np.sqrt(delta_xn**2 + delta_pxn**2)
    r0 = np.sqrt(((muxn * xn_std)**2 + (mupxn * pxn_std)**2)/(muxn**2 + mupxn**2))
    return (1+ delta_r / r0) **2         
#%%
xn_fp, pxn_fp = normalise(float(twiss_FP.ORBIT_X), 
                           float(twiss_FP.ORBIT_PX),float(twiss_FP.ALFX), float(twiss.BETX))

w = np.array(weights)

muxn= np.average(xn0,weights= w)
mupxn=np.average(pxn0,weights= w)

xn_std = np.sqrt(sum((xn0-muxn)**2*w) /sum(w))
pxn_std= np.sqrt(sum((pxn0-mupxn)**2 *w) /sum(w))

delta_xn = abs(muxn - xn_fp) 
delta_pxn = abs(mupxn - pxn_fp)    

delta_r = np.sqrt(delta_xn**2 + delta_pxn**2)
r0 = np.sqrt(((muxn * xn_std)**2 + (mupxn * pxn_std)**2)/(muxn**2 + mupxn**2))
err= (1+ delta_r / r0) **2    

plt.scatter(muxn,mupxn,marker='x',s=30,c='orange')
plt.scatter(xn_fp,pxn_fp,marker='x',s=30,c='red')
#%%
foc_err = focusing_error(float(twiss.ALFX), float(twiss_FP.ALFX), float(twiss.BETX), float(twiss_FP.BETX))

steer_err = steering_error(xn0, pxn0, float(twiss_FP.ORBIT_X), 
                           float(twiss_FP.ORBIT_PX), float(twiss.ALFX),float(twiss.BETX), weights)