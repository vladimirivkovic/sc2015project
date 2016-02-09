# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 16:28:15 2016

@author: Vlado
"""
import inOutFunctions
import measurePrediction
from sklearn import svm
from sklearn.externals import joblib
import numpy as np
import codes

def make_SVM_3(sw, x, filename):
    inputs_train = []
    outputs_train = []

    #read dataset file
    f = open(filename, 'r')
    
    for i in range(x):
        desc = f.readline().strip()
        primlen = int(desc.split('#')[1])
        prim = []
        
        for j in range(primlen):
            prim.append(f.readline().strip())
        sec = f.readline().strip()
        
        #prim = prim[-1:]
        
        primx = inOutFunctions.merge_sequences(prim)
        ins, outs = inOutFunctions.convert_inputX(sec, primx, sw)
        
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)
    
    f.close()
    
    #print inputs_train
    #print outputs_train

    clf = svm.SVC(C=1.5, gamma=0.1)
    clf.fit(inputs_train, outputs_train)
    
    return clf
    
def test_SVM_3(clf, z, x, sw, filename):
    f = open(filename, 'r')    
    qh = 0
    qhp = 0
    qe = 0
    qep = 0
    qc = 0
    qcp = 0
    sovh, zh = 0, 0.01
    sove, ze = 0, 0.01
    sovc, zc = 0, 0.01

    for i in range(x+z):
        desc = f.readline().strip()
        primlen = int(desc.split('#')[1])
        prim = []
        
        for j in range(primlen):
            prim.append(f.readline().strip())
        sec = f.readline().strip()
        
        prim = prim[-1:]

        if i >= x:
            primx = inOutFunctions.merge_sequences(prim)
            ins, outs = inOutFunctions.convert_inputX(sec, primx, sw)
            pred = inOutFunctions.display_result(clf.predict(np.array(ins, np.float32)), codes.alphabeth)
            
            qh += measurePrediction.calcQ(pred, sec, 'H')
            qhp += measurePrediction.calcQpred(pred, sec, 'H')
            qe += measurePrediction.calcQ(pred, sec, 'E')
            qep += measurePrediction.calcQpred(pred, sec, 'E')
            qc += measurePrediction.calcQ(pred, sec, 'C')
            qcp += measurePrediction.calcQpred(pred, sec, 'C')
            
            _sovh = measurePrediction.calcSOV(pred, sec, 'H')
            _sove = measurePrediction.calcSOV(pred, sec, 'E')
            _sovc = measurePrediction.calcSOV(pred, sec, 'C')
            
            #print sec
            #print pred
            
            if _sovh != None:
                sovh += _sovh
                zh += 1
            if _sove != None:
                sove += _sove
                ze += 1
            if _sovc != None:
                sovc += _sovc
                zc += 1
    
    f.close()

    return (qh/z, qhp/z, qe/z, qep/z, qc/z, qcp/z, sovh/zh, sove/ze, sovc/zc)
    
def saveSVM(clf, filename):
    joblib.dump(clf, filename)

def loadSVM(filename):
    return joblib.load(filename)