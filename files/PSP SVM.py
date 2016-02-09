import svm3psp

step = 1

dataset = 'rs126.fa'

# sliding window
for sw in range(7, 14, 2):
    # number of samples for file
    x = 50
    
    print 'sw = ' + str(sw)
    
    filename = 'dump.pkl'
    trained = False
    
    if trained:
        clf = svm3psp.loadSVM(filename)
    else:
        clf = svm3psp.make_SVM_3(sw, x, dataset)
        #svm3psp.saveSVM(clf, filename)
    
    while x < 70:
        rslt = svm3psp.test_SVM_3(clf, step, x, sw, dataset)
        x += step
        
        print rslt
    



