#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:44:32 2023

@author: sawang
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import plotly.graph_objects as go
# import plotly.io as pio
# from scipy.stats import chisquare
# pio.renderers.default='browser'


def normalise (x,px,alf,beta):
    xn = x/np.sqrt(beta)
    pxn = alf * x/np.sqrt(beta) + px * np.sqrt(beta)
    return xn,pxn

def pair_rela (k3s, a, b1, b2, c11,c12,c22):
    k31 = k3s[0]
    k32 = k3s[1]
    return a + b1* k31 +b2*k32 + c11*k31**2 +c12* k31*k32 + c22* k32**2

def order3 (k3s, a, b1, b2, c11,c12,c22,d11,d12,d21,d22):
    k31 = k3s[0]
    k32 = k3s[1]
    return a + b1* k31 +b2*k32 + c11*k31**2 +c12* k31*k32 + c22* k32**2 + d11* k31**3 +d12*k31**2*k32 +d21 + d21*k32**2*k31+d22*k32**3

def rmse(expected,observed):
    expected = np.array(expected)
    observed = np.array(observed)
    diff= observed-expected
    return np.sqrt(np.mean(diff**2))

def amp (x,px,alf,beta):
    x = np.array(x)
    px = np.array(px)
    xn,pxn = normalise(x, px, float(alf), float(beta))
    return xn**2 + pxn**2

twissname="Data/twiss_csv/1252_cents.csv"

twiss=pd.read_csv(twissname)
Qx=float(26.7495)
twiss=twiss[twiss["Qx"]==Qx] 
#%%
topdata= pd.read_csv("Data/twiss_csv/2232_-3,-2DQ_-3.12Qy_top.csv")
# botdata= pd.read_csv("Data/twiss_csv/1252Qx_26.7495_DQ_0.2,0.005top.csv")
# botdata= pd.read_csv("Data/twiss_csv/1252_"+str(Qx)+"bot.csv")
# botdata= pd.read_csv("Data/twiss_csv/1252Qx_"+str(Qx)+"_DQ_0.2,0.005bot.csv")
# botdata= pd.read_csv("Data/twiss_csv/1252Qx_"+str(Qx)+"_DQ_0.2,0.005top.csv")
# topdata = pd.read_csv("Data/twiss_csv/1252_DQ_3,3top.csv")


#%% Island Surface

topdata=topdata.replace(r'^\s*$', np.nan, regex=True)

surfdata = topdata[~topdata["Surface"].isna()]
surfdata['Surface'] = surfdata['Surface'].astype('float64')

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[surfdata.k31, surfdata.k32], surfdata.Surface, p0=p0)


k31s = np.linspace(0,-2.5,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(surfdata.k31, surfdata.k32,surfdata.Surface)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Island Surface', fontweight ='bold')
ax.legend()
#%% Mom compaction
fig = plt.figure(figsize = (10, 7),num='1')
ax = plt.axes(projection ="3d")



p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.ALPHA_C, p0=p0)
# bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.ALPHA_C, p0=p0)


k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
# ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="Qx=26.749")
ax.scatter3D(topdata.k31, topdata.k32,topdata.ALPHA_C)
# ax.scatter3D(botdata.k31,botdata.k32,botdata.ALPHA_C)
ax.scatter3D(k31,k32,np.full(len(k31),twiss.ALPHA_C),label='centre')
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Momentum Compaction', fontweight ='bold')
ax.legend()

print("order 2 top rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*top_fit[0]),topdata.ALPHA_C))
# print("order 2 bot rmse=",rmse(pair_rela([botdata.k31,botdata.k32],*bot_fit[0]),botdata.ALPHA_C))

#%%order 3 rmse


top_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.ALPHA_C, p0=[0,0,0,0,0,0,0,0,0,0])
# bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.ALPHA_C, p0=[0,0,0,0,0,0,0,0,0,0])

