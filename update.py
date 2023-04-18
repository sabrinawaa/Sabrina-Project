#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:52:48 2023

@author: sabo4ever
"""

from cpymad.madx import Madx
import numpy as np

import os
mad=Madx()
job = "qxk3_dependence_2.madx"

FP = [0.0,0.0005]

Qxs = [26.748, 26.7485]
k31s = [-2.6]
k32s = [-2.4]
Qx,k3=np.meshgrid(Qxs,k31s)
Qx=Qx.flatten()
k31=k3.flatten()
Qx,k32=np.meshgrid(Qxs,k32s)
Qx=Qx.flatten()
k312=k32.flatten()

for i in Qx:
    for j in range(len(k31)):
        with open(job, 'r') as file:
            data = file.read()
            data = data.replace("K3=k31", "K3="+str(k31[j]))
            data = data.replace("K3=k32", "K3="+str(k32[j]))
            data = data.replace("qx=QX","qx="+ str(i))

            with open(job, 'w') as file:
                file.write(data)

            mad.call(job)

            twiss_newname="twiss.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j])+"Qx="+str(i)+"top.tfs"
            twissum_newname="twissum.oct=LOE.12002,LOEN.52002"+"k3=" +str(k31[j])+','+str(k32[j]) +"Qx="+str(i)+"top.tfs"
            os.rename("ptc_twiss.tfs", twiss_newname)
            os.rename("ptc_twiss_summ.tfs", twissum_newname)

            with open(job, 'r') as file:
                data = file.read()
                data = data.replace("K3="+str(k31[j]),"K3=k31")
                data = data.replace("K3="+str(k32[j]),"K3=k32")
                data = data.replace("qx="+ str(i),"qx=QX")
            with open(job, 'w') as file:
                file.write(data)

#%%
 !system,"[ ! -e sps ] && [ -d /afs/cern.ch/eng/acc-models/sps/2021 ] && ln -nfs /afs/cern.ch/eng/acc-models/sps/2021 sps";
 !system,"[ ! -e sps ] && git clone https://gitlab.cern.ch/acc-models/acc-models-sps -b 2021 sps";

option, -echo;

call,file="sps1.seq";
call,file="ft_q26.str";

beam,particle=proton, PC=14;

use,sequence=sps;

!twiss;

LOE.12002, K3=k31;
LOEN.52002, K3=k32;

call,file="macro.madx";
qx=QX; ! originally 26.62
qy=26.58;

exec, sps_match_tunes(qx,qy);

! to set the chromaticity using knob in LSA
exec,sps_define_sext_knobs;
exec,sps_set_chroma_weights_ft;

! the qph and qpv correspond to normalized chromaticity
qph_setvalue = +0.1;
qpv_setvalue = +0.0;





! to match the chromaticity (varying the chroma knob settings)
sps_match_chroma(dq1_target_value,dq2_target_value) : macro = {
 match, sequence=sps;
        vary, name=qph_setvalue,  step=1.e-8;
        vary, name=qpv_setvalue,  step=1.e-8;
        global, dq1=dq1_targetvalue, dq2=dq2_targetvalue;
        jacobian, calls=10, tolerance=1e-25;
 endmatch;
};

dq1_targetvalue=3.12;
dq2_targetvalue=2;
exec, sps_match_chroma(dq1_targetvalue,dq2_targetvalue);

select,flag=twiss,column=name,keyword,s,betx,alfx,mux,bety,alfy,muy,x,px,y,py,t,pt,dx,dpx,dy,dpy,k2l,k3l;
twiss,file="sps.tfs";

seqedit,sequence=sps;
cycle,start=KIK.11654;
endedit;


#%%
from cpymad.madx import Madx
import os


mad=Madx()
job='pairs.madx'



oct_names=["LOE.12002","LOEN.52002"]
k31=[-3]
k32=[-2]
qx=26.7485
no_particles=16

for a in range (len(oct_names)):
    for k in range (len(oct_names)):
        if a>k:
            print (oct_names[k],oct_names[a])
            for j in range(len(k31)):
                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3=k31", "K3="+str(k31[j]))
                    data = data.replace("K3=k32", "K3="+str(k32[j]))
                    data = data.replace("qx=QX","qx="+ str(qx))
                    data = data.replace("oct1", oct_names[k])
                    data = data.replace("oct2",oct_names[a])

                with open(job, 'w') as file:
                    file.write(data)

                mad.call(job)

                for i in range (1,no_particles+1):
                    if i <10:
                        name="track.obs0001.p000"+str(i)
                    else:
                        name="track.obs0001.p00"+str(i)

                    newname="track.oct="+oct_names[k]+","+oct_names[a]+"k3=" +str(strengths[j])+"no="+str(i)
                    os.rename(name, newname)

                with open(job, 'r') as file:
                    data = file.read()
                    data = data.replace("K3="+str(k31[j]),"K3=k31")
                    data = data.replace("K3="+str(k32[j]),"K3=k32")
                    data = data.replace("qx="+ str(qx),"qx=QX")
                    data = data.replace( oct_names[k],"oct1")
                    data = data.replace(oct_names[a],"oct2")
                with open(job, 'w') as file:
                    file.write(data)
#%%

Qxs = [26.748, 26.7485]
k31s = [-2.6]
k32s = [-2.4]
Qx,k3=np.meshgrid(Qxs,k31s)
Qx=Qx.flatten()
k31=k3.flatten()
Qx,k32=np.meshgrid(Qxs,k32s)
k32=k32.flatten()


