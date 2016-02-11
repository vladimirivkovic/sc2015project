import svm3psp
import inOutFunctions

step = 1

datasetFile = 'rs126.fa'
groupsFile = 'RS126/groups.txt'

protDict = inOutFunctions.getProteinDict(datasetFile)
groups = inOutFunctions.getGroups(groupsFile)

# sliding window
for sw in range(9, 16, 2):
    # number of samples for file
    x = 6
    
    print 'sw = ' + str(sw)
    
    filename = 'dump.pkl'
    trained = False
    
    for x in range(7):
        if trained:
            clf = svm3psp.loadSVM(filename)
        else:
            clf = svm3psp.make_SVM_3X(sw, protDict, groups, x)
            #svm3psp.saveSVM(clf, filename)
        
    #    q3 = 0
    #    while x < 110:
    #        rslt = svm3psp.test_SVM_3(clf, step, x, sw, dataset)
    #        x += step
    #        
    #        #print rslt
    #    
    #        q3 += rslt[0]
    #    
    #    print q3/30
        print svm3psp.test_SVM_3X(clf, sw, protDict, groups, x)[0]


