from cpymad.madx import Madx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import scipy.optimize as op

mad=Madx()
#%%
mad.call("job2.madx")



#%% 
no_particles=17
no_turns=8192

strengths=[0.3,0.4,0.5,0.6]
tunes_all=[ []for i in range (len(strengths))]
x0_all=[ []for i in range (len(strengths))]
p0_all=[ []for i in range (len(strengths))]

def quad_func(x,a2,a0):
    return a2*np.square(x)+a0


for j in range(len(strengths)):
    with open('job1.madx', 'r') as file:
        data = file.read()
        data = data.replace("K3=0.1", "K3="+str(strengths[j]))
    with open('job1.madx', 'w') as file:     
        file.write(data)
        
    mad.call("job1.madx")
    
    tunes=[]
    x0s=[]
    p0s=[]
    
    twiss=pd.read_fwf("sps.tfs",skiprows=50)
    twiss=twiss.drop(index=0)
    twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

    #plt.plot(np.array(twiss.S), np.array(twiss.BETX))
    
    for i in range (1,no_particles+1):
        name="track.obs0001.p000"+str(i)
        
        track= pd.read_fwf(name, skiprows=6,infer_nrows=no_turns)
        track=track.drop(index=0,columns="*")
        track=track.astype(np.float)
        # plt.figure(num='y')
        # plt.scatter(track.Y,track.PY,marker='.', linewidths=0.1)
        # plt.xlabel("y")
        # plt.ylabel("p_y")
        # plt.show()
        
        plt.figure(num=j)
        plt.scatter(track.X,track.PX,marker='.',s=0.1)
        plt.xlabel("X")
        plt.ylabel("p_X")
        plt.show()
        
       
        xn=track.X/np.sqrt(twiss.BETX[1])
        pxn=twiss.ALFX[1]*track.X/np.sqrt(twiss.BETX[1]) + track.PX*np.sqrt(twiss.BETX[1])
        
        #plt.scatter(xn,pxn,marker='.',linewidths=0.25)
        # plt.xlabel("Xn")
        # plt.ylabel("p_Xn")
        # plt.axis('scaled')
        
        coords=xn - 1j * pxn
        freqs=np.fft.fft(coords)
        Qx=(np.where(abs(freqs)==max(abs(freqs)))[0][0]+1)/len(coords) 
        x0s.append(track.X[1])
        p0s.append(track.PX[1])
        
        tunes.append(Qx)
        
        
     #check if index need to +-1
    x0_all[j]=x0s
    p0_all[j]=p0s
    tunes_all[j]=tunes
    plt.figure(num='Qx')
    plt.scatter(x0s,tunes,marker='.', linewidths=0.5)
    plt.xlabel("x0")
    plt.ylabel("Q_x")

    
    pfit=op.curve_fit(quad_func,x0s,tunes,p0=[20,0.248])
    xx=np.linspace(x0s[0],x0s[-1],250)
    fit=quad_func(xx,*pfit[0])
    label="k3="+ str(strengths[j])+"  a2="+str(pfit[0][0])+" a0="+str(pfit[0][1])
    
    plt.plot(xx,fit,label=label)
    plt.legend()       
    
    with open('job1.madx', 'r') as file:
        data = file.read()
        data = data.replace("K3="+str(strengths[j]),"K3=0.1")
    with open('job1.madx', 'w') as file:     
        file.write(data)
        
    print('-----------finished running strength=',strengths[j],"---------------")
#%% single tune track
tunes=[]
x0s=[]
twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)

#plt.plot(np.array(twiss.S), np.array(twiss.BETX))

for i in range (2,no_particles+1):
    name="track.obs0001.p000"+str(i)
    
    track= pd.read_fwf(name, skiprows=6)
    track=track.drop(index=0,columns="*")
    track=track.astype(np.float)
    # plt.figure(num='y')
    # plt.scatter(track.Y,track.PY,marker='.', linewidths=0.1)
    # plt.xlabel("y")
    # plt.ylabel("p_y")
    # plt.show()
    
    plt.figure(num='x')
    plt.scatter(track.X,track.PX,marker='.',s=0.1)
    plt.xlabel("X")
    plt.ylabel("p_X")
    plt.show()
    
   
    xn=track.X/np.sqrt(twiss.BETX[1])
    pxn=twiss.ALFX[1]*track.X/np.sqrt(twiss.BETX[1]) + track.PX*np.sqrt(twiss.BETX[1])
    
    plt.figure(num='x')
    plt.scatter(xn,pxn,marker='.',linewidths=0.25)
    plt.xlabel("Xn")
    plt.ylabel("p_Xn")
    plt.axis('scaled')
    
    coords=xn - 1j * pxn
    freqs=np.fft.fft(coords)
    Qx=np.where(abs(freqs)==max(abs(freqs)))[0][0]+1/len(coords) 
    x0s.append(track.X[1])
    tunes.append(Qx)
 #check if index need to +-1
 