print("order 3 top rmse =", rmse(order3([topdata.k31,topdata.k32],*top_fit[0]),topdata.ALPHA_C))
# print("order 3 bot rmse=",rmse(order3([botdata.k31,botdata.k32],*bot_fit[0]),botdata.ALPHA_C))
#%% Transition Energy
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

def energy_tr (gamma_tr):
    gamma_tr = np.array(gamma_tr)
    return 938.2720813*gamma_tr/1000

p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], energy_tr(topdata.GAMMA_TR), p0=p0)
# bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], energy_tr(botdata.GAMMA_TR), p0=p0)

k31s = np.linspace(0,-2.8,50)
k32s = np.linspace(0,-2.8,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
# ax.scatter3D(k31,k32,pair_rela([k31,k32],*top_fit[0]),label="top")
# ax.scatter3D(k31,k32,pair_rela([k31,k32],*bot_fit[0]),label="DQ= 0.2,0.005")
ax.scatter3D(topdata.k31, topdata.k32,energy_tr(topdata.GAMMA_TR))
ax.scatter3D(k31,k32,np.full(len(k31),energy_tr(twiss.GAMMA_TR)),label='centre')
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Transition Energy (GeV)', fontweight ='bold')
ax.legend()
print("order 2 top rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*top_fit[0]),energy_tr(topdata.GAMMA_TR)))

#%%
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(k31,k32,np.full(len(k31),energy_tr(twiss.GAMMA_TR)),label='centre')
top_fit = curve_fit(order3,[topdata.k31, topdata.k32], energy_tr(topdata.GAMMA_TR), p0=[0,0,0,0,0,0,0,0,0,0])
# bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], energy_tr(botdata.GAMMA_TR), p0=[0,0,0,0,0,0,0,0,0,0])
# ax.scatter3D(k31,k32,order3([k31,k32],*top_fit[0]),label="747")
# ax.scatter3D(k31,k32,order3([k31,k32],*bot_fit[0]),label="7495")
ax.scatter3D(topdata.k31, topdata.k32,energy_tr(topdata.GAMMA_TR))
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Transition Energy (GeV)', fontweight ='bold')
ax.legend()
print("order 3 top rmse =",rmse(order3([topdata.k31,topdata.k32],*top_fit[0]),energy_tr(topdata.GAMMA_TR)))

#%%
plt.figure(num="transition energy")
plt.scatter(np.array(topdata.k31)+1*np.array(topdata.k32), energy_tr(topdata.GAMMA_TR), s=5)
plt.plot(np.array(topdata.k31)+1*np.array(topdata.k32), np.full(len(topdata.k31),energy_tr(twiss.GAMMA_TR)),label='centre')
plt.xlabel("k31+k32")
plt.ylabel("Transition energy (GeV)")
plt.legend()
#%% transition energy >0.5 GeV
k31_en=[]
k32_en=[]
# fit = curve_fit(order3,[botdata.k31, botdata.k32], energy_tr(botdata.GAMMA_TR), p0=[0,0,0,0,0,0,0,0,0,0])
fit = curve_fit(order3,[topdata.k31, topdata.k32], energy_tr(topdata.GAMMA_TR), p0=[0,0,0,0,0,0,0,0,0,0])
# fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], energy_tr(botdata.GAMMA_TR), p0=p0)
# pred_en_tr =pair_rela([k31,k32],*fit[0])
pred_en_tr =order3([k31,k32],*fit[0])

for i in range(len(pred_en_tr)):
    if abs(pred_en_tr[i] - energy_tr(twiss.GAMMA_TR)) >0.5:
        k31_en.append(k31[i])
        k32_en.append(k32[i])


#%% ORBIT_X
k31,k32 = np.meshgrid(k31s,k32s)

fig = go.Figure(data=[
    go.Surface(z=np.array(order3([k31,k32],*top_fit[0])),x=k31,y=k32,name='Top'),
    go.Surface(z=np.array(order3([k31,k32],*bot_fit[0])),x=k31,y=k32,name='Bot'),
    go.Surface(z=np.zeros_like(k31),x=k31,y=k32,name='X=0')
               ])

fig.update_layout(title='3D Surface Plot',
                  scene=dict(xaxis_title='k31', yaxis_title='k32', zaxis_title='ORBIT_X'),
                  legend=dict(title='Surfaces'))

fig.show()
#%% X
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")


p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
top_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.ORBIT_X, p0=[0,0,0,0,0,0,0,0,0,0])
bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.ORBIT_X, p0=[0,0,0,0,0,0,0,0,0,0])
print("order 3 top rmse =",rmse(order3([topdata.k31,topdata.k32],*top_fit[0]),topdata.ORBIT_X))
print("order 3 bot rmse=",rmse(order3([botdata.k31,botdata.k32],*bot_fit[0]),botdata.ORBIT_X))



