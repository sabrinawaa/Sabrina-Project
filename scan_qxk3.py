#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:26:13 2023

@author: sawang
"""
#%%
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependencee.madx"

#%%
mad.call(job)
#%%

FP = [0.0,0.0005]

Qxs = [26.747]
k3s = [2.1]
Qx,k3=np.meshgrid(Qxs,k3s)
Qx=Qx.flatten()
k3=k3.flatten()

#%%
chunk_size=8
folder = "./submit/223252_k3_10.4/"
os.mkdir(folder)

for i in range(0,len(x),chunk_size):
    
    mad_filename = folder+ "/qxk3_dependencee.madx"
    
    qxchunk = Qx[i:i + chunk_size]
    k3chunk = k3[i:i + chunk_size]
    value = []
    
    for j in range (len(xchunk)):
        value.append(f"ptc_start, x={xchunk[j]} , px={pxchunk[j]}, y= 0, py=0;\n")
    

    with open(mad_filename, "r") as f:
        contents = f.readlines()
    if contents[55].strip()=="":
        contents[55:55]=value
    else:
        print("ini pos already filled")

    with open(mad_filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)
        
#%%
mad.call("qxk3_dependencee.madx")
#%%
for i in Qx:
    for j in k3:
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=0.1", "K3="+str(j))
            data = data.replace("qx=QX","qx="+ str(i))
            
            with open(job, 'w') as file:     
                file.write(data)
                
            mad.call(job)
            
            twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(j)+"Qx="+str(i)+"cent.tfs"
            twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(j)+"Qx="+str(i)+"cent.tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)
                
            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(j),"K3=0.1")
                data = data.replace("qx="+ str(i),"qx=QX")
            with open(job, 'w') as file:     
                file.write(data)
#%%
Qx=26.747
i=Qx
k3=-0.9
j=k3
twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(j)+"Qx="+str(i)+".tfs"
twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(j)+"Qx="+str(i)+".tfs"
os.rename("ptc_twiss.tfs", twiss_newname)
os.rename("ptc_twiss_summ.tfs", twissum_newname)
