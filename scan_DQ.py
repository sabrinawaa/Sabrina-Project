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

k31 = [-1.8] 


k32 = [-1.8] 

DQ1 = [1, 1, 1, 1, 1, 1, 1, 1]#[1,2,3,4,5,1,1,1,1,-1,-2,-3,-4,-1,-1,-1,2,3,4,-2,-3,-4]
DQ2 = [ 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]#[1,1,1,1,1,2,3,4,5,-1,-1,-1,-1,-2,-3,-4,2,3,4,-2,-3,-4]
oct1="LOE.12002"
oct2="LOEN.52002"
Qy = [26.58]
island = "top"
for qy in Qy:
    for i in Qx:
        for j in range(len(k31)):
            for k in range (len(DQ1)):
                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
                    data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
                    data = data.replace("qx=QX","qx="+ str(i))
                    data = data.replace("qy=QY","qy="+ str(qy))
                    data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1[k]))
                    data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2[k]))
                    data = data.replace("oct1", oct1)
                    data = data.replace("oct2",oct2)
                    with open(job, 'w') as file:
                        file.write(data)
        
                    mad.call(job)
        
                    twiss_newname="twiss.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+island+".tfs"
                    twissum_newname="twissum.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+island+".tfs"
                    os.rename("ptc_twiss.tfs", twiss_newname)
                    os.rename("ptc_twiss_summ.tfs", twissum_newname)
    
                    with open(job, 'r') as file:
                        data = file.read()
                        data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
                        data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
                        data = data.replace("qx="+ str(i),"qx=QX")
                        data = data.replace("qy="+ str(qy),"qy=QY")
                        data = data.replace("dq1_targetvalue="+ str(DQ1[k]),"dq1_targetvalue=DQ_1")
                        data = data.replace("dq2_targetvalue="+ str(DQ2[k]),"dq2_targetvalue=DQ_2")
                        data = data.replace(oct1, "oct1")
                        data = data.replace(oct2,"oct2")
                    with open(job, 'w') as file:
                        file.write(data)
#%%
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_DQ_Qy.madx"

Qx = [26.7495]

k31 = [-3] 


k32 = [-2] 

DQ1 = [-3.12]#[1,2,3,4,5,1,1,1,1,-1,-2,-3,-4,-1,-1,-1,2,3,4,-2,-3,-4]
DQ2 = [-3.12]#[1,1,1,1,1,2,3,4,5,-1,-1,-1,-1,-2,-3,-4,2,3,4,-2,-3,-4]
oct1="LOE.22002"
oct2="LOE.32002"
Qy = [26.81,26.82,26.83,26.84]
island = "top"
for qy in Qy:
    for i in Qx:
        for j in range(len(k31)):
            for k in range (len(DQ1)):
                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
                    data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
                    data = data.replace("qx=QX","qx="+ str(i))
                    data = data.replace("qy=QY","qy="+ str(qy))
                    data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1[k]))
                    data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2[k]))
                    data = data.replace("oct1", oct1)
                    data = data.replace("oct2",oct2)
                    with open(job, 'w') as file:
                        file.write(data)
        
                    mad.call(job)
        
                    twiss_newname="twiss.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"Qy="+str(qy)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+island+".tfs"
                    twissum_newname="twissum.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"Qy="+str(qy)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+island+".tfs"
                    os.rename("ptc_twiss.tfs", twiss_newname)
                    os.rename("ptc_twiss_summ.tfs", twissum_newname)
    
                    with open(job, 'r') as file:
                        data = file.read()
                        data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
                        data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
                        data = data.replace("qx="+ str(i),"qx=QX")
                        data = data.replace("qy="+ str(qy),"qy=QY")
                        data = data.replace("dq1_targetvalue="+ str(DQ1[k]),"dq1_targetvalue=DQ_1")
                        data = data.replace("dq2_targetvalue="+ str(DQ2[k]),"dq2_targetvalue=DQ_2")
                        data = data.replace(oct1, "oct1")
                        data = data.replace(oct2,"oct2")
                    with open(job, 'w') as file:
                        file.write(data)
#%% qy after chroma

from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_DQ_Qy_2.madx"

Qx = [26.7495]

k31 = [-1.1] 

k32 = [-2.3] 


DQ1 = [1]#[1,2,3,4,5,1,1,1,1,-1,-2,-3,-4,-1,-1,-1,2,3,4,-2,-3,-4]
DQ2 = [0.005]#[1,1,1,1,1,2,3,4,5,-1,-1,-1,-1,-2,-3,-4,2,3,4,-2,-3,-4]
oct1="LOE.12002"
oct2="LOEN.52002"
Qy = np.arange(26.4,26.8,0.025)
island = "top"
for qy in Qy:
    for i in Qx:
        for j in range(len(k31)):
            for k in range (len(DQ1)):
                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("qy=QY","qy="+ str(qy))
                    data = data.replace("K3=k_31", "K3="+str(k31[j]))
                    data = data.replace("K3=k_32", "K3="+str(k32[j]))
                    data = data.replace("qx=QX","qx="+ str(i))
                    data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1[k]))
                    data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2[k]))
                    data = data.replace("oct1", oct1)
                    data = data.replace("oct2",oct2)
                    with open(job, 'w') as file:
                        file.write(data)
        
                    mad.call(job)
        
                    twiss_newname="twiss.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"Qy="+str(qy)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"after_"+island+".tfs"
                    twissum_newname="twissum.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"Qy="+str(qy)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"after_"+island+".tfs"
                    os.rename("ptc_twiss.tfs", twiss_newname)
                    os.rename("ptc_twiss_summ.tfs", twissum_newname)
    
                    with open(job, 'r') as file:
                        data = file.read()
                        data = data.replace("K3="+str(k31[j]),"K3=k_31")
                        data = data.replace("K3="+str(k32[j]),"K3=k_32")
                        data = data.replace("qx="+ str(i),"qx=QX")
                        data = data.replace("qy="+ str(qy),"qy=QY")
                        data = data.replace("dq1_targetvalue="+ str(DQ1[k]),"dq1_targetvalue=DQ_1")
                        data = data.replace("dq2_targetvalue="+ str(DQ2[k]),"dq2_targetvalue=DQ_2")
                        data = data.replace(oct1, "oct1")
                        data = data.replace(oct2,"oct2")
                    with open(job, 'w') as file:
                        file.write(data)
                    
                                        
                    
#%%
for i in Qx:
    for j in range(len(k31)):
        for k in range (len(DQ1)):
                twiss_name="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"cent.tfs"
                twissum_name="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"cent.tfs"
                twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"top.tfs"
                twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ="+str(DQ1[k])+','+str(DQ2[k])+"top.tfs"
                os.rename(twiss_name, twiss_newname)
                os.rename(twissum_name, twissum_newname)


#%%
k3s= np.arange(-3.5,-0.5,0.5)


k31,k32 = np.meshgrid(k3s,k3s)
k31 = k31.flatten()
k32 = k32.flatten()