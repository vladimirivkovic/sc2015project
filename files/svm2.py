# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 16:13:08 2016

@author: Vlado
"""
import inOutFunctions
import measurePrediction
from sklearn import svm
import numpy as np
import codes

def prepare_input_for(sec, prim, sw, struct):
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
        
        if sec[j] == struct:
            outs.append(1)
        else:
            outs.append(0)
    return (ins, outs)

def prepare_input_for2(sec, prim, sw, sx, sy, indexes): 
    length = len(prim)
    
    sec1 = ""
    prefix = ""
    sufix = ""
    for q in range(sw/2):
        prefix += codes.rest
        sufix += codes.rest
    primx = prefix + prim + sufix
    
    ins = []
    outs = []
    
    
    for j in range(length):
        if indexes is None:
            if sec[j] != sx and sec[j] != sy:
                continue
        if indexes is not None:
            if indexes[j] == 1:
                continue
        inputs = []
        for k in range(j, j + sw):
            if codes.aac.has_key(primx[k]):
                inputs.append(codes.aac[primx[k]])
            else:
                inputs.append(codes.aac[codes.rest])
        ins.append(np.array(inputs).flatten())
        if sec[j] == sx:
            outs.append(1)
        else:
            outs.append(0)
        sec1 += sec[j]
    return (ins, outs, sec1)

def make_SVM_1(sw, dssp, z):
    inputs_train = []
    outputs_train = []

    f = open('dataSet.txt', 'r')
    for i in range(z):
        f.readline()
        prim = f.readline().strip()
        sec = f.readline().strip()
        ins, outs = prepare_input_for(sec, prim, sw, dssp)
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    f.close()

    clfx = svm.SVC(C=1.5, gamma=0.1)
    clfx.fit(inputs_train, outputs_train)
    
    return clfx

    
sw = 7
dssp = 'H'
z = 100

clfH = make_SVM_1(sw, dssp, z)

def test_SMV_1(sw, dssp, w, clfx, z):
    f = open('dataSet.txt', 'r')

    cq = 0
    cqp = 0
    
    for i in range(z+w+2000):
        f.readline()
        prim = f.readline().strip()
        sec = f.readline().strip()


        if i > z+2000:
            ins, outs = prepare_input_for(sec, prim, sw, dssp)
            pred = inOutFunctions.display_result(clfx.predict(np.array(ins, np.float32)), {0:'X', 1:dssp})
#             print sec
#             print pred
#             print "\n"
            cq += measurePrediction.calcQ(pred, sec, dssp)
            cqp += measurePrediction.calcQpred(pred, sec, dssp)

    return (cq/w, cqp/w)

w = 50
test_SMV_1(sw, dssp, w, clfH, z)

inputs_train = []
outputs_train = []

sx = 'E'
sy = 'C'
z = 50

f = open('dataSet.txt', 'r')
for i in range(z):
    f.readline()
    prim = f.readline().strip()
    sec = f.readline().strip()
    ins, outs, sec1 = prepare_input_for2(sec, prim, sw, sx, sy, None)
    for q in ins:
        inputs_train.append(q)
    for q in outs:
        outputs_train.append(q)
    
f.close()

clf_EC = svm.SVC(C=1.5, gamma=0.1)
clf_EC.fit(inputs_train, outputs_train)

f = open('dataSet.txt', 'r')

for i in range(z+5):
    f.readline()
    prim = f.readline()
    sec = f.readline()

    ins, outs, sec = prepare_input_for2(sec, prim, sw, sx, sy, None)

    pred = inOutFunctions.display_result(clf_EC.predict(np.array(ins, np.float32)), {0:sy, 1:sx})
    if i > z:
        print sec
        print pred
        print measurePrediction.compare(sec, pred)

f = open('dataSet.txt', 'r')

w = 10

for i in range(z+w):
    f.readline()
    prim = f.readline().strip()
    sec = f.readline().strip()
    
    if i > z:
        ins, outs = prepare_input_for(sec, prim, sw, dssp)
        pred = clfH.predict(np.array(ins, np.float32))
        ins, outs, sec1 = prepare_input_for2(sec, prim, sw, sx, sy, pred)
        pred2 = clf_EC.predict(np.array(ins, np.float32))
        
        print sec

        preds = ""
        
        t = 0
        for i in range(len(pred)):
            if pred[i] == 1:
                preds += 'H'
            else:
                if pred2[t] == 0:
                    preds += 'E'
                else:
                    preds += 'C'
                t += 1
        
        print preds
        
        print measurePrediction.compare(sec, preds)
