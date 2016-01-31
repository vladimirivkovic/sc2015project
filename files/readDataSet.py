f1 = open('Proteins.fa', 'r')
f2 = open('SSpro.dssp', 'r')

proteins = {}
p = ""
struct = ""

while True:
    p = f1.readline()
    if p == "":
        break
        
    struct = f1.readline()
    if proteins.has_key(p) == False:
        proteins[p] = {}
    proteins[p]["prim"] = struct

while True:
    p = f2.readline()
    if p == "":
        break
        
    struct = f2.readline()
    if proteins.has_key(p) == False:
        proteins[p] = {}
    proteins[p]["sec"] = struct

len(proteins.keys())

f1.close()
f2.close()

f3 = open('dataSet.txt', 'w')
for x in proteins:
    f3.write(x)
    f3.write(proteins[x]["prim"])
    f3.write(proteins[x]["sec"])
    
    if len(proteins[x]["prim"]) != len(proteins[x]["sec"]):
        print('error')