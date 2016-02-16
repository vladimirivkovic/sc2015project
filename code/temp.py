# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 14:40:03 2016

@author: Vlado
"""

import inOutFunctions

protD = inOutFunctions.getProteinDict('rs126.fa')
gr = inOutFunctions.getGroups('RS126/groups.txt')

for g in gr:
    for p in g:
        if protD.has_key(p) == False:
            print p

