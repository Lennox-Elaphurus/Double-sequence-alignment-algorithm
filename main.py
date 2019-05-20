MAX=27
fin = open("BLOSUM-45-part")
lines=fin.readlines()
length=len(lines)-1
BLOSUMtemp= [[0 for i in range(length)] for i in range(length)]
for i in range(length):
    BLOSUMtemp[i]=lines[i].replace("\n","").split(",")
BLOSUM=[[0 for i in range(MAX)] for i in range(MAX)]
print(BLOSUM)
print(fin.name,"imported.")
# finish import BLOSUM
"""
['', 'I', 'P', 'G', 'A', 'W', 'D']
['V', '3', '-3', '-3', '0', '-3', '-3']
['G', '-4', '-2', '7', '0', '-2', '-1']
['W', '-2', '-3', '-2', '-2', '15', '-4']
['A', '-1', '-1', '0', '5', '-2', '-2']
"""
# read two sequence
sequence1=input("Please input the first sequence:")
# print(sequence1)
sequence2=input("Please input the second sequence:")
# finish reading two sequence
# build score matrix
GAP=-8
score=[[0 for i in range(length)] for i in range(length)]
for i in range(length):
    if(i is not 1):
        score[i][0]=score[i-1][0]+GAP
        score[0][i]=score[0][i-1]+GAP
    else:
        score[0][0]=0
        score[1][0]=GAP
        score[0][1]=GAP
# print(score)
def valueFromBLOSUM(i1,i2):
    global score
    global BLOSUMtemp
    global sequence1
    global sequence2
    charX=sequence1[i1]
    charY=sequence1[i1]

    return score[i1-1][i2-1]+score
for i1 in range(length):
    for i2 in range(length):
        score[i1][i2]=max(score[i1-1][i2]+GAP,score[i1][i2-1]+GAP,valueFromBLOSUM(i1,i2))
        