#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:30:00 2023

@author: sabo4ever
"""

from cpymad.madx import Madx
import os


mad=Madx()

strengths=[0.3,0.4,0.5,0.6]
no_particles=17

for j in range(len(strengths)):
    with open('job1.madx', 'r') as file:
        data = file.read()
        data = data.replace("K3=0.1", "K3="+str(strengths[j]))
    with open('job1.madx', 'w') as file:     
        file.write(data)
        
    mad.call("job1.madx")
    
    for i in range (1,no_particles+1):
        if i <10:
            name="track.obs0001.p000"+str(i)
        else:   
            name="track.obs0001.p00"+str(i)
            
        newname="k3=" +str(j)+"no="++str(i)
        os.rename('name', newname)
            
            
            