#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:30:00 2023

@author: sabo1ever
"""

from cpymad.madx import Madx
import os


mad=Madx()
job='pairs.madx'



oct_names=["LOE.12002","LOEN.52002"]
k31=[-2.3]
k32=[-1.3]
qx=26.7495
no_particles=16 #was 6
DQ1=2
DQ2 =0.005
qy = 26.65
for a in range (len(oct_names)):
    for k in range (len(oct_names)):
        if a>k:
            print (oct_names[k],oct_names[a])
            for j in range(len(k31)):
                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3=k_31", "K3="+str(k31[j]))
                    data = data.replace("K3=k_32", "K3="+str(k32[j]))
                    data = data.replace("qx=QX","qx="+ str(qx))
                    data = data.replace("qy=QY","qy="+ str(qy))
                    data = data.replace("oct1", oct_names[k])
                    data = data.replace("oct2",oct_names[a])
                    data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1))
                    data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2))

                with open(job, 'w') as file:
                    file.write(data)

                mad.call(job)

                for i in range (1,no_particles+1):
                    if i <10:
                        name="track.obs0001.p000"+str(i)
                    else:
                        name="track.obs0001.p00"+str(i)

                    newname="track.oct="+oct_names[k]+","+oct_names[a]+"k3=" +str(k31[j])+","+str(k32[j])+"no="+str(i)
                    os.rename(name, newname)

                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3="+str(k31[j]),"K3=k_31")
                    data = data.replace("K3="+str(k32[j]),"K3=k_32")
                    data = data.replace("qx="+ str(qx),"qx=QX")
                    data = data.replace("qy="+ str(qy),"qy=QY")
                    data = data.replace( oct_names[k],"oct1")
                    data = data.replace(oct_names[a],"oct2")
                    data = data.replace("dq1_targetvalue="+ str(DQ1),"dq1_targetvalue=DQ_1")
                    data = data.replace("dq2_targetvalue="+ str(DQ2),"dq2_targetvalue=DQ_2")
                with open(job, 'w') as file:
                    file.write(data)
                    
     

            
                    
     