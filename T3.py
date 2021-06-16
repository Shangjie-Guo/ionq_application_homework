#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:32:01 2021

@author: sjguo
"""


import numpy as np
import matplotlib.pyplot as plt

def est_approx_ratio(q, p, p0=4):
    return (1-q*p + 2*p*(p-1)*q*q/3)*(1-np.exp(-p/p0))

# q = np.geomspace(1e-5, 0.1, num=20)
q = np.linspace(0, 0.03, num=30) 
p = np.arange(1, 30, 1)  # len = 7

Q, P = np.meshgrid(q, p)

R = est_approx_ratio(Q, P)

plt.pcolormesh(q, p, R)
#plt.xscale('log')
plt.colorbar()

plt.plot(q, np.argmax(R, axis=0)+1, color='r')
plt.xlabel('q')
plt.ylabel('p')

#%%

plt.plot(q, np.max(R, axis=0), color='b')
plt.xlabel('q')
plt.ylabel('r_opt')