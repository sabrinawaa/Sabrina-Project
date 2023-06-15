from cpymad.madx import Madx
import os


mad=Madx()
job=
no_particles=16
            
mad.call(job)

for i in range (1,no_particles+1):
    if i <10:
        name="track.obs0001.p000"+str(i)
    elif 9<i<100:   
        name="track.obs0001.p00"+str(i)
    elif 99<i<1000:
        name="track.obs0001.p0"+str(i)
    else:
        name="track.obs0001.p"+str(i)
        
    newname="track.oct=LOE.12002,LOEN.52002k3=k_31,k_32no="+str(i)
    os.rename(name, newname)
                    
