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


#%% bot
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependencee.madx"

FP = [0.0,0.0005]

Qx = [26.748]

k31 = [-1.224] 

k32 = [-1.378] 

island = "bot"

for i in Qx:
    for j in range(len(k31)):
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
            data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
            data = data.replace("qx=QX","qx="+ str(i))

            with open(job, 'w') as file:
                file.write(data)

            mad.call(job)

            twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ=-3,-3"+island+".tfs"
            twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ=-3,-3"+island+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)

            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
                data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
                data = data.replace("qx="+ str(i),"qx=QX")
            with open(job, 'w') as file:
                file.write(data)
                
#%% top
from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_2.madx"

FP = [0.0,0.0005]

Qx = [26.748]

k31 = [-1.224] 

k32 = [-1.378] 

island = "top"

for i in Qx:
    for j in range(len(k31)):
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
            data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
            data = data.replace("qx=QX","qx="+ str(i))

            with open(job, 'w') as file:
                file.write(data)

            mad.call(job)

            twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ=-3,-3"+island+".tfs"
            twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"DQ=-3,-3"+island+".tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)

            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
                data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
                data = data.replace("qx="+ str(i),"qx=QX")
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

#%%  more renaminh
FP = [0.0,0.0005]

Qx = [26.7485]#26.7485, 26.749,26.7495]
k31 = [-3.5,-3.0,-2.5]#-0.6,-0.9,-1.2, -1.5,-1.8,-2.2,-2.3,-2.4
k32 = [-3.5,-3.5,-3.5]
for i in Qx:
    for j in range(len(k31)):
        twiss_name= "twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"top.tfs"
        twissum_name = "twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"top.tfs"
        twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ=-3,-3top.tfs"
        twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"DQ=-3,-3top.tfs"
        
        os.rename(twiss_name, twiss_newname)
        os.rename(twissum_name, twissum_newname)


