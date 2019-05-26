fin = open("BLOSUM-45-part")
lines = fin.readlines()
NumOfLines = len(lines)  # because I use range() to construct
NumOfElements = len(lines[0].replace("\n", "").split(","))
BLOSUM = [[0 for i in range(NumOfElements)] for i in range(NumOfLines)]
for i in range(NumOfLines):
    BLOSUM[i] = lines[i].replace("\n", "").split(",")
# print(BLOSUM)
print(fin.name, "imported.")
# finish import BLOSUM
"""
This just an example , not a direct input
['', 'I', 'P', 'G', 'A', 'W', 'D']
['V', '3', '-3', '-3', '0', '-3', '-3']
['G', '-4', '-2', '7', '0', '-2', '-1']
['W', '-2', '-3', '-2', '-2', '15', '-4']
['A', '-1', '-1', '0', '5', '-2', '-2']
['D', '-4', '-1', '-1', '-2', '-4', '7']
"""
# read two sequence
sequence1 ="AAAAA" #"IPGAWD"
# sequence1=input("Please input the first sequence:")
sequence1="0"+sequence1
print("sequence1:", sequence1)

# sequence2=input("Please input the second sequence:")
sequence2 = "AAAA"# "VGAWAD"
sequence2="0"+sequence2
print("sequence2:", sequence2)
# finish reading two sequence
# build score matrix
GAP = -8
score = [[0 for i in range(len(sequence1))] for i in range(len(sequence2))]
# use a 4-D list to represent whether two node are connected
connectivity= [[[[False for i in range(len(sequence1))] for i in range(len(sequence2))] for i in range(len(sequence1))] for i in range(len(sequence2))]
# initialize score matrix
score[0][0]= 0# debugging
for i in range(1, len(sequence2)):
    score[i][0]= score[i-1][0]+GAP
    connectivity[i][0][i-1][0]= True
    connectivity[i-1][0][i][0]= True
for i in range(1, len(sequence1)):
    score[0][i]= score[0][i-1]+GAP
    connectivity[0][i][0][i-1]= True
    connectivity[0][i-1][0][i]= True

def valueFromBLOSUM(i1, i2):
    global score
    global BLOSUM
    global sequence1
    global sequence2
    charX= sequence1[i2]   # the key to find the value
    charY= sequence2[i1]   # the key to find the value
    index1= -1   # the index of char in BLOSUM
    index2= -1   # the index of char in BLOSUM
    # find the corresponding index of char
    for i in range(NumOfLines):
        if BLOSUM[i][0] == charY:
            index2= i
    for i in range(NumOfElements):
        if BLOSUM[0][i] == charX:
            index1= i
    if index1 == -1 or index2 == -1:
        print("Error: can't find the value in BLOSUM matrix of :",
              charX, " ", charY, ".")
        return 0
    return float(BLOSUM[index2][index1])


for i1 in range(1, len(sequence2)):
    for i2 in range(1, len(sequence1)):
        score[i1][i2]= max(score[i1-1][i2]+GAP, score[i1]
                            [i2-1]+GAP, valueFromBLOSUM(i1, i2))
        if score[i1][i2] == score[i1-1][i2]+GAP:
            connectivity[i1][i2][i1-1][i2]= True
            connectivity[i1-1][i2][i1][i2]= True
        if score[i1][i2] == score[i1][i2-1]+GAP:
            connectivity[i1][i2][i1][i2-1]= True
            connectivity[i1][i2-1][i1][i2]= True
        if score[i1][i2] == valueFromBLOSUM(i1, i2):
            connectivity[i1][i2][i1-1][i2-1]= True
            connectivity[i1-1][i2-1][i1][i2]= True
# print connectivity
for i1 in range(len(sequence2)):
    for i2 in range(len(sequence1)):
        for i3 in range(len(sequence2)):
            for i4 in range(len(sequence1)):
                if connectivity[i1][i2][i3][i4]is True:
                    print("(",i1,",",i2,"),(",i3,",",i4,")","connected.")
# finish creating the score matrix
methodCnt= 0


def printAnswer(i1, i2, pathX, pathY):
    print("i1:", i1, " i2:", i2)
    print(pathX)
    print(pathY)
    global score
    global BLOSUM
    global sequence1
    global sequence2
    global methodCnt
    for i3 in range(len(sequence2)):
        for i4 in range(len(sequence1)):
            if connectivity[i1][i2][i3][i4] == True and i3 <= i1 and i4 <= i2:
                if i3 == i1-1 and i4 == i2-1:  # come from diag
                    pathX.insert(0, sequence1[i2])
                    pathY.insert(0, sequence2[i1])
                    # printAnswer(i3, i4, pathX.copy(), pathY.copy())
                elif i3 == i1 and i4 == i2-1:   # from left
                    pathX.insert(0, sequence1[i2])
                    pathY.insert(0, "-")
                    # printAnswer(i3, i4, pathX.copy(), pathY.copy())
                elif i3 == i1-1 and i4 == i2:   # from up
                    pathX.insert(0, "-")
                    pathY.insert(0, sequence2[i1])
                else:
                    print("Error: didn't find the last element.")
                printAnswer(i3, i4, pathX.copy(), pathY.copy())
    if i1 == 0 and i2 == 0:
        print("Here is the method NO.", methodCnt+1, ":")
        print(pathX)
        print(pathY)
        methodCnt= methodCnt+1


pathX= []
pathY= []
printAnswer(len(sequence2)-1, len(sequence1)-1, pathX.copy(), pathY.copy())
i = 0
