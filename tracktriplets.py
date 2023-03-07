#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 14:51:50 2023

@author: sabo4ever
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:30:00 2023

@author: sabo1ever
"""

from cpymad.madx import Madx
import os


mad=Madx()
job='triplets.madx'


      
oct_names=["LOE.12002","LOE.22002","LOE.32002","LOEN.52002"]
strengths=[0.6]#
no_particles=8
for b in range (len(oct_names)):
    for a in range (len(oct_names)):
        if b>a:
            for k in range (len(oct_names)):
                if a>k:
                    print (oct_names[k],oct_names[a],oct_names[b])
                    for j in range(len(strengths)):
                        with open(job, 'r') as file:
                            data = file.read()
                            data = data.replace("K3=0.1", "K3="+str(strengths[j]))
                            data = data.replace("oct1", oct_names[k])
                            data = data.replace("oct2",oct_names[a])
                            data = data.replace("oct3",oct_names[b])
                        with open(job, 'w') as file:     
                            file.write(data)
                            
                        mad.call(job)
                        
                        for i in range (1,no_particles+1):
                            if i <10:
                                name="track.obs0001.p000"+str(i)
                            else:   
                                name="track.obs0001.p00"+str(i)
                                
                            newname="track.oct="+oct_names[k]+","+oct_names[a]+","+oct_names[b]+"k3=" +str(strengths[j])+"no="+str(i)
                            os.rename(name, newname)
                            
                        with open(job, 'r') as file:
                            data = file.read()
                            data = data.replace("K3="+str(strengths[j]),"K3=0.1")
                            data = data.replace( oct_names[k],"oct1")
                            data = data.replace(oct_names[a],"oct2")
                            data = data.replace(oct_names[b],"oct3")
                        with open(job, 'w') as file:     
                            file.write(data)
                    
     

            