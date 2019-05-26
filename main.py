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
# sequence1=input("Please input the first sequence:")
sequence1 = "IPGAWD"
print("sequence1:", sequence1)
# sequence2=input("Please input the second sequence:")
sequence2 = "VGAWAD"
print("sequence2:", sequence2)
# finish reading two sequence
# build score matrix
GAP = -8
score = [[0 for i in range(NumOfElements)] for i in range(NumOfLines)]
for i in range(NumOfLines):
    if(i is not 1):
        score[i][0] = score[i-1][0]+GAP
        score[0][i] = score[0][i-1]+GAP
    else:
        score[0][0] = 0
        score[1][0] = GAP
        score[0][1] = GAP
# print(score)


def valueFromBLOSUM(i1, i2):
    global score
    global BLOSUM
    global sequence1
    global sequence2
    charX = sequence1[i1]   # the key to find the value
    charY = sequence2[i2]   # the key to find the value
    index1 = -1   # the index of char in BLOSUM
    index2 = -1   # the index of char in BLOSUM
    # find the corresponding index of char
    for i in range(NumOfLines):
        if BLOSUM[i][0] == charY:
            index2 = i
    for i in range(NumOfElements):
        if BLOSUM[0][i] == charX:
            index1 = i
    if index1 == -1 or index2 == -1:
        print("Error: can't find the value in BLOSUM matrix of :",
              charX, " ", charY, ".")
        return 0
    return float(BLOSUM[index2][index1])


# use a 4-D list to represent whether two node are connected
connextivity = [[[[False for i in range(NumOfElements)] for i in range(
    NumOfLines)] for i in range(NumOfElements)] for i in range(NumOfLines)]
for i1 in range(NumOfLines):
    for i2 in range(NumOfLines):
        score[i1][i2] = max(score[i1-1][i2]+GAP, score[i1]
                            [i2-1]+GAP, valueFromBLOSUM(i1, i2))
        if score[i1][i2] == score[i1-1][i2]+GAP:
            connextivity[i1][i2][i1-1][i2] = True
            connextivity[i1-1][i2][i1][i2] = True
        if score[i1][i2] == score[i1][i2-1]+GAP:
            connextivity[i1][i2][i1][i2-1] = True
            connextivity[i1][i2-1][i1][i2] = True
        if score[i1][i2] == valueFromBLOSUM(i1, i2):
            connextivity[i1][i2][i1-1][i2-1] = True
            connextivity[i1-1][i2-1][i1][i2] = True
# print(connextivity)
# finish creating the score matrix

methodCnt = 0


def printAnswer(i1, i2, pathX, pathY, situation):
    global score
    global BLOSUM
    global sequence1
    global sequence2
    global connextivity
    global methodCnt
    if situation == 2:  # from diag
        pathX.insert(0,sequence1[i1])
        pathY.insert(0,sequence2[i2])
    if situation == 1:  # from left
        pathX.insert(0,sequence1[i1])
        pathY.insert(0,"-")
    if situation == 3:  # from up
        pathX.insert(0,"-")
        pathY.insert(0,sequence2[i2])
    if i1 == 0 and i2 == 0:
        print("Here is the method NO.", methodCnt, ".")
        print(pathX)
        print(pathY)
        methodCnt = methodCnt+1
    else:
        for i3 in range(NumOfLines):
            for i4 in range(NumOfElements):
                if connextivity[i1][i2][i3][i4] == True and i3<=i1 and i4<=i2:
                    if i1 == i1-1 and i4 == i2-1:  # come from diag
                        printAnswer(i3, i4, pathX.copy(), pathY.copy(), 2)
                    elif i3 == i1 and i4 == i2-1:
                        printAnswer(i3, i4, pathX.copy(), pathY.copy(), 1)
                    else:
                        printAnswer(i3, i4, pathX.copy(), pathY.copy(), 3)


pathX = []
pathY = []
printAnswer(len(sequence1)-1, len(sequence2)-1, pathX.copy(), pathY.copy(), 2)
