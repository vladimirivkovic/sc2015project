# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 16:14:53 2016

@author: Vlado
"""

from math import sqrt

def calcQ(pred, sec, struct):
    correct = 1.0
    observed = 1.0
    
    for i in range(len(pred)):
        if sec[i] == struct:
            observed += 1
            if sec[i] == pred[i]:
                correct += 1
    
    return 100 * correct / observed

def calcQpred(pred, sec, struct):
    correct = 1.0
    observed = 1.0
    
    for i in range(len(pred)):
        if pred[i] == struct:
            observed += 1
            if pred[i] == sec[i]:
                correct += 1
    
    return 100 * correct / observed

def calcQ3(pred, sec):
    predicted = {'H': 1.0, 'E':1.0, 'C':1.0}
    observed = {'H': 1.0, 'E':1.0, 'C':1.0}
    
    for i in range(len(pred)):
        observed[sec[i]] += 1
        if pred[i] == sec[i]:
            predicted[sec[i]] += 1
        
    return 100 * sum(predicted.values()) / sum(observed.values())
    
    
def compare(a, b):
    l = len(b)
    x = 0.000
    y = 0.000
    for i in range(l):
        if a[i] == b[i]:
            x += 1
        else:
            y += 1
    return x/(x+y)

def getSegments(string, letter):
    sgmts = []
    inside = False
    b = -1
    e = -1
    for i in range(len(string)):
        if string[i] == letter:
            if inside == False:
                b = i
                inside = True
        else:
            if inside:
                e = i-1
                sgmts.append((b,e))
                inside = False
    if inside:
        sgmts.append((b,len(string)-1))
    
    return sgmts

def minOV(s1, s2):
    if s1[1] < s2[0] or s1[0] > s2[1]:
        return 0
    else:
        return float(min(s1[1], s2[1]) - max(s1[0], s2[0]))

def maxOV(s1, s2):
    if s1[1] < s2[0] or s1[0] > s2[1]:
        return 0
    else:
        return float(max(s1[1], s2[1]) - min(s1[0], s2[0]))

def delta(s1, s2):
    return min(maxOV(s1, s2) - minOV(s1, s2), minOV(s1, s2), int(0.5*(s1[1] - s1[0] + 1)), int(0.5*(s2[1] - s2[0] + 1)))

def calcSOV(pred, sec, dssp):
    sgmts1 = getSegments(pred, dssp)
    sgmts2 = getSegments(sec, dssp)
    
    sov = 0
    N = 0
    
    for s1 in sgmts1:
        N += s1[1] - s1[0] + 1
        for s2 in sgmts2:
            if maxOV(s1, s2) > 0:
                sov += (minOV(s1, s2) + delta(s1, s2))*(s1[1] - s1[0] + 1)/maxOV(s1, s2)
    
    if N == 0:
        return None
    return sov/N * 100
    
def calcC(pred, sec, dssp):
    p = 0.0
    r = 0.0
    u = 0.0
    o = 0.0
    
    l = len(sec)
    for i in range(l):
        if sec[i] == dssp:
            if pred[i] == dssp:
                p += 1
            else:
                u += 1
        else:
            if pred[i] == dssp:
                o += 1
            else:
                r += 1
    
    return 100 * (p*r - u*o)/sqrt((p+u)*(p+o)*(r+u)*(r+o))