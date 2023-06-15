#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:33:06 2023

@author: sawang
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import shutil
import os
#%%

no_turns = 2048


# for i in range (1,no_particles+1):
#     if i <10:
#         name=folder+"track.obs0001.p000"+str(i)
#     elif 9<i<100:   
#         name=folder+"track.obs0001.p00"+str(i)
#     elif 99<i<1000:
#         name=folder+"track.obs0001.p0"+str(i)
#     else:
#         name=folder+"track.obs0001.p"+str(i)    
    
#     track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
#     track = track.drop(index = 0,columns="*")
#     track = track.astype(np.float64)
#     plt.scatter(track.X,track.PX,marker='.',s=0.01)
    
    
# twiss_cent = pd.read_csv("Data/twiss_csv/cent_twiss.csv")
# twiss_cent = twiss_cent.iloc[[0]]


twiss_cent = pd.DataFrame(data= [[64.33992636,1.728756478]],columns=["BETX","ALFX"])
twiss_cent.BETX = 64.33992636
twiss_cent.ALFX = 1.728756478

# xns=np.linspace(-0.0047,0.0047,120)#bot island
# pxns=np.arange(-0.0025,-0.014,-0.00015625)#bot island

# xns=np.linspace(-0.005,0.005,150)#cent
# pxns=np.arange(-0.005,0.005,0.00015625)#cent

# xns=np.linspace(-0.0038,0.0038,130)#cent small
# pxns=np.arange(-0.0038,0.0038,0.00015625)#cent

# xns=np.linspace(-0.0054,0.0034,120)#top large
# pxns=np.arange(0.002,0.014,0.00015625)#top

# xns=np.linspace(-0.0044,0.0028,120)#top small
# pxns=np.arange(0.0019,0.01,0.00015625)#top

# xns=np.linspace(-0.0038,0.0038,120)#bot small
# pxns=np.arange(-0.0014,-0.011,-0.00015625)#bot small

xns=np.linspace(-0.0055,-0.004,20)# large sep
pxns=np.linspace(0.002,0.005,18)

# xns=np.linspace(-0.0042,-0.0032,20)# small sep
# pxns=np.linspace(0.0015,0.006,18)

# xns=np.linspace(-0.0027,-0.0024,18)
# pxns=np.linspace(0.002,0.003,15) #for 32, qx=0.744, k3=2.1, enough central area.

xn,pxn=np.meshgrid(xns,pxns)
xn=xn.flatten()
pxn=pxn.flatten()


x = np.sqrt(float(twiss_cent.BETX)) * xn 
px = - float(twiss_cent.ALFX) * xn / np.sqrt(float(twiss_cent.BETX)) + pxn / np.sqrt(float(twiss_cent.BETX)) 
# plt.figure(num='2')
plt.scatter(x,px,s=5)
#%%small separatrix grid
chunk_size=20
# folder = "./submit/1252sq_k3_"+str(k3[idx])+"qx_"+str(qx[idx])+"/"
folder ="submit/1252sq_-1.732,-2.479DQ_-0.2,-0.005_sep/"
os.mkdir(folder)

for i in range(0,len(x),chunk_size):
    
    mad_filename = folder+ "sq32_"+str(i)+".madx"
    shutil.copy("sq_template.madx",mad_filename)
        
    xchunk = x[i:i + chunk_size]
    pxchunk = px[i:i + chunk_size]
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
k3=[-1.732]#np.arange(4.9,8.41,0.7)
qx=[26.747]#np.arange(26.729,26.7164,-0.0025)

# for idx in range(len(k3)):
    
#     with open("sq_template.madx", 'r') as file:
#         data = file.read()
#         data = data.replace("K3=0.1", "K3="+str(k3[idx]))
#         data = data.replace("qx=QX","qx="+ str(qx[idx]))
        
#         with open("sq_template.madx", 'w') as file:     
#             file.write(data)
    
            
    
        
chunk_size=5
# folder = "./submit/1252sq_k3_"+str(k3[idx])+"qx_"+str(qx[idx])+"/"
folder = "submit/1252sq_-1.403,-1.687DQ_1,0.005_cent/"
os.mkdir(folder)

for i in range(0,len(x),chunk_size):
    
    mad_filename = folder+ "/sq32_"+str(i)+".madx"
    shutil.copy("sq_template.madx",mad_filename)
        
    xchunk = x[i:i + chunk_size]
    pxchunk = px[i:i + chunk_size]
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
            
    # with open("sq_template.madx", 'r') as file:
    #     data = file.read()
    #     data = data.replace("K3="+str(k3[idx]),"K3=0.1")
    #     data = data.replace("qx="+ str(qx[idx]),"qx=QX")
    # with open("sq_template.madx", 'w') as file:     
    #     file.write(data)
