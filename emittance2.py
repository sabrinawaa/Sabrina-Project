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

def focusing_error (alf_nom, alf_fp,beta_nom, beta_fp):
    return 0.5* ((beta_nom/beta_fp) + (beta_fp/beta_nom)
                 +(alf_nom/beta_nom - alf_fp/beta_fp)**2 * beta_fp * beta_nom)
                 # +(alf_nom - alf_fp*beta_fp/beta_nom)**2 * beta_nom/ beta_fp )
                  
                 

def normalise (x,px,alf,beta):
    xn = np.array(x)/np.sqrt(beta)
    pxn = alf * np.array(x)/np.sqrt(beta) + np.array(px) * np.sqrt(beta)
    return xn,pxn

def unnormalise(xn, pxn, alf, beta):
    x = np.sqrt(beta) * np.array(xn)
    px = -alf * np.array(xn)/np.sqrt(beta) + np.array(pxn) / np.sqrt(beta)
    return x,px
                 
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
twissname="Data/twiss_csv/747cent_twiss.csv"

twiss=pd.read_csv(twissname)
twiss=twiss[twiss["k3"]==0.6]
twiss=twiss.iloc[[0]]

twiss_FP = pd.read_csv("Data/twiss_csv/1252_top.csv")
twiss_FP = twiss_FP[twiss_FP["k3"]==-2.2]
twiss_FP = twiss_FP[twiss_FP["Qx"]==26.7485]

# twiss = pd.DataFrame(data= [[64.33992636,1.728756478]],columns=["BETX","ALFX"])
# twiss.BETX = 64.33992636
# twiss.ALFX = 1.728756478

# twiss_FP = pd.DataFrame(data= [[64.22611778,1.941697691,-0.006786209248, 0.001178558315]],columns=["BETX","ALFX","ORBIT_X", "ORBIT_PX"])


# area = 1.24e-6
# std = np.sqrt( area *0.05/ np.pi) /3
# std =  0.000937
std = 0.000613
offset = 0.008

#%% using square gridsqmean * px_sqmean -xpx_sqmean)
no_particles=7800 #7774
no_turns=2048
folder="submit/1252sq_k3_-2.2qx_26.7485/"
# stds = np.linspace(std*0.5, std*1.5, 50)
stds = np.linspace(0.0001,0.0011,80)
offsets = np.linspace(offset*0.5, offset *1.5, 50)

std_grid,offs_grid=np.meshgrid(stds,offset)
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
plt.figure()
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
xn_fp, pxn_fp = normalise(float(twiss_FP.ORBIT_X), 
                           float(twiss_FP.ORBIT_PX),float(twiss.ALFX), float(twiss.BETX))

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
        #weighti = gaussian(xn0[j],0,std_grid[i]) * delta_xn *gaussian (pxn0[j],offs_grid[i],std_grid[i]) * delta_pxn
        weighti = gaussian(xn0[j],xn_fp,std_grid[i]) * delta_xn *gaussian (pxn0[j],pxn_fp,std_grid[i]) * delta_pxn
        weights.append(weighti)

        
    emm_ini =  emittance(np.array(xn0), np.array(pxn0),weights)
    emm_fin = emittance(np.array(xn_fin), np.array(pxn_fin),weights)
    emm_grid.append(emm_fin)
    emm_inis.append(emm_ini)
    print(i)
#%%    
# i=np.argmin(emm_inc)
i=20
weights=[]
for j in range (len(xn0)):
      
        # weighti = gaussian(xn0[j],0,std_grid[i]) * delta_xn *gaussian (pxn0[j],offs_grid[i],std_grid[i]) * delta_pxn
        weighti = gaussian(xn0[j],xn_fp,std_grid[i]) * delta_xn *gaussian (pxn0[j],pxn_fp,std_grid[i]) * delta_pxn
        weights.append(weighti)
  
#%%
plt.figure()
plt.scatter(std_grid,offs_grid,c=emm_grid,s=10,cmap=plt.cm.jet)
plt.colorbar(label="final emittance [m rad]")
plt.xlabel("initial std [m]")
plt.ylabel("momentum offset")
#%%
plt.figure()
gamma = float((1+twiss.ALFX**2)/twiss.BETX)
def emm_norm(emm):
    return  float(twiss.BETX) * gamma * np.array(emm)
