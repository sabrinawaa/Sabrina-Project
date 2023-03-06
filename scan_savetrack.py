#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:30:00 2023

@author: sabo1ever
"""

from cpymad.madx import Madx
import os


mad=Madx()
job='job1.madx'
# #%%
# oct_names=[]
# strengths=[0.3,0.1,0.5,0.6,0.7,0.8,0.9]
# no_particles=10

# for j in range(len(strengths)):
#     with open(job, 'r') as file:
#         data = file.read()
#         data = data.replace("K3=0.1", "K3="+str(strengths[j]))
#     with open(job, 'w') as file:     
#         file.write(data)
        
#     mad.call(job)
    
#     for i in range (1,no_particles+1):
#         if i <10:
#             name="track.obs0001.p000"+str(i)
#         else:   
#             name="track.obs0001.p00"+str(i)
            
#         newname="track.k3=" +str(strengths[j])+"no="+str(i)
#         os.rename(name, newname)
        
#     with open(job, 'r') as file:
#         data = file.read()
#         data = data.replace("K3="+str(strengths[j]),"K3=0.1")
#     with open(job, 'w') as file:     
#         file.write(data)
        
#     print('-----------finished running strength=',strengths[j],"---------------")

      
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.3,0.6,0.9]#
no_particles=8


for k in oct_names:
    for j in range(len(strengths)):
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=0.1", "K3="+str(strengths[j]))
            data = data.replace("LOF.30802", k)
            
        with open(job, 'w') as file:     
            file.write(data)
            
        mad.call(job)
        
        for i in range (1,no_particles+1):
            if i <10:
                name="track.obs0001.p000"+str(i)
            else:   
                name="track.obs0001.p00"+str(i)
                
            newname="track.oct="+k+"k3=" +str(strengths[j])+"no="+str(i)
            os.rename(name, newname)
            
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3="+str(strengths[j]),"K3=0.1")
            data = data.replace(k,"LOF.30802")
        with open(job, 'w') as file:     
            file.write(data)
            
        print('-----------finished running strength=',strengths[j],"---------------")

            