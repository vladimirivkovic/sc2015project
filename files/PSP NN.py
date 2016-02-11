import nn3psp

filename = 'rs126.fa'
nnfn = 'nn_dump'
step = 1


# sliding window
for sw in range(9, 10, 2):
    # number of samples for file
    x = 50
    
    print 'sw = ' + str(sw)

    trained = False    
    
    if trained:
        nn = nn3psp.loadNN(nnfn)
    else:
        nn = nn3psp.make_NN(sw, x, filename)
        nn3psp.saveNN(nn, nnfn)
    
    q3 = 0
    while x < 100:
        rslt = nn3psp.test_NN(nn, step, x, sw, filename)
        x += step
        
        print rslt
        
        q3 += rslt[0]
    
    print q3/50