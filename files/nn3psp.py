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
    
    return ann
    
def train_ann(ann, X_train, y_train):  
    theano.exception_verbosity='high'  
    
    X_train = np.array(X_train, np.float32)
    y_train = np.array(y_train, np.float32)

    sgd = SGD(lr=0.01, momentum=0.9)
    ann.compile(loss='mean_squared_error', optimizer=sgd)

    ann.fit(X_train, y_train, nb_epoch=150, batch_size=1, verbose = 0, validation_data=None, shuffle=False, show_accuracy = False) 
      
    return ann

def make_NN(sw, x, filename):
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
        
        ins, outs = inOutFunctions.convert_inputX(sec, prim, sw)
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    f.close()
    
    print np.array(inputs_train, np.float32)
    print np.array(outputs_train, np.float32)

    ann = train_ann(ann, inputs_train, outputs_train)
    
    return ann
    
def test_NN(ann, z, x, sw, filename):
    f = open(filename, 'r')
    sum = 0    
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
            ins, outs = inOutFunctions.convert_inputX(sec, prim, sw)
            pred = inOutFunctions.display_result(ann.predict(np.array(ins, np.float32)), codes.alphabeth)
            print pred
            print sec
            sum += measurePrediction.compare(pred, sec)
            
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

    return (qh/z, qhp/z, qe/z, qep/z, qc/z, qcp/z, sovh/zh, sove/ze, sovc/zc)