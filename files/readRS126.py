# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 08:56:08 2016

@author: Vlado
"""

import os
from random import shuffle

def readProteinFile(name):
    f = open(name, 'r')

    primPrefix = 'OrigSeq:'
    secPrefix = 'dssp:'
    prim = ''
    sec = ''
    ln = ''
    
    while True:
        ln = f.readline()
        if ln == '':
            break
    
        if ln.startswith(primPrefix):
            prim = ln[len(primPrefix):]
        
        if ln.startswith(secPrefix):
            sec = ln[len(secPrefix):]
    
    f.close()
    
    secx = ''
    for i in range(len(sec)):
        if sec[i] == '-':
            secx += 'C'
        else:
            secx += sec[i]
        
    if len(secx) != len(prim):
        secx = secx[:-2] + '\n'

    return prim, secx

path = 'RS126/';

f = open('rs126.fa', 'w')

list_dir = []
for x in os.listdir(path):
    list_dir.append(x)

shuffle(list_dir)

for filename in list_dir:
    f.write('>p,' + filename + '\n')
    
    prim, sec = readProteinFile(path + filename)
    f.write(prim)
    f.write(sec)
    
f.close()

