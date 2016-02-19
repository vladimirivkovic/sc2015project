# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 10:58:51 2016

@author: Vlado
"""

import inOutFunctions
import measurePrediction
from sklearn import svm
import numpy as np

def make_SVM_2(sw, dataset, groups, without, struct):
    inputs_train = []
    outputs_train = []
    
    protCodes = []
    for i in range(len(groups)):
        if i == without:
            continue
        else:
            for s in groups[i]:
                protCodes.append(s)

    for p in protCodes:
        sec = dataset[p]['sec']
        
        prim = dataset[p]['prim']
        
        #prim = prim[-2:]
        
        primx = inOutFunctions.merge_sequences(prim)
        ins, outs = inOutFunctions.prepare_input_forX(sec, primx, sw, struct)
        
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    clf = svm.SVC(C=1.5, gamma=0.1)
    clf.fit(inputs_train, outputs_train)

    return clf


datasetFile = 'rs126.fa'
groupsFile = 'RS126/groups.txt'

protDict = inOutFunctions.getProteinDict(datasetFile)
groups = inOutFunctions.getGroups(groupsFile)
    


def test_SMV_2(clf, sw, dataset, groups, without, dssp):
    cq = 0
    cqp = 0
    cc = 0
    sov = 0
    q = 18
    qq = 0
    
    protCodes = []
    for s in groups[without]:
        protCodes.append(s)

    for p in protCodes:
        
        sec = dataset[p]['sec']
        
        prim = dataset[p]['prim']
        
        #prim = prim[-2:]

        primx = inOutFunctions.merge_sequences(prim)
    
        ins, outs = inOutFunctions.prepare_input_forX(sec, primx, sw, dssp)

        pred = inOutFunctions.display_result(clf.predict(np.array(ins, np.float32)), {0:'X', 1:dssp})
#        print sec
#        print pred
#        print "\n"
        cq += measurePrediction.calcQ(pred, sec, dssp)
        cqp += measurePrediction.calcQpred(pred, sec, dssp)
        cc += measurePrediction.calcC(pred, sec, dssp)
        sovx = measurePrediction.calcSOV(pred, sec, dssp)
        
        if sovx != None:
            sov += sovx
            qq += 1

    return (cq/q, cqp/q, cc/q, sov/qq)

for sw in range(7,17,2):
    print "sw = " + str(sw)
    for dssp in ['H','E','C']:
        print "dssp = " + str(dssp)

        for i in range(7):
            clfH = make_SVM_2(sw, protDict, groups, i, dssp)
            
            print test_SMV_2(clfH, sw, protDict, groups, i, dssp)