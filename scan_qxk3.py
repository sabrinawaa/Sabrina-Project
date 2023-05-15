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
# job = "qxk3_dependencee.madx"
job = "qxk3_dependence_2.madx"

#%%
mad.call(job)


#%% top
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependencee.madx"

FP = [0.0,0.0005]

Qx = [26.747]

  

# k31 = [-0.4, -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#         -0.7, -1.1, -1.5, -1.9, -2.3, -2.7] 

  

# k32 = [-0.4, -0.7, -0.7, -0.7, -0.7, -0.7, -0.7, 
#         -1.1, -1.1, -1.1, -1.1, -1.1, -1.1, 
#         -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, 
#         -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, 
#         -2.3, -2.3, -2.3, -2.3, -2.3, -2.3, 
#         -2.7, -2.7, -2.7, -2.7, -2.7, -2.7] 

k31 = [-1.8, 1.8]
k32 = [-1.8, 1.8]

island = "top"
DQ1 = 3.12
DQ2 = 2
oct1 = "LOE.22002"
oct2 = "LOE.32002"
qy = 26.58
for i in Qx:
    for j in range(len(k31)):
      with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
            data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
            data = data.replace("qx=QX","qx="+ str(i))
            data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1))
            data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2))
            data = data.replace("oct1", oct1)
            data = data.replace("oct2",oct2)

            with open(job, 'w') as file:
                file.write(data)

            mad.call(job)

            twiss_newname="twiss.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
            twissum_newname="twissum.oct="+oct1+','+oct2+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)

            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
                data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
                data = data.replace("qx="+ str(i),"qx=QX")
                data = data.replace("dq1_targetvalue="+ str(DQ1),"dq1_targetvalue=DQ_1")
                data = data.replace("dq2_targetvalue="+ str(DQ2),"dq2_targetvalue=DQ_2")
                data = data.replace(oct1, "oct1")
                data = data.replace(oct2,"oct2")
            with open(job, 'w') as file:
                file.write(data)
#%% top
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_2.madx"

FP = [0.0,0.0005]

Qx = [26.7495]


# k31 = [-0.4, -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#        -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#        -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#        -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#        -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
#        -0.7, -1.1, -1.5, -1.9, -2.3, -2.7] 

  

# k32 = [-0.4, -0.7, -0.7, -0.7, -0.7, -0.7, -0.7, 
#        -1.1, -1.1, -1.1, -1.1, -1.1, -1.1, 
#        -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, 
#        -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, 
#        -2.3, -2.3, -2.3, -2.3, -2.3, -2.3, 
#        -2.7, -2.7, -2.7, -2.7, -2.7, -2.7] 

k31 = [-3.8,-3.7, -3.9, -3.5, -4, -3.4]
k32 = [-3.8,-3.7, -3.5, -3.8, -2.3, -4]

DQ1 = 4
DQ2 = 0.005
island = "top"

oct1 = "LOE.12002"
oct2 = "LOEN.52002"
for i in Qx:
    for j in range(len(k31)):
      with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
            data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
            data = data.replace("qx=QX","qx="+ str(i))
            data = data.replace("dq1_targetvalue=DQ_1","dq1_targetvalue="+ str(DQ1))
            data = data.replace("dq2_targetvalue=DQ_2","dq2_targetvalue="+ str(DQ2))
            data = data.replace("oct1", oct1)
            data = data.replace("oct2",oct2)

            with open(job, 'w') as file:
                file.write(data)

            mad.call(job)

            twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
            twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)

            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
                data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
                data = data.replace("qx="+ str(i),"qx=QX")
                data = data.replace("dq1_targetvalue="+ str(DQ1),"dq1_targetvalue=DQ_1")
                data = data.replace("dq2_targetvalue="+ str(DQ2),"dq2_targetvalue=DQ_2")
                data = data.replace(oct1, "oct1")
                data = data.replace(oct2,"oct2")
            with open(job, 'w') as file:
                file.write(data)
#%% anothe DQ value
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_DQ.madx"

Qx = [26.748]

k31 = [-3.9]#,-2.1, -0.9, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

k32 = [-1.1]#, -0.4, -0.9, -1.2, -1.5, -1.8,-2.1, -2.2, -2.3, -2.4,-2.5] 

for i in Qx:
    for j in range(len(k31)):
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=k_31", "K3="+str(k31[j]))
            data = data.replace("K3=k_32", "K3="+str(k32[j]))
            data = data.replace("qx=QX","qx="+ str(i))

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
            with open(job, 'w') as file:
                file.write(data)
#%%renaming
Qx=26.747
i=Qx
k31=-3.927
k32=-1.073
j=k31
k=k32
twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(j)+','+str(k)+"Qx="+str(i)+"top.tfs"
twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(j)+','+str(k)+"Qx="+str(i)+"top.tfs"
os.rename("ptc_twiss.tfs", twiss_newname)
os.rename("ptc_twiss_summ.tfs", twissum_newname)

#%%
oct_names=[["LOE.12002","LOE.22002"],["LOE.22002","LOE.32002"],["LOE.12002","LOE.32002"],["LOE.22002","LOEN.52002"],["LOE.32002","LOEN.52002"]]
strengths=[-1.8, 1.8]
islands=["cent"]
for k in range(len(oct_names)):
    for j in range(len(strengths)):
        for i in range(len(islands)):
            twiss_name="twiss.oct="+oct_names[k][0]+","+oct_names[k][1]+"k3=" +str(strengths[j])+islands[i]+".tfs"
            twissum_name="twissum.oct="+oct_names[k][0]+","+oct_names[k][1]+"k3=" +str(strengths[j])+islands[i]+".tfs"
            twiss_newname="twiss.oct="+oct_names[k][0]+","+oct_names[k][1]+"k3=" +str(strengths[j])+"Qx=26.747"+islands[i]+".tfs"
            twissum_newname="twissum.oct="+oct_names[k][0]+","+oct_names[k][1]+"k3=" +str(strengths[j])+"Qx=26.747"+islands[i]+".tfs"

            os.rename(twiss_name, twiss_newname)
            os.rename(twissum_name, twissum_newname)
#%%  more renaminh
FP = [0.0,0.0005]

Qx = [26.7495]#26.7485, 26.749,26.7495]
k31 = [-0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
       -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
       -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
       -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
       -0.7, -1.1, -1.5, -1.9, -2.3, -2.7, 
       -0.7, -1.1, -1.5, -1.9, -2.3, -2.7] 

  

k32 = [-0.7, -0.7, -0.7, -0.7, -0.7, -0.7, 
       -1.1, -1.1, -1.1, -1.1, -1.1, -1.1, 
       -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, 
       -1.9, -1.9, -1.9, -1.9, -1.9, -1.9, 
       -2.3, -2.3, -2.3, -2.3, -2.3, -2.3, 
       -2.7, -2.7, -2.7, -2.7, -2.7, -2.7] 
DQ1 = 1
DQ2 = 0.005
island = "top"


for i in Qx:
    for j in range(len(k31)):
        twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(26.747)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
        twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(26.747)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
        twiss_name="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
        twissum_name="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ="+str(DQ1)+','+str(DQ2)+island+".tfs"
        
        os.rename(twiss_name, twiss_newname)
        os.rename(twissum_name, twissum_newname)


