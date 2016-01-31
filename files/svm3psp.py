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

def make_SVM_3(sw, x):
    inputs_train = []
    outputs_train = []

    #read dataset file
    f = open('dataSet.txt', 'r')
    for i in range(x):
        f.readline()
        prim = f.readline().strip()
        sec = f.readline().strip()
        ins, outs = inOutFunctions.convert_input(sec, prim, sw)
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    f.close()

    clf = svm.SVC(C=1.5, gamma=0.1)
    clf.fit(inputs_train, outputs_train)
    
    return clf
    
def test_SVM_3(clf, z, x, sw):
    f = open('dataSet.txt', 'r')
    sum = 0    
    qh = 0
    qhp = 0
    qe = 0
    qep = 0
    qc = 0
    qcp = 0

    for i in range(x+z):
        f.readline()
        prim = f.readline().strip()
        sec = f.readline().strip()

        if i > x:
            ins, outs = inOutFunctions.convert_input(sec, prim, sw)
            pred = inOutFunctions.display_result(clf.predict(np.array(ins, np.float32)), codes.alphabeth)
            sum += measurePrediction.compare(pred, sec)
            
            qh += measurePrediction.calcQ(pred, sec, 'H')
            qhp += measurePrediction.calcQpred(pred, sec, 'H')
            qe += measurePrediction.calcQ(pred, sec, 'E')
            qep += measurePrediction.calcQpred(pred, sec, 'E')
            qc += measurePrediction.calcQ(pred, sec, 'C')
            qcp += measurePrediction.calcQpred(pred, sec, 'C')
            
            sovh = measurePrediction.calcSOV(pred, sec, 'H')
            sove = measurePrediction.calcSOV(pred, sec, 'E')
            sovc = measurePrediction.calcSOV(pred, sec, 'C')

    return (qh/z, qhp/z, qe/z, qep/z, qc/z, qcp/z, sovh, sove, sovc)
    
def saveSVM(clf, filename):
    joblib.dump(clf, filename)

def loadSVM(filename):
    return joblib.load(filename)