#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:32:04 2021

@author: sjguo
"""

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
    
class Layout():
    # Layout arbitary graph to square lattice for shallow QAOA implementation
    def __init__(self, G):
        # Fixed:
        self.G = G
        self.n_nodes = len(G.nodes)
        self.edges = tuple(G.edges)
        self.a = int(np.ceil(np.sqrt(len(G.nodes)))) # size of smallest square lattice
        # Make a random initial arrangement
        arr = np.random.permutation(np.arange(self.a**2)).reshape((self.a, self.a)) 
        
        # Dynamic:
        # coordinates of each node on lattice
        XY = np.transpose(np.squeeze([np.where(arr==i) for i in range(self.a**2)]))
        self.X = XY[0]
        self.Y = XY[1]
        self.len_edges = {} # length of each edge on lattice
        for e in self.edges: 
            self.update_edge_length(e)
        self.longest_len = max(list(self.len_edges.values())) # length of the longest edge      
        # Change this to self.longest_len = x[np.argsort(x)[-n]]
                
    def step(self):
        # choose a random choice among all longest edges 
        long_edges = [k for k,v in self.len_edges.items() if v == self.longest_len]
        long_edge = long_edges[np.random.choice(len(long_edges))]
        
        if random.getrandbits(1): # flip coin for which end to move
            long_edge = long_edge[::-1]
        
        if self.X[long_edge[0]] == self.X[long_edge[1]]: # if long_edge is vertical
            neighbor = self.find_neighbor(long_edge, 'Y')
        elif self.Y[long_edge[0]] == self.Y[long_edge[1]]: # if long_edge is harizontal
            neighbor = self.find_neighbor(long_edge, 'X')
        else: # if neither
            if random.getrandbits(1): # flip coin for which direction to move
                neighbor = self.find_neighbor(long_edge, 'Y')
            else:
                neighbor = self.find_neighbor(long_edge, 'X')
                
        self.swap(long_edge[0], neighbor)
        
    def update_edge_length(self, e): # update length of edge e
        if e[0] > e[1]:
            e = (e[1], e[0])
        self.len_edges[e] = abs(self.X[e[0]]-self.X[e[1]])+abs(self.Y[e[0]]-self.Y[e[1]])
    
    def swap(self, a, b): # swap two nodes on lattice
        # swap
        self.X[a], self.X[b] = self.X[b], self.X[a]
        self.Y[a], self.Y[b] = self.Y[b], self.Y[a]
        # update edge lengths
        for x in (a, b):
            if x < self.n_nodes:
                for e in tuple(self.G.edges(x)):
                    self.update_edge_length(e)
                
        self.longest_len = max(list(self.len_edges.values())) 

    def find_neighbor(self, edge, axis):# find the neightbor of edge[0] that can reduced dist
        if axis=='Y':
            neighbor = np.intersect1d(np.where(self.X==self.X[edge[0]]), 
                                      np.where(self.Y==(self.Y[edge[0]] + np.sign(self.Y[edge[1]]-self.Y[edge[0]]))))[0]
        elif axis=='X':
            neighbor = np.intersect1d(np.where(self.Y==self.Y[edge[0]]), 
                                      np.where(self.X==(self.X[edge[0]] + np.sign(self.X[edge[1]]-self.X[edge[0]]))))[0]
        return neighbor
            
if __name__ == "__main__":
    n_nodes = 200
    d = 3
    g = nx.generators.random_graphs.random_regular_graph(d, n_nodes)
    # nx.draw(g)
    
    lo = Layout(g)
    longest_history = []
    longest_history.append(lo.longest_len)
    for i in range(100000):
        lo.step()
        longest_history.append(lo.longest_len)
    #%%
    plt.plot(longest_history)
    plt.xlabel('step')
    plt.ylabel('longest edge length')
    
    
    #%%
    from tqdm import tqdm
    d = 3
    opt_len = []
    opt_step = []
    for n_nodes in tqdm(np.arange(10,201,2)):
        opt_len_i = []
        opt_step_i = []
        for i in range(10):
            g = nx.generators.random_graphs.random_regular_graph(d, n_nodes)
            # nx.draw(g)
            
            lo = Layout(g)
            longest_history = []
            longest_history.append(lo.longest_len)
            for i in range(30000):
                lo.step()
                longest_history.append(lo.longest_len)
            opt_len_i.append(np.min(longest_history))
            opt_step_i.append(np.argmin(longest_history))
        opt_len.append(np.mean(opt_len_i))
        opt_step.append(np.mean(opt_step_i))
        
        
    #%%
    plt.plot(np.arange(10,201,2), opt_len)
    plt.xlabel('num of nodes')
    plt.ylabel('optimized longest edges length')
    
    #%%
    plt.plot(np.arange(10,201,2), opt_step)
    plt.xlabel('num of nodes')
    plt.ylabel('optimization step needed')
    
    
    