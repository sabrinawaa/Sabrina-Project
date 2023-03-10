#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 14:14:53 2023

@author: sabo4ever
"""

from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import scipy.optimize as op

mad=Madx()


no_particles=10
no_turns=8192

strengths=[0.3,0.4,0.5,0.6]
tunes_all=[ []for i in range (len(strengths))]
x0_all=[ []for i in range (len(strengths))]
p0_all=[ []for i in range (len(strengths))]

def quad_func(x,a2,a0):
    return a2*np.square(x)+a0


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
        name="track.obs0001.p000"+str(i)
        
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
        
       
        xn=track.X/np.sqrt(twiss.BETX[1])
        pxn=twiss.ALFX[1]*track.X/np.sqrt(twiss.BETX[1]) + track.PX*np.sqrt(twiss.BETX[1])
        
        #plt.scatter(xn,pxn,marker='.',linewidths=0.25)
        # plt.xlabel("Xn")
        # plt.ylabel("p_Xn")
        # plt.axis('scaled')
        
        # coords=xn - 1j * pxn
        # freqs=np.fft.fft(coords)
        # Qx=np.where(abs(freqs)==max(abs(freqs)))[0][0]+1/len(coords) 
        # x0s.append(track.X[1])
        # p0s.append(track.PX[1])
        
        # tunes.append(Qx)
        
        
     #check if index need to +-1
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