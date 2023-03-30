#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 17:14:12 2023

@author: sawang
"""
import numpy as np
import matplotlib.pyplot as plt

k3 = np.array([0.6,0.9,1.2,1.5,1.8,2.1,2.4,2.7,4,5,6,7,8,9,10])
area = np.array([2.2836247556816813e-06,2.5708705680100447e-06,2.745690369568217e-06,
                 2.8464304391616223e-06,2.8983813317290796e-06,2.9163331440741754e-06,
                 2.9330454835646496e-06, 2.9125595290220617e-06,2.792164337453154e-06 ,
                 2.6556116849614286e-06,2.5101776734361804e-06 ,2.3800335479180705e-06,
                 2.2493619363117687e-06,2.1285641225179724e-06,2.017631004143895e-06 ])



plt.scatter(k3,area,marker='x')
plt.ylabel("Island Surface [m rad]")
plt.xlabel("k3 [m^-4]")

pfit=np.polyfit(k3,area,2)
xx=np.linspace(k3[0],k3[-1],250)
fit=np.poly1d(pfit)
label="  a2="+str(pfit[0])+" a1="+str(pfit[1])+" a0="+str(pfit[2])
    
# plt.plot(xx,fit(xx),label=label)
# plt.legend()  

#%%
height = np.array([0.000959,0.001038,0.001137,0.001184,0.001215,0.001256,0.001276,
                   0.001336,0.001343,0.001344,0.001332,0.001319,0.001298,0.001275])
plt.scatter(k3[1:],height,marker='x')
plt.ylabel("Island Normalised Height at x=0[rad]")
plt.xlabel("k3 [m^-4]")
