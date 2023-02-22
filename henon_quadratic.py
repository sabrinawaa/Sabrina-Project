#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 14:14:53 2023

@author: sabo4ever
"""
#%%
from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as op


def hanning_window(x):
    return x * 2 * np.power((np.sin(np.pi * np.arange(len(x)) / (len(x)))), 2)

def A(a, b, c):
    return (-(a + b * c) * (a - b) + b * np.sqrt(c**2 * (a + b)**2 - 2 * a * b * (2 * c**2 - c - 1))) / (a**2 + b**2 + 2 * a * b * c)

def interpolation(data):
    index = np.argmax(data)
    N=len(data)
    
    if index==0:
        return 1.0
    elif (index== N-1):
        return 0.0
    if (data[index - 1] > data[index + 1]):
        i1 = index - 1
        i2 = index
        index = index - 1
    else:
        i1 = index
        i2 = index + 1
    value=   (index/N)+(1.0/(2.0*np.pi))*np.arcsin(A(data[i1], data[i2], np.cos(2.0*np.pi/N)) * np.sin(2.0*np.pi/N))
    return abs(value)
    

def fft_tune(x,px,alf,beta):
    xn=x/np.sqrt(beta)
    pxn=alf*x/np.sqrt(beta) + px*np.sqrt(beta)
    xn=hanning_window(xn)
    pxn=hanning_window(pxn)
    coords=xn - 1j * pxn
    freqs=np.fft.fft(coords)
    return interpolation(abs(freqs))



mad=Madx()


no_particles=17
no_turns=8192



def quad_func(x,a2,a0):
    return a2*np.square(x)+a0

#%% from data generated from condor
twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

#plt.plot(np.array(twiss.S), np.array(twiss.BETX))
tunes=[]
x0s=[]
for i in range (1,no_particles+1):
    if i <10:
        name="track.obs0001.p000"+str(i)
    else:   
        name="track.obs0001.p00"+str(i)
    
    track= pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track=track.drop(index=0,columns="*")
    track=track.astype(np.float)
  
    
    plt.figure(num='x')
    plt.scatter(track.X,track.PX,marker='.',s=0.1)
    plt.xlabel("X")
    plt.ylabel("p_X")
    plt.show()
    
   
  
    Qx=fft_tune(track.X,track.PX,twiss.ALFX[1],twiss.BETX[1])
    x0s.append(track.X[1])
    tunes.append(Qx)

 
plt.figure(num='Qx')
plt.scatter(x0s,tunes,marker='.', linewidths=0.5)
plt.xlabel("x0")
plt.ylabel("Q_x")
#%% also generating data

strengths=[0.3,0.4,0.5,0.6]
tunes_all=[ []for i in range (len(strengths))]
x0_all=[ []for i in range (len(strengths))]
p0_all=[ []for i in range (len(strengths))]

for j in range(len(strengths)):
    with open('job1.madx', 'r') as file:
        data = file.read()
        data = data.replace("K3=0.1", "K3="+str(strengths[j]))
    with open('job1.madx', 'w') as file:     
        file.write(data)
        
    mad.call("job1.madx")
    
    tunes=[]
    x0s=[]
    p0s=[]
    
    twiss=pd.read_fwf("sps.tfs",skiprows=50)
    twiss=twiss.drop(index=0)
    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

    #plt.plot(np.array(twiss.S), np.array(twiss.BETX))
    
    for i in range (1,no_particles+1):
        if i <10:
            name="track.obs0001.p000"+str(i)
        else:   
            name="track.obs0001.p00"+str(i)
        
        track= pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
        track=track.drop(index=0,columns="*")
        track=track.astype(np.float)
        # plt.figure(num='y')
        # plt.scatter(track.Y,track.PY,marker='.', linewidths=0.1)
        # plt.xlabel("y")
        # plt.ylabel("p_y")
        # plt.show()
        
        plt.figure(num=j)
        plt.scatter(track.X,track.PX,marker='.',s=0.1)
        plt.xlabel("X")
        plt.ylabel("p_X")
        plt.show()
        
       
        Qx=fft_tune(track.X,track.PX,twiss.ALFX[1],twiss.BETX[1])
        x0s.append(track.X[1])
        p0s.append(track.PX[1])
        
        tunes.append(Qx)
        

    x0_all[j]=x0s
    p0_all[j]=p0s
    tunes_all[j]=tunes
    plt.figure(num='Qx')
    plt.scatter(x0s,tunes,marker='.', linewidths=0.5)
    plt.xlabel("x0")
    plt.ylabel("Q_x")
    

    
    pfit=op.curve_fit(quad_func,x0s,tunes,p0=[20,0.247])
    xx=np.linspace(x0s[0],x0s[-1],250)
    fit=quad_func(xx,*pfit[0])
    label="k3="+ str(strengths[j])+"  a2="+str(pfit[0][0])+" a0="+str(pfit[0][1])
    
    plt.plot(xx,fit,label=label)
    plt.legend()      
    plt.savefig("Tunes.png")
    
    with open('job1.madx', 'r') as file:
        data = file.read()
        data = data.replace("K3="+str(strengths[j]),"K3=0.1")
    with open('job1.madx', 'w') as file:     
        file.write(data)
        
    print('-----------finished running strength=',strengths[j],"---------------")
    
   #%% tune inside island
twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

#plt.plot(np.array(twiss.S), np.array(twiss.BETX))
tunes=[]
x0s=[]
for i in range (9,13):
    if i <10:
        name="track.obs0001.p000"+str(i)
    else:   
        name="track.obs0001.p00"+str(i)
    
    track= pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track=track.drop(index=0,columns="*")
    track=track.astype(np.float)
  
    
    plt.figure(num='x')
    x4=track.X[::4]
    px4=track.PX[::4]
    plt.scatter(x4,px4,marker='.',s=0.1)
    plt.xlabel("X")
    plt.ylabel("p_X")
    plt.show()
    
   
  
    Qx=fft_tune(x4,px4,twiss.ALFX[1],twiss.BETX[1])
    x0s.append(track.X[1])
    tunes.append(Qx)

 
plt.figure(num='Qx')
plt.scatter(x0s,tunes,marker='.', linewidths=0.5)
plt.xlabel("x0")
plt.ylabel("Q_x")

pfit=op.curve_fit(quad_func,x0s,tunes,p0=[20,0.248])
xx=np.linspace(x0s[0],x0s[-1],250)
fit=quad_func(xx,*pfit[0])
label="  a2="+str(pfit[0][0])+" a0="+str(pfit[0][1])
    
plt.plot(xx,fit,label=label)
plt.legend()    
# %%
