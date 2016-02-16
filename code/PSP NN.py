import nn3psp
import inOutFunctions

datasetFile = 'rs126.fa'
groupsFile = 'RS126/groups.txt'

protDict = inOutFunctions.getProteinDict(datasetFile)
groups = inOutFunctions.getGroups(groupsFile)


#for sw in range(7, 16, 2):
#    print 'sw = ' + str(sw)
#    
#    for x in range(7):
sw, x = 11, 4

ann = nn3psp.make_NN(sw, protDict, groups, x)

print nn3psp.test_NN(ann, sw, protDict, groups, x)