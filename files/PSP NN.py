#import potrebnih biblioteka
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy.spatial import distance

# keras
from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD

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

hidden_neurons = 2
sw = 17

def create_ann():
    
    ann = Sequential()
    # Postavljanje slojeva neurona mreže 'ann'
    ann.add(Dense(input_dim=21*sw, output_dim=hidden_neurons,init="glorot_uniform"))
    ann.add(Activation("sigmoid"))
    ann.add(Dense(input_dim=hidden_neurons, output_dim=3,init="glorot_uniform"))
    ann.add(Activation("sigmoid"))
    return ann
    
def train_ann(ann, X_train, y_train):
    X_train = np.array(X_train, np.float32)
    y_train = np.array(y_train, np.float32)
   
    # definisanje parametra algoritma za obucavanje
    sgd = SGD(lr=0.01, momentum=0.9)
    ann.compile(loss='mean_squared_error', optimizer=sgd)

    # obucavanje neuronske mreze
    ann.fit(X_train, y_train, nb_epoch=50, batch_size=1, verbose = 0, shuffle=False, show_accuracy = False) 
      
    return ann

#amino acid sinle letter codes
aac = {}
codes = np.eye(21)
aac['G'] = codes[0]
aac['A'] = codes[1]
aac['L'] = codes[2]
aac['M'] = codes[3]
aac['F'] = codes[4]
aac['W'] = codes[5]
aac['K'] = codes[6]
aac['Q'] = codes[7]
aac['E'] = codes[8]
aac['S'] = codes[9]
aac['P'] = codes[10]
aac['V'] = codes[11]
aac['C'] = codes[12]
aac['I'] = codes[13]
aac['Y'] = codes[14]
aac['H'] = codes[15]
aac['R'] = codes[16]
aac['N'] = codes[17]
aac['D'] = codes[18]
aac['T'] = codes[19]
aac['ERROR'] = codes[20]

alphabeth = ['H', 'E', 'C']
alph = {}
alph['H'] = [1,0,0]
alph['E'] = [0,1,0]
alph['C'] = [0,0,1]

def convert_input(sec, prim, sw):
    length = len(prim)
    ins = []
    outs = []
    for j in range(length - sw):
        inputs = []
        for k in range(j, j+sw):
            if aac.has_key(prim[k]):
                inputs.append(aac[prim[k]])
            else:
                inputs.append(aac['ERROR'])
        ins.append(np.array(inputs).flatten())
        outs.append(alph[sec[j+sw/2]])
    return (ins, outs)

#convert_input('TWTYILRQGD', 'CCEEEEEHHH', 3)

#read dataset file
x = 20

inputs_train = []
outputs_train = []

f = open('dataSet.txt', 'r')
for i in range(x):
    f.readline()
    prim = f.readline()
    sec = f.readline()
    ins, outs = convert_input(sec, prim, sw)
    for q in ins:
        inputs_train.append(q)
    for q in outs:
        outputs_train.append(q)
    
f.close()
    
#print inputs_train
    
ann = create_ann()
ann = train_ann(ann, inputs_train, outputs_train)

def display_result(outputs, alphabet):
    result = ''
    for x in outputs:
        result += alphabet[winner(x)]
    return result

def compare(a, b, s):
    l = len(b)
    x = 0.0
    y = 0.0
    for i in range(l - s):
        if a[i] == b[i + s/2]:
            x += 1
        else:
            y += 1
    return x/(x+y)

f = open('dataSet.txt', 'r')

z = 100
sum = 0

for i in range(x+z):
    f.readline()
    prim = f.readline()
    sec = f.readline()
    if i > x:
        ins, outs = convert_input(sec, prim, sw)
        pred = display_result(ann.predict(np.array(ins, np.float32)), ['H', 'E', 'C'])
        #print "XXXXXXXX" + pred + "XXXXXXXX"
        #print sec
        #print compare(pred, sec, sw)
        sum += compare(pred, sec, sw)

print sum/z

