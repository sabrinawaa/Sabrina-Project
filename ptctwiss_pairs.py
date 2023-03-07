#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:29:31 2023

@author: sabo4ever
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 22:02:29 2023

@author: sabo4ever
"""

from cpymad.madx import Madx

import os
mad=Madx()
job='ptctwiss_pairs.madx'

oct_names=[["LOE.12002","LOE.22002"],["LOE.22002","LOE.32002"],["LOE.22002","LOE.52002"]]
strengths=[0.6]
no_particles=8
no_turns=1024

islands=["top","bot"]
# FP=[[[-0.016,0.0008],[0.025,-0.00049],[0.015,-0.00075],[-0.026,0.0005]],
#     [[-0.028,0.0009],[0.0044,0.0003],[0.029,-0.0009],[-0.008,0.00025]],
#     [[-0.017,0.0008],[0.025,-0.0005],[0.014,-0.0008],[-0.026,0.0005]],
#     [[-0.017,0.0008],[0.025,-0.0005],[0.014,-0.0008],[-0.026,0.0005]]]
#0.25

FP=[
    [[-0.00466,0.000524],[0.0027,-0.00046]],
    [[0.0009,0.000378],[-0.003,-0.000315]],
    [[0.0041,0.00028],[-0.006,-0.00023]],
   ]
# 0.75


for k in range(len(oct_names)):
    for j in range(len(strengths)):
        for i in range(len(islands)):
            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3=0.1", "K3="+str(strengths[j]))
                data = data.replace("oct1", oct_names[k][0])
                data = data.replace("oct2",oct_names[k][1])
                data = data.replace("x=0.02", "x="+str(FP[k][i][0]))
                data = data.replace("px=0.0", "px="+str(FP[k][i][1]))
                
            with open(job, 'w') as file:     
                file.write(data)
                
            mad.call(job)
            
           
            twiss_newname="twiss.oct="+oct_names[k][0]+","+oct_names[k][1]+"k3=" +str(strengths[j])+islands[i]+".tfs"
            twissum_newname="twissum.oct="+oct_names[k][0]+","+oct_names[k][1]+"k3=" +str(strengths[j])+islands[i]+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)
                
            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(strengths[j]),"K3=0.1")
                data = data.replace( oct_names[k][0],"oct1")
                data = data.replace(oct_names[k][1],"oct2")
                data = data.replace("x="+str(FP[k][i][0]),"x=0.02")
                data = data.replace("px="+str(FP[k][i][1]),"px=0.0")
            with open(job, 'w') as file:     
                file.write(data)
       
                    
     

            