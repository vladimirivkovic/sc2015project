import svm3psp
import inOutFunctions

datasetFile = 'rs126.fa'
groupsFile = 'RS126/groups.txt'

protDict = inOutFunctions.getProteinDict(datasetFile)
groups = inOutFunctions.getGroups(groupsFile)

def main():  
    # sliding window
    for sw in range(7, 16, 2):
        
        print 'sw = ' + str(sw)
        
        for x in range(7):
            clf = svm3psp.make_SVM_3X(sw, protDict, groups, x)
            
            print svm3psp.test_SVM_3X(clf, sw, protDict, groups, x)

def test(trained):
    sw = 15
    x = 2
    
    filename = 'dump.pkl'
    
    if trained:
        clf = svm3psp.loadSVM(filename)
    else:
        clf = svm3psp.make_SVM_3X(sw, protDict, groups, x)
        svm3psp.saveSVM(clf, filename)
            
    print svm3psp.test_SVM_3X(clf, sw, protDict, groups, x)
        
    

if __name__ == "__main__":
    test(True)