k31s = np.linspace(0,-2.5,50)
k32s = np.linspace(0,-2.5,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
ax.scatter3D(k31,k32,np.full(len(k31),0.0),label="x=0")

ax.scatter3D(k31,k32,order3([k31,k32],*top_fit[0]),label="top")
ax.scatter3D(k31,k32,order3([k31,k32],*bot_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,np.array(topdata.ORBIT_X))
ax.scatter3D(botdata.k31, botdata.k32,np.array(botdata.ORBIT_X))
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('ORBIT_X', fontweight ='bold')
ax.legend()

#%%

top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], np.array(topdata.ORBIT_X), p0=p0)
bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], np.array(botdata.ORBIT_X), p0=p0)


print("order 2 top rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*top_fit[0]),topdata.ORBIT_X))
print("order 2 bot rmse=",rmse(pair_rela([botdata.k31,botdata.k32],*bot_fit[0]),botdata.ORBIT_X))

#%% bottom FP lower than -0.00105

bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.ORBIT_PX, p0=[0,0,0,0,0,0,0,0,0,0])
botpx_pred =order3([np.array(k31_en),np.array(k32_en)],*bot_fit[0])

k31_en_px,k32_en_px = [],[]

# fig = plt.figure(figsize = (10, 7))
# ax = plt.axes(projection ="3d")

for i in range(len(botpx_pred)):
    if botpx_pred[i] < -0.0009:
        k31_en_px.append(k31_en[i])
        k32_en_px.append(k32_en[i])
        # ax.scatter3D(k31_en[i],k32_en[i],botpx_pred[i])
   
#%% sum of distance to 0
top_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.ORBIT_X, p0=[0,0,0,0,0,0,0,0,0,0])
bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.ORBIT_X, p0=[0,0,0,0,0,0,0,0,0,0])

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(k31,k32,abs(order3([k31,k32],*top_fit[0]))+abs(order3([k31,k32],*bot_fit[0])),label="sum")

# ax.scatter3D(topdata.k31, topdata.k32,abs(np.array(topdata.ORBIT_X)) + abs(np.array(botdata.ORBIT_X)))



sumx_pred = abs(order3([np.array(k31_en_px),np.array(k32_en_px)],*top_fit[0]))+ abs(order3([np.array(k31_en_px),np.array(k32_en_px)],*bot_fit[0]))
ax.scatter3D(k31_en_px,k32_en_px,sumx_pred,label="selected size and energy")
k31_en_xsum,k32_en_xsum = [],[]

for i in range(len(sumx_pred)):
    if sumx_pred[i] <0.007:
        k31_en_xsum.append(k31_en_px[i])
        k32_en_xsum.append(k32_en_px[i])
        ax.scatter3D(k31_en_px[i],k32_en_px[i],sumx_pred[i],label="here")

ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Sum of ORBIT_X', fontweight ='bold')
ax.legend()
        
print("best k31s= ",k31_en_xsum)
print("best k32s= ",k32_en_xsum)
# print('x dist sum = ',min(sumx_pred))