emm_norm_fin = emm_norm(emm_grid)
emm_norm_ini = emm_norm(emm_inis)

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
plt.scatter(emm_norm_ini,offs_grid,c=emm_inc,s=10,cmap=plt.cm.jet)
plt.colorbar(label="emm_fin / emm_ini")
plt.xlabel("normalised initial emittance [m rad]")
plt.ylabel("momentum offset")
#%%
plt.figure()
plt.scatter(xn_fin,pxn_fin,c=weights,s=0.5,cmap=plt.cm.jet)
# plt.scatter(xn0,pxn0,c=weights,s=0.5,cmap=plt.cm.jet)
plt.colorbar(label="weights")
plt.xlabel("xn")
plt.ylabel("pxn")
#%%
xx = np.sqrt(float(twiss.BETX)) * xn0
pxx = - float(twiss.ALFX) * xn0 / np.sqrt(float(twiss.BETX)) + pxn0/ np.sqrt(float(twiss.BETX)) 
plt.scatter(xx,pxx,c=weights,s=1,cmap=plt.cm.jet)
plt.colorbar(label="weights")
plt.scatter(twiss_FP.ORBIT_X, twiss_FP.ORBIT_PX, marker='x', s=10)
#%%
std = 0.000467
uncertainty= []

steps = np.array([1,2,3,4,5,6,8,10,12,14,16,18,20])

for k in std_grid[::10]:
    em_fin=[]
    for i in steps:
        weights = []
        xn0_sliced = xn0[::i]
        pxn0_sliced = pxn0[::i]
        xn_fin_sliced = xn_fin[::i]
        pxn_fin_sliced = pxn_fin[::i]
        
        for j in range (len(xn0_sliced)):
            weighti = gaussian(xn0_sliced[j],xn_fp,k) * delta_xn *gaussian (pxn0_sliced[j],pxn_fp,k) * delta_pxn
            weights.append(weighti)
        em_fin.append(emittance(np.array(xn_fin_sliced), np.array(pxn_fin_sliced),weights))
        
    uncertainty.append((max(abs(em_fin[:3]-em_fin[0]))-min(abs(em_fin[:3]-em_fin[0])))/em_fin[0])    
    plt.figure(num=k)    
    plt.plot(len(xn0)/steps, np.array(em_fin)-em_fin[0],'-x',label="ini norm em="+str(round(emm_norm(k**2),9)))
    plt.xlabel("No. of Initial Conditions")
    plt.ylabel("Final Normalised Emittance (m rad)")
    plt.xscale("log")
    plt.legend()

           
#%%
plt.figure(num="growth")
plt.scatter(emm_norm_ini, emm_inc,s=1, label= "k3=-2.2, Qx=0.7485, Surface=2.767e-05,Foc_Err=1.0413")
# plt.scatter(emm_norm_ini, emm_inc,s=1, label= "k3=-2.1, Qx=0.747, Surface=3.316e-05,Foc_Err=1.0234")
# plt.scatter(emm_norm_ini, emm_inc,s=1, label= "k3=-2.5, Qx=0.7485, Surface=4.374e-05,Foc_Err=1.0425")
# plt.scatter(emm_norm_ini, emm_inc,s=1, label= "k3=-2.5, Qx=0.747, Surface=4.853e-05,Foc_Err=1.0369")
# plt.scatter(emm_norm_ini, emm_inc,s=1, label= "k3=-2.1, Qx=0.746, Surface=3.739e-05 ,Foc_Err=1.0261")
plt.errorbar(emm_norm_ini, emm_inc,yerr = emm_inc*uncertainty,elinewidth=0.2)

plt.xlabel("Normalised Initial Emittance (m rad)")
plt.ylabel("Emittance Growth")
plt.legend()
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


xn_fp, pxn_fp = normalise(float(twiss_FP.ORBIT_X), 
                           float(twiss_FP.ORBIT_PX),float(twiss.ALFX), float(twiss.BETX))

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
# twiss_name = "twiss.oct=LOE.12002,LOEN.52002k3=-3.2,-1.8Qx=26.748top.tfs"
# twiss_file=pd.read_fwf(twiss_name,skiprows=88,infer_nrows=3000)
# twiss_file=twiss_file.drop(index=0)
# twiss_file=twiss_file.loc[:, ~twiss_file.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float64)

# twiss_FP.ALFX=twiss_file.ALFX[1]
# twiss_FP.BETX=twiss_file.BETX[1]

foc_err = focusing_error(float(twiss.ALFX), float(twiss_FP.ALFX), float(twiss.BETX), float(twiss_FP.BETX))

steer_err = steering_error(xn0, pxn0, float(twiss_FP.ORBIT_X), 
                           float(twiss_FP.ORBIT_PX), float(twiss.ALFX),float(twiss.BETX), weights)
print("focusing err= ", foc_err)
print('steering error=', steer_err)
