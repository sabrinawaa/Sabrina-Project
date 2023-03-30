#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:42:38 2023

@author: sawang
"""
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

oct_names=["LOE.22002"]
strengths=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
islands=["top","bot"]


for k in oct_names:
    for j in strengths:
        for i in islands:
            twissname = "Data/twiss_csv/75Islandtwiss_csv/"+k+i+"_twiss.csv"
            twiss = pd.read_csv(twissname)
            twiss = twiss[twiss.k3==j]
            params = np.array([twiss.max_X, twiss.BETX, twiss.ALFX, twiss.ALPHA_C,
                              twiss.ALPHA_C_P, twiss.ALPHA_C_P2, twiss.ALPHA_C_P3,
                              twiss.DQ1, twiss.DQ2, twiss.ORBIT_X, twiss.ORBIT_PX]).flatten()
        