#%%kicked
k3=[-1.925]#np.arange(4.9,8.41,0.7)
qx=[26.7495]#np.arange(26.729,26.7164,-0.0025)

# for idx in range(len(k3)):
    
#     with open("sq_template.madx", 'r') as file:
#         data = file.read()
#         data = data.replace("K3=0.1", "K3="+str(k3[idx]))
#         data = data.replace("qx=QX","qx="+ str(qx[idx]))
        
#         with open("sq_template.madx", 'w') as file:     
#             file.write(data)
    
            
    
        
chunk_size=5
# folder = "./submit/1252sq_k3_"+str(k3[idx])+"qx_"+str(qx[idx])+"/"
folder = "submit/1252sq_-1.957,-2.918DQ_3,0.005_cent_fil_orig_moremore/"
# folder = "submit/1252sq_-1.403,-1.687DQ_1,0.005_cent_fil/"
# os.mkdir(folder)


x_fins=[]
px_fins=[]
folder_orig =  "submit/1252sq_-1.957,-2.918DQ_3,0.005_cent_fil_orig_more/"
# folder_orig = "submit/1252sq_-1.336,-1.586DQ_-0.2,-0.005_bot/"
no_particles = 9000
for i in range (1,no_particles+1):

    name = folder_orig + "track.no=" + str(i)
    
    track = pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
    track = track.drop(index = 0,columns="*")
    track = track.astype(np.float64)
    
    if track.X.iloc[0]!= track.X.iloc[-1]:

        x_fins.append(track.X.iloc[-1])
        px_fins.append(track.PX.iloc[-1])
#%%kicked continued

px_kicked = np.array(px_fins)#-0.0012953864584999595 #- 0.0012728885016671549# large
# px_kicked = np.array(px_fins)-0.000824808616445194

plt.scatter(x_fins,px_kicked,c=weights_stage4, s=1)
#%%kicked write

for i in range(0,len(x_fins),chunk_size):
    
    mad_filename = folder+ "/sq32_"+str(i)+".madx"
    shutil.copy("sq_template.madx",mad_filename)
        
    xchunk = x_fins[i:i + chunk_size]
    pxchunk = px_kicked[i:i + chunk_size]
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
            
    # with open("sq_template.madx", 'r') as file:
    #     data = file.read()
    #     data = data.replace("K3="+str(k3[idx]),"K3=0.1")
    #     data = data.replace("qx="+ str(qx[idx]),"qx=QX")
    # with open("sq_template.madx", 'w') as file:     
    #     file.write(data)
                
#%%
k31 = [-0.9, -1.2, 
       -1.5, -1.8,-2.1,-2.4] 

k32 = [-0.9, -1.2,
       -1.5, -1.8,-2.1,-2.4] 
oct_1= "LOE.12002"
oct_2 = "LOEN.52002"
            
Qx=26.248
folder = "./submit/1252Qx_248/"
os.mkdir(folder)
for idx in range(len(k31)):
    
    with open("pairs.madx", 'r') as file:
        data = file.read()
        data = data.replace("K3=k_31;!1", "K3="+str(k31[j])+";!1")
        data = data.replace("K3=k_32;!2", "K3="+str(k32[j])+";!2")
        data = data.replace("qx=QX","qx="+ str(Qx))

        data = data.replace("oct1", oct_1)
        data = data.replace("oct2",oct_2)
        
        with open("pairs.madx", 'w') as file:     
            file.write(data)
    
        mad_filename = folder+ "K3="+str(k31[idx])+'_'+str(k32[idx])+".madx"
        shutil.copy("pairs.madx",mad_filename)

            
    with open("pairs.madx", 'r') as file:
        data = file.read()
        data = data.replace("K3="+str(k31[j])+";!1","K3=k_31;!1")
        data = data.replace("K3="+str(k32[j])+";!2","K3=k_32;!2")
        data = data.replace("qx="+ str(Qx),"qx=QX")
    with open("pairs.madx", 'w') as file:     
        file.write(data)
    
    with open("pairs_template.py", 'r') as file:
        data = file.read()
        data = data.replace("k_31", str(k31[idx]))
        data = data.replace("k_32", str(k32[idx]))


        
        with open("pairs_template.py", 'w') as file:     
            file.write(data)
    
        py_filename = folder+"K3="+str(k31[idx])+'_'+str(k32[idx])+".py"
        shutil.copy("pairs_template.py",py_filename)

            
    with open("pairs_template.py", 'r') as file:
        data = file.read()
        data = data.replace(str(k31[idx]),"k_31")
        data = data.replace(str(k32[idx]),"k_32")
        
        data = data.replace(oct_1, "oct1")
        data = data.replace(oct_2, "oct2")


    with open("pairs_template.py", 'w') as file:     
        file.write(data)

 ##remember to restore k_32 after each run!!              
            
            
            