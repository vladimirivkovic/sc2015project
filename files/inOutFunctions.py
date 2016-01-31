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
    
def display_result(outputs, alphabet):
    result = ''
    for x in outputs:
        result += alphabet[x]
    return result