print ("top x=",order3([np.array(k31_en_xsum),np.array(k32_en_xsum)],*top_fit[0])) 
print ("bot x=",order3([np.array(k31_en_xsum),np.array(k32_en_xsum)],*bot_fit[0])) 

#%%DQ1
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")


p0= [0.001,0.00001, 0.00001, 0.00001, 0.00001,0.00001]
DQ1_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.DQ1, p0=p0)
DQ2_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.DQ2, p0=p0)
# bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.DQ1, p0=p0)

k31s = np.linspace(0,-4,50)
k32s = np.linspace(0,-2.8,50)
k31,k32 = np.meshgrid(k31s,k32s)
k31 = k31.flatten()
k32 = k32.flatten()
# ax.scatter3D(k31,k32,pair_rela([k31,k32],*DQ1_fit[0]),label="DQ1")
# ax.scatter3D(k31,k32,pair_rela([k31,k32],*DQ2_fit[0]),label="DQ2")
ax.scatter3D(topdata.k31, topdata.k32,topdata.DQ1)
ax.scatter3D(topdata.k31, topdata.k32,topdata.DQ2)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('DQ', fontweight ='bold')
ax.legend()
print("order 2 DQ1 rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))
print("order 2 DQ2 rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*DQ2_fit[0]),topdata.DQ2))

#%%
plt.figure(num="DQ1")
plt.scatter(np.array(topdata.k31)+1*np.array(topdata.k32), topdata.DQ1, s=5,label="DQ1")
plt.scatter(np.array(topdata.k31)+1*np.array(topdata.k32), topdata.DQ2, s=5,label="DQ2")
plt.plot(np.array(topdata.k31)+1*np.array(topdata.k32), np.full(len(topdata.k31),0),label='0')
plt.xlabel("k31+k32")
plt.ylabel("DQ")
plt.legend()

#%%
DQ1_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.DQ1, p0=[0,0,0,0,0,0,0,0,0,0])
DQ2_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.DQ2, p0=[0,0,0,0,0,0,0,0,0,0])
k31_DQ, k32_DQ= [],[]
DQ1_pred = order3([k31,k32],*DQ1_fit[0])
DQ2_pred = order3([k31,k32],*DQ2_fit[0])

for i in range(len(DQ1_pred)):
    if DQ1_pred[i]*DQ2_pred[i] >0:
        k31_DQ.append(k31[i])
        k32_DQ.append(k32[i])
        
#transition energy plot
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
top_fit =  curve_fit(order3,[topdata.k31, topdata.k32], energy_tr(topdata.GAMMA_TR), p0=[0,0,0,0,0,0,0,0,0,0])
# ax.scatter3D(k31,k32,order3([k31,k32],*top_fit[0]),label="top")

ax.scatter3D(topdata.k31, topdata.k32,energy_tr(topdata.GAMMA_TR))
ax.scatter3D(k31,k32,np.full(len(k31),energy_tr(twiss.GAMMA_TR)),label='centre')

ax.scatter3D(k31_DQ,k32_DQ,order3([np.array(k31_DQ),np.array(k32_DQ)],*top_fit[0]))
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('Transition Energy (GeV)', fontweight ='bold')
ax.legend()        

# x sum plot
# top_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.ORBIT_X, p0=[0,0,0,0,0,0,0,0,0,0])
# bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.ORBIT_X, p0=[0,0,0,0,0,0,0,0,0,0])
# fig2 = plt.figure(figsize = (10, 7))
# ax2 = plt.axes(projection ="3d")
# ax2.scatter3D(k31,k32,abs(order3([k31,k32],*top_fit[0]))+abs(order3([k31,k32],*bot_fit[0])),label="sum")
# ax2.scatter3D(k31_DQ,k32_DQ,abs(order3([np.array(k31_DQ),np.array(k32_DQ)],*top_fit[0]))+abs(order3([np.array(k31_DQ),np.array(k32_DQ)],*bot_fit[0])),label="sum")
# ax2.set_xlabel('k31', fontweight ='bold')
# ax2.set_ylabel('k32', fontweight ='bold')
# ax2.set_zlabel('sum of x distance to 0', fontweight ='bold')
#%% DQ1,2 intersection plot
k31,k32 = np.meshgrid(k31s,k32s)
DQ1_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.DQ1, p0=[0,0,0,0,0,0,0,0,0,0])
DQ2_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.DQ2, p0=[0,0,0,0,0,0,0,0,0,0])

