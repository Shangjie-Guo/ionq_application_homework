#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 18:37:05 2021

@author: sjguo
"""

from qiskit import QuantumCircuit
import numpy as np

n_qubit = 8
n_step = 2

# Hamiltonian params
ht = 0.2 
alpha = 0.3
beta = 0.4
gamma = 0.5 

def N_gate(qc, i, j): #qubit interaction N decomposed
    qc.cnot(j, i)
    qc.rz(gamma, i)
    qc.ry(alpha, j)
    qc.cnot(i, j)
    qc.ry(beta, j)
    qc.cnot(j, i)

def evo_step(qc): #Trotterized evolution step
    
    qc.rz(ht-np.pi/2, 0)
    qc.rz(ht+np.pi/2, -1)
    for i in range(1, n_qubit-1):
        qc.rz(ht, i)
        
    for i in range(n_qubit//2):
        N_gate(qc, 2*i, 2*i+1)
        
    for i in range((n_qubit-1)//2):
        N_gate(qc, 2*i+1, 2*i+2)

XYZ_sim = QuantumCircuit(n_qubit) #Circuit that simulate XYZ model.

XYZ_sim.rz(np.pi/2, 0) #Compensate the rotation on first qubit
for i in range(n_step):
    evo_step(XYZ_sim)
    
XYZ_sim.rz(-np.pi/2, 0) #Compensate the rotation on first qubit
XYZ_sim.draw(output='mpl')
