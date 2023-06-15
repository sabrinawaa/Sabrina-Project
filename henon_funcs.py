#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:03:58 2023

@author: sabo4ever
"""

import numpy as np
from numba import njit
import pandas as pd


@njit
def hanning_window(x):
    return x * 2 * np.power((np.sin(np.pi * np.arange(len(x)) / (len(x)) )), 2)
@njit
def A(a, b, c):
    return (-(a + b * c) * (a - b) + b * np.sqrt(c**2 * (a + b)**2 - 2 * a * b * (2 * c**2 - c - 1))) / (a**2 + b**2 + 2 * a * b * c)
@njit
def interpolation(data):
    index = np.argmax(data)
    N=len(data)
    
    if index==0:
        return 0.0
    elif (index== N-1):
        return 1.0
    if (data[index - 1] > data[index + 1]):
        i1 = index - 1
        i2 = index
        index = index - 1
    else:
        i1 = index
        i2 = index + 1
    value=   (index/N)+(1.0/(2.0*np.pi))*np.arcsin(A(data[i1], data[i2], np.cos(2.0*np.pi/N)) * np.sin(2.0*np.pi/N))
    return abs(value)
    

def fft_tune(x,px,alf,beta):
    xn=x/np.sqrt(beta)
    pxn=alf*x/np.sqrt(beta) + px*np.sqrt(beta)
    xn=hanning_window(xn)
    pxn=hanning_window(pxn)
    coords=xn - 1j * pxn
    freqs=np.fft.fft(coords)
    return interpolation(abs(freqs))

def quad_func(x,a2,a0):
    return a2*np.square(x)+a0


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def trig_area(x1, y1, x2, y2, x3, y3):
    # calculate the area using the formula above
    area = 0.5 * abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    return area

def shape_area(x,px,x0=0,px0=0):#need to have shape centred around 0,0. orelse coords not ordered right
    r,theta = cart2pol(x,px)
    data = {"theta":theta,"r":r}
    polar = pd.DataFrame(data=data)
    polar = polar.sort_values(by="theta")
    
    x_re = list(polar.r*np.cos(polar.theta))
    px_re = list(polar.r*np.sin(polar.theta))
    
    area=0
    for j in range (len(r)-1):
        area += trig_area(x0, px0, x_re[j], px_re[j], x_re[j+1], px_re[j+1])
        
    return area