fig = go.Figure(data=[
    go.Surface(z=np.array(order3([k31,k32],*DQ1_fit[0])),x=k31,y=k32,name='DQ1'),
    go.Surface(z=np.array(order3([k31,k32],*DQ2_fit[0])),x=k31,y=k32,name='DQ2'),
    go.Surface(z=np.zeros_like(k31),x=k31,y=k32,name='X=0')
               ])

fig.update_layout(title='3D Surface Plot',
                  scene=dict(xaxis_title='k31', yaxis_title='k32', zaxis_title='DQ'),
                  legend=dict(title='Surfaces'))

fig.show()
print("order 3 DQ1 rmse=",rmse(order3([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))
print("order 3 DQ2 rmse=",rmse(order3([topdata.k31,topdata.k32],*DQ2_fit[0]),topdata.DQ2))

#%%
DQ1_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.DQ1, p0=[0,0,0,0,0,0,0,0,0,0])
# bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.DQ1, p0=[0,0,0,0,0,0,0,0,0,0])

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(k31,k32,order3([k31,k32],*DQ1_fit[0]),label="top")
# ax.scatter3D(k31,k32,order3([k31,k32],*DQ2_fit[0]),label="bot")
ax.scatter3D(topdata.k31, topdata.k32,topdata.DQ1)
ax.set_xlabel('k31', fontweight ='bold')
ax.set_ylabel('k32', fontweight ='bold')
ax.set_zlabel('DQ2', fontweight ='bold')
ax.legend()
print("order 3 top rmse =", rmse(order3([topdata.k31,topdata.k32],*DQ1_fit[0]),topdata.DQ1))
# print("order 3 bot rmse=",rmse(order3([botdata.k31,botdata.k32],*bot_fit[0]),botdata.DQ1))

#%%DQ2
top_fit = curve_fit(pair_rela,[topdata.k31, topdata.k32], topdata.DQ2, p0=p0)

# bot_fit = curve_fit(pair_rela,[botdata.k31, botdata.k32], botdata.DQ2, p0=p0)
print("order 2 top rmse =",rmse(pair_rela([topdata.k31,topdata.k32],*top_fit[0]),topdata.DQ1))
# print("order 2 bot rmse=",rmse(pair_rela([botdata.k31,botdata.k32],*bot_fit[0]),botdata.DQ1))
#%%
top_fit = curve_fit(order3,[topdata.k31, topdata.k32], topdata.DQ2, p0=[0,0,0,0,0,0,0,0,0,0])
# bot_fit = curve_fit(order3,[botdata.k31, botdata.k32], botdata.DQ2, p0=[0,0,0,0,0,0,0,0,0,0])

print("order 3 top rmse =", rmse(order3([topdata.k31,topdata.k32],*top_fit[0]),topdata.DQ2))
# print("order 3 bot rmse=",rmse(order3([botdata.k31,botdata.k32],*bot_fit[0]),botdata.DQ2))
#%%
a=[]
b1=[]
b2=[]
c11=[]
c12=[]
c22=[]

coef= [a,b1,b2,c11,c12,c22]
coef_name = ['a','b1','b2','c11','c12','c22']
value = "DQ2"
Qxs = [26.747, 26.748, 26.7485, 26.749 ,26.7495]
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
for i in Qxs:

    data= pd.read_csv("Data/twiss_csv/1252_"+str(i)+"top.csv")
    fit = curve_fit(pair_rela,[data.k31, data.k32], data[value], p0=p0)
    ax.scatter3D(k31,k32,pair_rela([k31,k32],*fit[0]),label="Qx="+str(i))
    plt.legend()
    ax.set_xlabel('k31', fontweight ='bold')
    ax.set_ylabel('k32', fontweight ='bold')
    ax.set_zlabel(value, fontweight ='bold')

    
    for j in range(len(coef)):
        coef[j].append(fit[0][j])

#%%
for k in range (len(coef)):
    plt.scatter(Qxs,coef[k])
    fit = np.polyfit(Qxs, coef[k],2)
    pfit = np.poly1d(fit)
    Qxx = np.linspace(Qxs[0],Qxs[-1],100)
    plt.plot(Qxx, pfit(Qxx), label=coef_name[k])
    print(fit)
plt.legend()
plt.xlabel("Qx")
plt.ylabel("k3 Coefficients for "+value)

#%%
a=[]
b1=[]
b2=[]
c11=[]
c12=[]
c22=[]
d11=[]
d12=[]
d21=[]
d22=[]
coef= [a,b1,b2,c11,c12,c22,d11,d12,d21,d22]
coef_name = ['a','b1','b2','c11','c12','c22','d11','d12','d21','d22']
value = "DQ2"
Qxs = [26.747, 26.748, 26.7485, 26.749 ,26.7495]
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
for i in Qxs:
    
    # twiss=pd.read_csv("Data/twiss_csv/1252_cents.csv")
    # twiss = twiss[twiss.Qx == i]
    data= pd.read_csv("Data/twiss_csv/1252_"+str(i)+"top.csv")
    fit = curve_fit(order3,[data.k31, data.k32], data[value], p0=[0,0,0,0,0,0,0,0,0,0])
    ax.scatter3D(k31,k32,order3([k31,k32],*fit[0]),label="Qx="+str(i))
    plt.legend()
    ax.set_xlabel('k31', fontweight ='bold')
    ax.set_ylabel('k32', fontweight ='bold')
    ax.set_zlabel(value, fontweight ='bold')

    
    for j in range(len(coef)):
        coef[j].append(fit[0][j])
#%%
for k in range (len(coef)):
    plt.scatter(Qxs,coef[k])
    fit = np.polyfit(Qxs, coef[k],2)
    pfit = np.poly1d(fit)
    Qxx = np.linspace(Qxs[0],Qxs[-1],100)
    plt.plot(Qxx, pfit(Qxx), label=coef_name[k]+",rmse="+str(rmse(pfit(Qxs),coef[k])))

    print(fit)
plt.legend()
plt.xlabel("Qx")
plt.ylabel("k3 Coefficients for "+value)

#%% just Qx dependence, fixed k3
Qxs = [26.747, 26.748, 26.7485, 26.749 ,26.7495]
joint_data=pd.DataFrame(columns=['Unnamed: 0', 'name', 'island', 'k31', 'k32', 'Qx', 'max_X', 'BETX',
       'ALFX', 'ALPHA_C', 'GAMMA_TR', 'ALPHA_C_P', 'ALPHA_C_P2', 'ALPHA_C_P3',
       'DQ1', 'DQ2', 'ORBIT_X', 'ORBIT_PX'])
for i in Qxs:
    data= pd.read_csv("Data/twiss_csv//1252_csv/1252_"+str(i)+"bot.csv")
    data= data[data.k31==-1.8]#.iloc[2]
    joint_data = joint_data.append(data)
for value in ["ORBIT_X","GAMMA_TR", "DQ1", "DQ2"]  :
    plt.figure()
    plt.scatter(Qxs,joint_data[value])
    fit = np.polyfit(Qxs, joint_data[value],3)
    pfit = np.poly1d(fit)
    Qxx = np.linspace(Qxs[0],Qxs[-1],100)
    plt.plot(Qxx, pfit(Qxx), label=value)
    print(fit)
    plt.xlabel("Qx")
    plt.ylabel(value)
    plt.legend()
    

    
    

