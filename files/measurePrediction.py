# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 16:14:53 2016

@author: Vlado
"""

def calcQ(pred, sec, struct):
    correct = 1
    observed = 1
    
    for i in range(len(pred)):
        if sec[i] == struct:
            observed += 1
            if sec[i] == pred[i]:
                correct += 1
    
    return 100 * correct / observed

def calcQpred(pred, sec, struct):
    correct = 1
    observed = 1
    
    for i in range(len(pred)):
        if pred[i] == struct:
            observed += 1
            if pred[i] == sec[i]:
                correct += 1
    
    return 100 * correct / observed
    
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
        return min(s1[1], s2[1]) - max(s1[0], s2[0])

def maxOV(s1, s2):
    if s1[1] < s2[0] or s1[0] > s2[1]:
        return 0
    else:
        return max(s1[1], s2[1]) - min(s1[0], s2[0])

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
                sov += (minOV(s1, s2) + delta(s1, s2))/maxOV(s1, s2)
    
    return sov/N