#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:43:20 2023

@author: sawang
"""

from cpymad.madx import Madx
import os
import numpy as np

mad=Madx()
job='turns.madx'

turns=np.arange(1000,10001,1000)
      

no_particles=1

for k in turns:     
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("turns=", "turns="+str(k))
        with open(job, 'w') as file:     
            file.write(data)
            
        mad.call(job)
        
       
        name="track.obs0001.p0001"
    
            
                
        newname="32track.turn="+str(k)
        os.rename(name, newname)
            
            
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("turns="+str(k),"turns=")
        with open(job, 'w') as file:     
            file.write(data)
                