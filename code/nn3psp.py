# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 15:37:44 2016

@author: Vlado
"""

import inOutFunctions
import measurePrediction
import theano

from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD
from keras.models import model_from_json

import numpy as np
import codes

def matrix_to_vector(mat):
    return mat.flatten()
def prepare_for_ann(regions):
    ready_for_ann = []
    for region in regions:
        ready_for_ann.append(matrix_to_vector(region))
    return ready_for_ann
def convert_output(outputs):
    return np.eye(len(outputs))
def winner(output):
    return max(enumerate(output), key=lambda x: x[1])[0]
    
def create_ann(hidden_neurons, sw):   
    ann = Sequential()

    ann.add(Dense(input_dim=len(codes.aac)*sw, output_dim=hidden_neurons,init="glorot_uniform"))
    ann.add(Activation("sigmoid"))
    ann.add(Dense(input_dim=hidden_neurons, output_dim=len(codes.alphabeth),init="glorot_uniform"))
    ann.add(Activation("sigmoid"))
    
    return ann
    
def train_ann(ann, X_train, y_train):  
    theano.exception_verbosity='high'  
    
    X_train = np.array(X_train, np.float32)
    y_train = np.array(y_train, np.float32)

    sgd = SGD(lr=0.01, momentum=0.9)
    ann.compile(loss='mean_squared_error', optimizer=sgd)

    ann.fit(X_train, y_train, nb_epoch=150, batch_size=1, verbose = 0, validation_data=None, shuffle=False, show_accuracy = False) 
      
    return ann

def make_NN_(sw, x, filename):
    ann = create_ann(2, sw)
    
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
        
        prim = inOutFunctions.merge_sequences(prim)
        
        #prim = "ADTRIG"
        #sec = "CCEEEE"
        
        ins, outs = inOutFunctions.convert_inputNN(sec, prim, sw)
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    f.close()

    ann = train_ann(ann, inputs_train, outputs_train)
    
    return ann
    
def make_NN(sw, dataset, groups, without):
    ann = create_ann(5, sw)
    
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
        ins, outs = inOutFunctions.convert_inputNN(sec, primx, sw)
        
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    ann = train_ann(ann, inputs_train, outputs_train)
    
    return ann
    
def test_NN(ann, sw, dataset, groups, without):
    sum = 0 
    q3 = 0
    qh = 0
    qhp = 0
    qe = 0
    qep = 0
    qc = 0
    qcp = 0
    sovh, zh = 0, 0.01
    sove, ze = 0, 0.01
    sovc, zc = 0, 0.01
    z = 126/7

    protCodes = []
    for s in groups[without]:
        protCodes.append(s)

    for p in protCodes:
        
        sec = dataset[p]['sec']
        
        prim = dataset[p]['prim']
        
        #prim = prim[-2:]
        prim = inOutFunctions.merge_sequences(prim)
        ins, outs = inOutFunctions.convert_inputNN(sec, prim, sw)
        pred = ann.predict(np.array(ins, np.float32))
        
        predx = []
        for p in pred:
            predx.append(winner(p))
        pred = inOutFunctions.display_result(predx, codes.alphabeth)

        sum += measurePrediction.compare(pred, sec)
        
        q3 += measurePrediction.calcQ3(pred, sec)
        
        qh += measurePrediction.calcQ(pred, sec, 'H')
        qhp += measurePrediction.calcQpred(pred, sec, 'H')
        qe += measurePrediction.calcQ(pred, sec, 'E')
        qep += measurePrediction.calcQpred(pred, sec, 'E')
        qc += measurePrediction.calcQ(pred, sec, 'C')
        qcp += measurePrediction.calcQpred(pred, sec, 'C')
        
        _sovh = measurePrediction.calcSOV(pred, sec, 'H')
        _sove = measurePrediction.calcSOV(pred, sec, 'E')
        _sovc = measurePrediction.calcSOV(pred, sec, 'C')
        
        if _sovh != None:
            sovh += _sovh
            zh += 1
        if _sove != None:
            sove += _sove
            ze += 1
        if _sovc != None:
            sovc += _sovc
            zc += 1
    
    return (q3/z, qh/z, qhp/z, qe/z, qep/z, qc/z, qcp/z, sovh/zh, sove/ze, sovc/zc)
    
def test_NN_(ann, z, x, sw, filename):
    f = open(filename, 'r')
    sum = 0 
    q3 = 0
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

        if i >= x:
            prim = inOutFunctions.merge_sequences(prim)
            ins, outs = inOutFunctions.convert_inputNN(sec, prim, sw)
            pred = ann.predict(np.array(ins, np.float32))
            
            predx = []
            for p in pred:
                predx.append(winner(p))
            pred = inOutFunctions.display_result(predx, codes.alphabeth)

            sum += measurePrediction.compare(pred, sec)
            
            q3 += measurePrediction.calcQ3(pred, sec)
            
            qh += measurePrediction.calcQ(pred, sec, 'H')
            qhp += measurePrediction.calcQpred(pred, sec, 'H')
            qe += measurePrediction.calcQ(pred, sec, 'E')
            qep += measurePrediction.calcQpred(pred, sec, 'E')
            qc += measurePrediction.calcQ(pred, sec, 'C')
            qcp += measurePrediction.calcQpred(pred, sec, 'C')
            
            _sovh = measurePrediction.calcSOV(pred, sec, 'H')
            _sove = measurePrediction.calcSOV(pred, sec, 'E')
            _sovc = measurePrediction.calcSOV(pred, sec, 'C')
            
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

    return (q3/z, qh/z, qhp/z, qe/z, qep/z, qc/z, qcp/z, sovh/zh, sove/ze, sovc/zc)

def saveNN(ann, filename):
    json_string = ann.to_json()
    f = open(filename, 'w')
    f.write(json_string)

def loadNN(filename):
    f = open(filename, 'r')
    json_string = ''
    
    while True:
        s = f.readline();
        if s == '':
            break
        json_string += s
    
    return model_from_json(json_string)