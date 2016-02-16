# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 08:56:08 2016

@author: Vlado
"""

import os
from random import shuffle

def readProteinFile(name):
    f = open(name, 'r')

    secPrefix = 'dssp:'
    prim = []
    sec = ''
    ln = ''
    
    while True:
        ln = f.readline()
        if ln == '':
            break
        
        if 'seq' in ln or 'Seq' in ln:
            parts = ln.split(':')
            prim.append(parts[1])
        
        if ln.startswith(secPrefix):
            sec = ln[len(secPrefix):]
    
    f.close()
    
    secx = ''
    for i in range(len(sec)):
        if sec[i] == '-':
            secx += 'C'
        else:
            secx += sec[i]
        
    if len(secx) != len(prim[0]):
        secx = secx[:-2] + '\n'

    return prim, secx

path = 'RS126/';

f = open('RS126.fa', 'w')

list_dir = []
for x in os.listdir(path):
    list_dir.append(x)

shuffle(list_dir)

for filename in list_dir:   
    prim, sec = readProteinFile(path + filename)
    f.write('>p,' + filename + '#' + str(len(prim))  + '\n')
    
    for p in prim:
        f.write(p)
    f.write(sec)
    
f.close()

