import nn3psp
import inOutFunctions

def main():
    datasetFile = 'rs126.fa'
    groupsFile = 'RS126/groups.txt'
    
    protDict = inOutFunctions.getProteinDict(datasetFile)
    groups = inOutFunctions.getGroups(groupsFile)
    
    
    #for sw in range(7, 16, 2):
    #    print 'sw = ' + str(sw)
    #    
    #    for x in range(7):
    sw, x = 13, 3
    for x in range(7):
        print x
        ann = nn3psp.make_NN(sw, protDict, groups, x)
        
        print nn3psp.test_NN(ann, sw, protDict, groups, x)
        
if __name__ == "__main__":
    main()