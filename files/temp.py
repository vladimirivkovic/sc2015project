# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 14:40:03 2016

@author: Vlado
"""

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD

model = Sequential()
model.add(Dense(input_dim=1000, output_dim=10,init="glorot_uniform"))
model.add(Activation('softmax'))

model.compile(optimizer='sgd', loss='mse')

X_train = []
y_train = []
for i in range(1000):
    X_train.append([i/100, i/10, i%10])
    y_train.append(i%10)

model.fit(X_train, y_train, nb_epoch=3, batch_size=10, verbose=1, shuffle="batch")

print model.predict([3, 3, 3])
