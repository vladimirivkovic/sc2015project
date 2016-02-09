# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:37:14 2016

@author: Vlado
"""
import numpy as np

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

alphNN = {}
alphNN['H'] = [1, 0, 0]
alphNN['E'] = [0, 1, 0]
alphNN['C'] = [0, 0, 1]