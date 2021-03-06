# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:48:08 2016

@author: Vlado
"""
import numpy as np
import codes

# prepare training data for 3-class SVM
def convert_input(sec, prim, sw):
    length = len(prim)
    prefix = ""
    sufix = ""
    for q in range(sw/2):
        prefix += codes.rest
        sufix += codes.rest
    primx = prefix + prim + sufix
    ins = []
    outs = []
    for j in range(length):
        inputs = []
        for k in range(j, j + sw):
            if codes.aac.has_key(primx[k]):
                inputs.append(codes.aac[primx[k]])
            else:
                inputs.append(codes.aac[codes.rest])
        ins.append(np.array(inputs).flatten())
        outs.append(codes.alph[sec[j]])
    return (ins, outs)

def merge_sequences(seq):
    merged = []    
    
    length = len(seq[0])
    for i in range(length):
        merged.append(np.zeros(len(codes.aac)))
    for s in seq:
        for j in range(length):
            if codes.aac.has_key(s[j]):
                merged[j] += np.array(codes.aac[s[j]])
            else:
                merged[j] += np.array(codes.aac[codes.rest])
    
    for j in range(length):
        merged[j] /= float(len(seq));
            
    return merged
        
    
def display_result(outputs, alphabet):
    result = ''
    for x in outputs:
        result += alphabet[x]
    return result

def convert_inputX(sec, prim, sw):
    length = len(sec)
    sump = sum(prim[0])
    
    for q in range(sw/2):
        prim.insert(0, sump*np.array(codes.aac[codes.rest]))
        prim.append(sump*np.array(codes.aac[codes.rest]))
    
    ins = []
    outs = []
    
    for j in range(length):
        inputs = []
        for k in range(j, j + sw):
            inputs.append(prim[k])
        ins.append(np.array(inputs).flatten())
        outs.append(codes.alph[sec[j]])
    return (ins, outs)

def convert_inputNN(sec, prim, sw):
    length = len(sec)
    sump = sum(prim[0])
    
    for q in range(sw/2):
        prim.insert(0, sump*np.array(codes.aac[codes.rest]))
        prim.append(sump*np.array(codes.aac[codes.rest]))
    
    ins = []
    outs = []
    
    for j in range(length):
        inputs = []
        for k in range(j, j + sw):
            inputs.append(prim[k])
        ins.append(np.array(inputs).flatten())
        outs.append(codes.alphNN[sec[j]])
    return (ins, outs)

def convert_inputNN2(sec, prim, sw):
    length = len(sec)
    sump = sum(prim[0])
    
    for q in range(sw/2):
        prim.insert(0, sump*np.array([0,0,0]))
        prim.append(sump*np.array([0,0,0]))
    
    ins = []
    outs = []
    
    for j in range(length):
        inputs = []
        for k in range(j, j + sw):
            inputs.append(prim[k])
        ins.append(np.array(inputs).flatten())
        outs.append(codes.alphNN[sec[j]])
    return (ins, outs)

def prepare_input_forX(sec, prim, sw, struct):
    length = len(sec)
    sump = sum(prim[0])
    
    for q in range(sw/2):
        prim.insert(0, sump*np.array(codes.aac[codes.rest]))
        prim.append(sump*np.array(codes.aac[codes.rest]))
    
    ins = []
    outs = []
    
    for j in range(length):
        inputs = []
        for k in range(j, j + sw):
            inputs.append(prim[k])
        ins.append(np.array(inputs).flatten())
        if sec[j] == struct:
            outs.append(1)
        else:
            outs.append(0)
    return (ins, outs)

def getProteinDict(filename):
    proteins = {}    
    
    f = open(filename, 'r')
    
    while True:
        line = f.readline().strip()
        if line == '':
            break
        
        protName = line.split(',')[1].split('.')[0]
        primlen = int(line.split('#')[1])
        prim = []
        
        for j in range(primlen):
            prim.append(f.readline().strip())
        sec = f.readline().strip()
        
        proteins[protName] = {'prim': prim, 'sec': sec}
    
    f.close()
    
    return proteins

def getGroups(filename):
    f = open(filename, 'r')
    
    groups = []
    
    while True:
        line = f.readline().strip()
        if line == '':
            break
        
        groups.append(line.split(','))
    
    f.close()
    
    return groups