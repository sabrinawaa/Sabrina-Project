#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 17:16:56 2023

@author: sawang
"""

from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_DQ.madx"

Qx = [26.748]

k31 = [-1.8]#,-2.1, -0.9, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

k32 = [-1.8]#, -0.4, -0.9, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

DQ1 = [1,2,3,4,5,1,1,1,1,-1,-2,-3,-4,-1,-1,-1,2,3,4,-2,-3,-4]
DQ2 = [1,1,1,1,1,2,3,4,5,-1,-1,-1,-1,-2,-3,-4,2,3,4,-2,-3,-4]

for i in Qx:
    for j in range(len(k31)):
        for k in range (len(DQ1)):
            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3=k_31", "K3="+str(k31[j]))
                data = data.replace("K3=k_32", "K3="+str(k32[j]))
                data = data.replace("qx=QX","qx="+ str(i))
                data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1[k]))
                data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2[k]))
                with open(job, 'w') as file:
                    file.write(data)
    
                mad.call(job)
    
                twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"top.tfs"
                twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"top.tfs"
                os.rename("ptc_twiss.tfs", twiss_newname)
                os.rename("ptc_twiss_summ.tfs", twissum_newname)
    
                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3="+str(k31[j]),"K3=k_31")
                    data = data.replace("K3="+str(k32[j]),"K3=k_32")
                    data = data.replace("qx="+ str(i),"qx=QX")
                    data = data.replace("dq1_targetvalue="+ str(DQ1[k]),"dq1_targetvalue=DQ_1")
                    data = data.replace("dq2_targetvalue="+ str(DQ2[k]),"dq2_targetvalue=DQ_2")
                with open(job, 'w') as file:
                    file.write(data)