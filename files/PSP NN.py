import nn3psp

filename = 'rs126.fa'
sw = 3
x = 1

nn = nn3psp.make_NN(sw, x, filename)

#rslt = nn3psp.test_NN(nn, 1, x, sw, filename)