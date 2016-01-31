import svm3psp

step = 50


# sliding window
for sw in range(5, 17, 2):
    # number of samples for file
    x = 40
    
    print 'sw = ' + str(sw)
    
    filename = 'dump.pkl'
    trained = False
    
    if trained:
        clf = svm3psp.loadSVM(filename)
    else:
        clf = svm3psp.make_SVM_3(sw, x)
        svm3psp.saveSVM(clf, filename)
    
    z = x + step
    while z < 500:
        rslt = svm3psp.test_SVM_3(clf, z, x, sw)
        z += step
        x += step
        
        print rslt