plt.figure(num='Qx')
plt.scatter(x0s,tunes,marker='.', linewidths=0.5)
plt.xlabel("x0")
plt.ylabel("Q_x")


pfit=op.curve_fit(quad_func,x0s,tunes,p0=[20,0.248])
fit=quad_func(x0s,*pfit[0])
label="  a2="+str(pfit[0][1])+" a0="+str(pfit[0][0])
plt.plot(x0s,fit,label=label)
plt.legend() 
     
#%% octupole strength=0.1
pfit=np.polyfit(x0s,tunes,2)
fit=np.polyval(pfit,x0s)
label="params="+str(pfit)
plt.plot(x0s,fit,label=label)
plt.legend()   

#%% octupole strength=0.2
tunes2=[]
x0s2=[]
twiss=pd.read_fwf("sps.tfs",skiprows=50)
twiss=twiss.drop(index=0)
twiss=twiss.loc[:, ~twiss.columns.isin(['* NAME', 'KEYWORD'])].astype(np.float)
    #plt.plot(np.array(twiss.S), np.array(twiss.BETX))
    
for i in range (1,no_particles+1):
    name="track.obs0001.p000"+str(i)
    
    track= pd.read_fwf(name, skiprows=6,infer_nrows=1024)
    track=track.drop(index=0,columns="*")
    track=track.astype(np.float)
    # plt.figure(num='y')
    # plt.scatter(track.Y,track.PY,marker='.', linewidths=0.1)
    # plt.xlabel("y")
    # plt.ylabel("p_y")
    # plt.show()
    
    plt.figure(num='x')
    plt.scatter(track.X,track.PX,marker='.',s=0.1)
    plt.xlabel("X")
    plt.ylabel("p_X")
    plt.show()
   
    xn=track.X/np.sqrt(twiss.BETX[1])
    pxn=twiss.ALFX[1]*track.X/np.sqrt(twiss.BETX[1]) + track.PX*np.sqrt(twiss.BETX[1])
    
    coords=xn - 1j * pxn
    freqs=np.fft.fft(coords)
    Qx=np.where(abs(freqs)==max(abs(freqs)))[0][0]+1/len(coords) 
    x0s2.append(track.X[1])
    tunes2.append(Qx)
    
plt.figure(num='Qx')
plt.scatter(x0s2,tunes2,marker='.', linewidths=0.5)
plt.xlabel("x0")
plt.ylabel("Q_x")

# def quad_func(x,a2,a0):
#     return a2*np.square(x)+a0

# pfit=op.curve_fit(quad_func,x0s2,tunes2,p0=[20,0.248])
# fit=quad_func(x0s2,*pfit[0])
# label="a2="+str(pfit[0][0])+"  a0="+str(pfit[0][1])
# plt.plot(x0s2,fit,label=label)
# plt.legend()       





#%% plotting tunes from saved data from loop
for j in range(0,8):
    x0s=x0_all[j]
    tunes=tunes_all[j]
    plt.figure(num='Qx')
    plt.scatter(x0s,tunes,marker='.', linewidths=0.5)
    plt.xlabel("x0")
    plt.ylabel("Q_x")

    
    pfit=op.curve_fit(quad_func,x0s,tunes,p0=[20,0.247])
    xx=np.linspace(x0s[0],x0s[-1],250)
    fit=quad_func(xx,*pfit[0])
    label="k3="+ str(strengths[j])+"  a2="+str(pfit[0][0])+" a0="+str(pfit[0][1])
    
    plt.plot(xx,fit,label=label)
    plt.legend()     

#%% single particle track

name="track.obs0001.p0006"

track= pd.read_fwf(name, skiprows=6)
track=track.drop(index=0,columns="*")
track=track.astype(np.float)
   
plt.figure(num='x')
plt.scatter(track.X,track.PX,marker='.',linewidths=0.1)
plt.xlabel("X")
plt.ylabel("p_X")
plt.show()

# xn=track.X/np.sqrt(twiss.BETX[1])
# pxn=twiss.ALFX[1]*track.X/np.sqrt(twiss.BETX[1]) + track.PX*np.sqrt(twiss.BETX[1])

# coords=xn - 1j * pxn
# freqs=np.fft.fft(coords)

# plt.figure()
# plt.plot(abs(freqs))


#%%
mad.call("sps/sps.seq")
#print('Passed SPS sequence')
mad.call("sps/strengths/ft_q26.str")
#print('Passed strenght definition')
#mad.command.beam(sequence="sps", particle='proton')
twiss1=mad.twiss(sequence="sps")

#%%

mad.call("sps/toolkit/macro.madx")
qx=26.62
qy=26.58

