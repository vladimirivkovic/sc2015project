from sklearn import svm
import collections
import numpy as np
import scipy as sc

#amino acid sinle letter codes
aac = {}

rest = 'Z';

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
aac[rest] = codes[20]

alphabeth = ['H', 'E', 'C']
alph = {}
alph['H'] = 0
alph['E'] = 1
alph['C'] = 2

# prepare training data for 3-class SVM
def convert_input(sec, prim, sw):
    length = len(prim)
    prefix = ""
    sufix = ""
    for q in range(sw/2):
        prefix += rest
        sufix += rest
    primx = prefix + prim + sufix
    ins = []
    outs = []
    for j in range(length):
        inputs = []
        for k in range(j, j + sw):
            if aac.has_key(primx[k]):
                inputs.append(aac[primx[k]])
            else:
                inputs.append(aac[rest])
        ins.append(np.array(inputs).flatten())
        outs.append(alph[sec[j]])
    return (ins, outs)

def make_SVM_3(sw, x):
    inputs_train = []
    outputs_train = []

    #read dataset file
    f = open('dataSet.txt', 'r')
    for i in range(x):
        f.readline()
        prim = f.readline().strip()
        sec = f.readline().strip()
        ins, outs = convert_input(sec, prim, sw)
        for q in ins:
            inputs_train.append(q)
        for q in outs:
            outputs_train.append(q)

    f.close()

    clf = svm.SVC(C=1.5, gamma=0.1)
    clf.fit(inputs_train, outputs_train)
    
    return clf

# sliding window
sw = 11
# number of samples for file
x = 50

clf = make_SVM_3(sw, x)

def display_result(outputs, alphabet):
    result = ''
    for x in outputs:
        result += alphabet[x]
    return result

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

def test_SVM_3(clf, z, x):
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
            ins, outs = convert_input(sec, prim, sw)
            pred = display_result(clf.predict(np.array(ins, np.float32)), alphabeth)
            sum += compare(pred, sec)
            
            qh += calcQ(pred, sec, 'H')
            qhp += calcQpred(pred, sec, 'H')
            qe += calcQ(pred, sec, 'E')
            qep += calcQpred(pred, sec, 'E')
            qc += calcQ(pred, sec, 'C')
            qcp += calcQpred(pred, sec, 'C')

    print "total"
    return (qh/z, qhp/z, qe/z, qep/z, qc/z, qcp/z)

sw = 11
z = 200
test_SVM_3(clf, z, x)

def prepare_input_for(sec, prim, sw, struct):
    length = len(prim)
    
    prefix = ""
    sufix = ""
    for q in range(sw/2):
        prefix += rest
        sufix += rest
        
    primx = prefix + prim + sufix
    ins = []
    outs = []
    
    for j in range(length):
        inputs = []
        
        for k in range(j, j + sw):
            if aac.has_key(primx[k]):
                inputs.append(aac[primx[k]])
            else:
                inputs.append(aac[rest])
                
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
        prefix += rest
        sufix += rest
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
            if aac.has_key(primx[k]):
                inputs.append(aac[primx[k]])
            else:
                inputs.append(aac[rest])
        ins.append(np.array(inputs).flatten())
        if sec[j] == sx:
            outs.append(1)
        else:
            outs.append(0)
        sec1 += sec[j]
    return (ins, outs, sec1)

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
            pred = display_result(clfx.predict(np.array(ins, np.float32)), {0:'X', 1:dssp})
#             print sec
#             print pred
#             print "\n"
            cq += calcQ(pred, sec, dssp)
            cqp += calcQpred(pred, sec, dssp)

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

    pred = display_result(clf_EC.predict(np.array(ins, np.float32)), {0:sy, 1:sx})
    if i > z:
        print sec
        print pred
        print compare(sec, pred)

f = open('dataSet.txt', 'r')

w = 10

for i in range(z+w):
    f.readline()
    prim = f.readline().strip()
    sec = f.readline().strip()
    
    if i > z:
        ins, outs = prepare_input_for(sec, prim, sw, dssp)
        pred = clf_H.predict(np.array(ins, np.float32))
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
        
        print compare(sec, preds)

