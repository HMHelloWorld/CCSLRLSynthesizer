import copy
import CCSL
#Check Relation
def checkRelation(leftClock,rightClock,relType):
    if relType == 5 or relType == 6:
        relType -= 4
        clock = leftClock
        leftClock = rightClock
        rightClock = clock
    elif relType == 7:
        return True
    check = {0:checkCoincidence,
             1:checkPrecedence,
             2:checkCausality,
             3:checkExclusion,
             4:checkSubclock,
             5:checkAlternate}
    return check.get(relType)(leftClock,rightClock)

def checkCoincidence(leftClock,rightClock):
    if len(leftClock) != len(rightClock):
        return False
    for i in range(len(leftClock)):
        if leftClock[i] != rightClock[i]:
            return False
    return True

def checkPrecedence(leftClock,rightClock):
    if len(leftClock) < len(rightClock):
        return False
    for i in range(len(rightClock)):
        if leftClock[i] >= rightClock[i]:
            return False
    return True

def checkCausality(leftClock,rightClock):
    if len(leftClock) < len(rightClock):
        return False
    for i in range(len(rightClock)):
        if leftClock[i] > rightClock[i]:
            return False
    return True

def checkExclusion(leftClock,rightClock):
    lenLeft = len(leftClock)
    lenRight = len(rightClock)
    i = 0
    j = 0
    while i < lenLeft and j < lenRight:
        if leftClock[i] == rightClock[j]:
            return False
        if leftClock[i] > rightClock[j]:
            j += 1
        else:
            i += 1
    return True

def checkSubclock(leftClock,rightClock):
    if len(leftClock) > len(rightClock):
        return False
    lenLeft = len(leftClock)
    lenRight = len(rightClock)
    i = 0
    j = 0
    while i < lenLeft and j < lenRight:
        if leftClock[i] == rightClock[j]:
            i += 1
            j += 1
        elif leftClock[i] < rightClock[j]:
            return False
        else:
            j+=1
    if i < lenLeft:
        return False
    return True

def checkAlternate(leftClock,rightClock):
    lenLeft = len(leftClock)
    lenRight = len(rightClock)
    if abs(lenLeft - lenRight) > 1 or lenLeft < lenRight :
        return False
    for i in range(0, lenRight):
        if leftClock[i] >= rightClock[i]:
            return False
    if lenLeft > lenRight:
        if rightClock[lenRight-1] <= leftClock[lenLeft-1]:
            return False
    return True

#Check Expression
def getExpressionClock(expression,traces,spec,traceLen):
    type = expression.type
    leftClk = expression.clockArr[0]
    if type == 4 or type == 5:
        rightClk = expression.clockArr[0]
    else:
        rightClk = expression.clockArr[1]
    leftId = spec.getClockId(leftClk)
    rightId = spec.getClockId(rightClk)
    getExp = {0: getUnionClock,
             1: getIntersectionClock,
             2: getSupremumClock,
             3: getInfimumClock,}
    getExpExtend = {4: getDelayClock,
              5: getPeriodicClock,
              6: getDelayForClock }

    clkTraces = []
    if type <= 3:
        for trace in traces:
            expTrace= getExp.get(type)(trace[leftId],trace[rightId])
            clkTraces.append(expTrace)
    else:
        for trace in traces:
            expTrace= getExpExtend.get(type)(trace[leftId],trace[rightId],expression.addition,traceLen)
            clkTraces.append(expTrace)

    return clkTraces

def getUnionClock(leftClock,rightClock):
    resultClk = []
    lenLeft = len(leftClock)
    lenRight = len(rightClock)
    i = 0
    j = 0
    while i < lenLeft and j < lenRight:
        if leftClock[i] == rightClock[j]:
            resultClk.append(leftClock[i])
            i += 1
            j += 1
        elif leftClock[i] < rightClock[j]:
            resultClk.append(leftClock[i])
            i += 1
        else:
            resultClk.append(rightClock[j])
            j+=1
    if j < lenRight:
        while j < lenRight:
            resultClk.append(rightClock[j])
            j += 1
    elif i < lenLeft:
        while i < lenLeft:
            resultClk.append(leftClock[i])
            i += 1
    return resultClk

def getIntersectionClock(leftClock,rightClock):
    resultClk = []
    lenLeft = len(leftClock)
    lenRight = len(rightClock)
    i = 0
    j = 0
    while i < lenLeft and j < lenRight:
        if leftClock[i] == rightClock[j]:
            resultClk.append(leftClock[i])
            i += 1
            j += 1
        elif leftClock[i] < rightClock[j]:
            i += 1
        else:
            j+=1
    return resultClk

def getSupremumClock(leftClock,rightClock):
    resultClk = []
    count = min(len(leftClock),len(rightClock))
    i = 0
    while i < count:
        if leftClock[i] >= rightClock[i]:
            resultClk.append(leftClock[i])
        else:
            resultClk.append(rightClock[i])
        i+=1
    return resultClk

def getInfimumClock(leftClock,rightClock):
    resultClk = []
    count = min(len(leftClock), len(rightClock))
    i = 0
    while i < count:
        if leftClock[i] <= rightClock[i]:
            resultClk.append(leftClock[i])
        else:
            resultClk.append(rightClock[i])
        i += 1
    if i == len(leftClock):
        while i < len(rightClock):
            resultClk.append(rightClock[i])
            i+=1
    else:
        while i < len(leftClock):
            resultClk.append(leftClock[i])
            i+=1
    return resultClk

def getDelayClock(leftClock,rightClock,addition,traceLen):
    resultClk = []
    count = len(leftClock)
    i = 0
    for i in range(count - addition):
        clk = leftClock[i + addition]
        if clk <= traceLen:
            resultClk.append(clk)

    return resultClk

def getPeriodicClock(leftClock,rightClock,addition,traceLen):
    resultClk = []
    count = len(leftClock)/addition
    for i in range(count):
        resultClk.append(leftClock[(i+1)*addition - 1])
    return resultClk

def getDelayForClock(leftClock,rightClock,addition,traceLen):
    resultClk = []
    leftCount = len(leftClock)
    rightCount = len(rightClock)
    i = addition
    j = 0
    while i < rightCount and j < leftCount:
        if j == 0 :
            if leftClock[j] <= rightClock[i - addition]:
                resultClk.append(rightClock[i])
                j = j + 1
                i = i + 1
            else:
                i = i + 1
        else:
            if leftClock[j] <= rightClock[i - addition] and leftClock[j] > rightClock[i - addition - 1]:
                resultClk.append(rightClock[i])
                j = j + 1
                i = i + 1

            # elif leftClock[j] <= rightClock[i - addition]:
            #     j = j + 1
            else:
                i = i + 1
    return resultClk

#Induction
def holeNetworkInit(traceArr,ccslSpec):
    uncertainExps = []
    for expression in ccslSpec.expressions:
        uncertainExps.append(expression)
    traceArr,uncertainExps = expressionTraceExtend(traceArr,ccslSpec,uncertainExps)
    initNet = []
    clkCount = ccslSpec.getClockCount()
    lenArr = clockLengthSort(traceArr)
    for hole in ccslSpec.expClkHole:
        arr = getExpClkSelArr(hole,lenArr,ccslSpec)
        initNet.append(arr)
    for hole in ccslSpec.expOptHole:
        arr = getExpOptSelArr(hole, lenArr, ccslSpec)
        initNet.append(arr)
    for hole in ccslSpec.relOptHole:
        type = hole.holeType
        if type == 0:
            leftId = ccslSpec.getClockId(hole.clockArr[0])
            rightId = ccslSpec.getClockId(hole.clockArr[1])
            arr = []
            if (len(traceArr[0][leftId]) == 0 or traceArr[0][leftId][0] != -1) and (
                    len(traceArr[0][rightId]) == 0 or traceArr[0][rightId][0] != -1):
                control = traceLengthInduction(traceArr, leftId, rightId)
                # if control == -2:
                #     arr = [-1, -1, -1, 0.0, -1, -1, -1, 0.0]
                # elif control > 0:
                #     arr = [-1, 0.0, 0.0, 0.0, -1, -1, -1, 0.0]
                # elif control == 0:
                #     arr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                # else:
                #     arr = [-1, -1, -1, 0.0, 0.0, 0.0, 0.0, 0.0]
                if control == -2:
                    arr = [-1, -1, -1, 0.0, -1, -1, -1]
                elif control > 0:
                    arr = [-1, 0.0, 0.0, 0.0, -1, -1, -1]
                elif control == 0:
                    arr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                else:
                    arr = [-1, -1, -1, 0.0, 0.0, 0.0, 0.0]
                initNet.append(arr)
            else:
                initNet.append(arr)
    for hole in ccslSpec.relClkHole:
        type = hole.holeType
        if type == 1:
            arr = []
            relType = hole.type
            if hole.clockArr[0] == "":
                clockName = hole.clockArr[1]
            else:
                clockName = hole.clockArr[0]
            if (hole.clockArr[0] == "" and (relType == 1 or relType == 2)) or (hole.clockArr[1] == "" and relType == 4):
                clkSelType = 1
            elif (hole.clockArr[1] == "" and (relType == 1 or relType == 2)) or (hole.clockArr[0] == "" and relType == 4):
                clkSelType = -1
            elif relType == 0:
                clkSelType = 0
            else:
                clkSelType = -2
            for i in range(0,clkCount):
                arr.append(0.0)
            arr = getClkSelArr(arr,lenArr,clkSelType,ccslSpec.getClockId(clockName))
            arr[ccslSpec.getClockId(clockName)] = -1
            initNet.append(arr)
    return initNet,traceArr,uncertainExps

def checkUncertain(clock,spec):
    clockId = spec.getClockId(clock)
    if clockId < len(spec.clocks):
        return False
    elif clockId < len(spec.clocks) + len(spec.expressions):
        exp = spec.expressions[clockId - len(spec.clocks)]
        return checkUncertain(exp.clockArr[0],spec) or checkUncertain(exp.clockArr[1],spec)
    else:
        return True

def checkExpressionUncertain(clock,spec,holeId):
    clockId = spec.getClockId(clock)
    if holeId == clockId:
        return False
    if clockId < len(spec.clocks):
        # eqList = getEqualClockList(spec)
        # clkEqList = []
        #
        # for list in eqList:
        #     for clk in list:
        #         if clock == clk:
        #             clkEqList = list
        #             break
        # clkEq = False
        # for clk in clkEqList:
        #     clkId = spec.getClockId(clk)
        #     if clkId < len(spec.clocks):
        #         clkEq= clkEq or False
        #     if clkId < len(spec.clocks) + len(spec.expressions):
        #         exp = spec.expressions[clkId - len(spec.clocks)]
        #         clkEq= clkEq or checkExpressionUncertain(clk, spec, holeId)
        #         if clkEq:
        #             return clkEq
        #     else:
        #         return True
        return False
    elif clockId < len(spec.clocks) + len(spec.expressions):
        exp = spec.expressions[clockId - len(spec.clocks)]
        return checkExpressionUncertain(exp.clockArr[0],spec,holeId) or checkExpressionUncertain(exp.clockArr[1],spec,holeId)
    else:
        return True

def checkSameRelation(relation,spec):
    equalList = getEqualClockList(spec)
    leftEqualList = []
    rightEqualList = []
    for i in range(0,len(equalList)):
        for j in range(len(equalList[i])):
            if equalList[i][j] == relation.clockArr[0]:
                leftEqualList = equalList[i]
            if equalList[i][j] == relation.clockArr[1]:
                rightEqualList = equalList[i]

    for rel in spec.relations:
        if rel.type == relation.type:
            isLeft = False
            isRight = False
            if relation.clockArr[0] == rel.clockArr[0] or relation.clockArr[0] == rel.clockArr[1]:
                isLeft = True
            else:
                for clock in leftEqualList:
                    if clock == rel.clockArr[0] or clock == rel.clockArr[1]:
                        isLeft = True
                        break
            if relation.clockArr[1] == rel.clockArr[0] or relation.clockArr[1] == rel.clockArr[1]:
                isRight = True
            else:
                for clock in rightEqualList:
                    if clock == rel.clockArr[0] or clock == rel.clockArr[1]:
                        isRight = True
                        break

            if isLeft and isRight:
                return True
    return False
def checkChoseRelation(relation,spec,holeList,actionList,index):
    equalList = getEqualClockList(spec)
    leftEqualList = []
    rightEqualList = []
    for i in range(0, len(equalList)):
        for j in range(len(equalList[i])):
            if equalList[i][j] == relation.clockArr[0]:
                leftEqualList = equalList[i]
            if equalList[i][j] == relation.clockArr[1]:
                rightEqualList = equalList[i]
    for i in range(0,index):
        hole = holeList[i]
        if hole.holeType == 0:
            if actionList[i] == relation.type:
                isLeft = False
                isRight = False
                if relation.clockArr[0] == hole.clockArr[0] or relation.clockArr[0] == hole.clockArr[1]:
                    isLeft = True
                else:
                    for clock in leftEqualList:
                        if clock == hole.clockArr[0] or clock == hole.clockArr[1]:
                            isLeft = True
                            break
                if relation.clockArr[1] == hole.clockArr[0] or relation.clockArr[1] == hole.clockArr[1]:
                    isRight = True
                else:
                    for clock in rightEqualList:
                        if clock == hole.clockArr[0] or clock == hole.clockArr[1]:
                            isRight = True
                            break
                if isLeft and isRight:
                    return True
        elif hole.holeType == 1:
            if actionList[i] == relation.type:
                actionClk = spec.getClockList()[actionList[i]]
                if hole.clockArr[0] == "":
                    relClk = hole.clockArr[1]
                else:
                    relClk = hole.clockArr[0]
                isLeft = False
                isRight = False
                if relation.clockArr[0] == relClk or relation.clockArr[0] == actionClk:
                    isLeft = True
                else:
                    for clock in leftEqualList:
                        if clock == relClk or clock == actionClk:
                            isLeft = True
                            break
                if relation.clockArr[1] == relClk or relation.clockArr[1] == actionClk:
                    isRight = True
                else:
                    for clock in rightEqualList:
                        if clock == relClk or clock == actionClk:
                            isRight = True
                            break
                if isLeft and isRight:
                    return True
    return False

def getEqualClockList(spec):
    equalList = []
    for rel in spec.relations:
        if rel.type == 0:
            if len(equalList) == 0:
                equalList.append(copy.copy(rel.clockArr))
            else:
                leftListId = -1
                rightListId = -1
                for i in range(len(equalList)):
                    for j in range(len(equalList[i])):
                        if equalList[i][j] == rel.clockArr[0]:
                            leftListId = i
                        if equalList[i][j] == rel.clockArr[1]:
                            rightListId = i
                if leftListId != -1 and rightListId != -1:
                    leftList = equalList[leftListId]
                    rightList = equalList[rightListId]
                    equalList[leftListId] = leftList + rightList
                    equalList.remove(rightList)
                elif leftListId == -1 and rightListId == -1:
                    equalList.append(copy.copy(rel.clockArr))
                elif leftListId == -1:
                    equalList[rightListId].append(rel.clockArr[0])
                else:
                    equalList[rightListId].append(rel.clockArr[1])
    return equalList

def getExpClkSelArr(hole,lenArr,spec):
    expName = hole.clockArr[0]
    expId = spec.getClockId(expName)
    expType = hole.type
    if hole.clockArr[1] == "":
        expClkName = hole.clockArr[2]
    else:
        expClkName = hole.clockArr[1]
    arr = []
    for i in range(0, spec.getClockCount()):
        if i == expId:
            arr.append(-1)
        else:
            arr.append(0)

    for relation in hole.relateRelations:
        selType = checkRelClkSel(relation, expName)
        if relation.clockArr[0] == expName:
            relClk = relation.clockArr[1]
        else:
            relClk = relation.clockArr[0]
        arr[spec.getClockId(expClkName)] = -1
        for clkLenArr in lenArr:
            if clkLenArr[spec.getClockId(relClk)] == -1:
                return arr
            clkLen = clkLenArr[spec.getClockId(relClk)] / spec.getClockCount()
            expClkLen = clkLenArr[spec.getClockId(expClkName)] / spec.getClockCount()
            arr[spec.getClockId(relClk)] = -1

            if selType == 1:
                if expType == 0:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and clkLenArr[i] / spec.getClockCount() + expClkLen < clkLen:
                            arr[i] = -1
                elif expType == 1:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() < clkLen or expClkLen < clkLen ):
                            arr[i] = -1
                elif expType == 2:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() < clkLen or expClkLen < clkLen ):
                            arr[i] = -1
                else:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() < clkLen and expClkLen < clkLen ):
                            arr[i] = -1
            elif selType == 0:
                if expType == 0:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and clkLenArr[i] / spec.getClockCount() > clkLen or expClkLen > clkLen:
                            arr[i] = -1
                elif expType == 2:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() < clkLen or expClkLen < clkLen ):
                            arr[i] = -1
                elif expType == 3:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() > clkLen or expClkLen > clkLen ):
                            arr[i] = -1
            elif selType == -1:
                if expType == 0:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() > clkLen or expClkLen > clkLen ):
                            arr[i] = -1
                elif expType == 2:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() > clkLen and expClkLen > clkLen ):
                            arr[i] = -1
                elif expType == 3:
                    for i in range(0,len(clkLenArr)):
                        if clkLenArr[i]!=-1 and (clkLenArr[i] / spec.getClockCount() > clkLen or expClkLen > clkLen ):
                            arr[i] = -1
    return arr

def getExpOptSelArr(hole,lenArr,spec):
    if len(hole.clockArr) == 2:
        arr = [0.0,0.0]
    else:
        arr = [0.0,0.0,0.0,0.0]
        for relation in hole.relateRelations:
            selType = checkRelClkSel(relation, hole.clockArr[0])
            loc = 1
            if relation.clockArr[1] == hole.clockArr[0]:
                loc = 0
            for clkLenArr in lenArr:
                lId = spec.getClockId(hole.clockArr[1])
                rId = spec.getClockId(hole.clockArr[2])
                if clkLenArr[lId] == -1 or clkLenArr[rId] == -1 or clkLenArr[
                    spec.getClockId(relation.clockArr[loc])] == -1:
                    return arr
                rankL = clkLenArr[lId] % spec.getClockCount()
                rankR = clkLenArr[rId] % spec.getClockCount()
                rankLenL = clkLenArr[lId] / spec.getClockCount()
                rankLenR = clkLenArr[rId] / spec.getClockCount()
                rankClk = clkLenArr[spec.getClockId(relation.clockArr[loc])] % spec.getClockCount()
                rankLenClk = clkLenArr[spec.getClockId(relation.clockArr[loc])] / spec.getClockCount()
                rank = 0
                same = 0
                if rankLenL == rankLenClk:
                    rank += 0
                    same += 1
                elif rankClk > rankL:
                    rank += 1
                elif rankClk < rankL:
                    rank -= 1

                if rankLenR == rankLenClk:
                    rank += 0
                    same += 1
                elif rankClk > rankR:
                    rank += 1
                elif rankClk < rankR:
                    rank -= 1

                if selType == 1:
                    if rank > 1:
                        arr[1] = -1
                        arr[2] = -1
                        arr[3] = -1
                    elif rank == 1:
                        arr[1] = -1
                        arr[2] = -1
                    elif rank == 0:
                        arr[1] = -1
                elif selType == 0:
                    if rank > 1:
                        arr[1] = -1
                        arr[2] = -1
                        arr[3] = -1
                    elif rank == 1:
                        arr[1] = -1
                        arr[2] = -1
                    elif rank < -1:
                        arr[0] = -1
                        arr[2] = -1
                        arr[3] = -1
                    elif rank == -1:
                        arr[0] = -1
                        arr[3] = -1
                elif selType == -1:
                    if rank < -1:
                        arr[0] = -1
                        arr[2] = -1
                        arr[3] = -1
                    elif rank == -1:
                        arr[0] = -1
                        arr[3] = -1
                    elif rank == 0:
                        arr[0] = -1

    return arr

def checkRelClkSel(relation,clk):
    loc = 0
    if relation.clockArr[1]==clk:
        loc = 1
    if (loc == 0 and (relation.type == 1 or relation.type == 2)) or (loc == 1 and relation.type == 4):
        clkSelType = 1
    elif (loc == 1 and (relation.type == 1 or relation.type == 2)) or (loc == 0 and relation.type == 4):
        clkSelType = -1
    elif relation.type == 0:
        clkSelType = 0
    else:
        clkSelType = -2
    return clkSelType

def getClkSelArr(oldSelArr,clkLenArr,selType,clkId):

    for lenArr in clkLenArr:
        if lenArr[clkId] == -1:
            break
        clkRank = int(lenArr[clkId]%len(oldSelArr))
        clkLen = int(lenArr[clkId]/len(oldSelArr))
        for i in range(0,len(oldSelArr)):
            if oldSelArr[i] == 0:
                if lenArr[i] == -1:
                    continue
                selLen = int(lenArr[i] / len(oldSelArr))
                if selType == -2:
                    continue
                elif selType == -1:
                    if clkLen < selLen:
                        oldSelArr[i] = -1
                elif selType == 1:
                    if clkLen > selLen:
                        oldSelArr[i] = -1
                else:
                    if clkLen != selLen:
                        oldSelArr[i] = -1
    return oldSelArr

def clockLengthSort(traceArr):
    count = len(traceArr[0])
    lenList = []
    for trace in traceArr:
        lengthArr = []
        sortArr = []
        for i in range(0,len(trace)):
            lengthArr.append(-1)
            clockList = trace[i]
            length = len(clockList)
            if not(length == 1 and clockList[0] == -1):
                sortArr.append(length * count + i)
        sortArr.sort()
        i = 0
        while i < len(sortArr)-1:
            lenL = int(sortArr[i]/count)
            lId = sortArr[i]%count
            lenR = int(sortArr[i+1] / count)
            rId = sortArr[i+1] % count
            if lenL == lenR:
                traceLeft = trace[lId]
                traceRight = trace[rId]
                tag = 0
                j = lenL - 1
                while j >=0:
                    if traceLeft[j] < traceRight[j]:
                        sortArr[i] = lenR*count + rId
                        sortArr[i+1] = lenL*count + lId
                        i = max(i-2,0)
                        break
                    elif traceLeft[j] > traceRight[j]:
                        break
                    j-=1
            i+=1
        for i in range(0,len(sortArr)):
            lengthArr[sortArr[i]%count] = int(sortArr[i]/count)*count + i
        lenList.append(lengthArr)
    return lenList

def traceLengthInduction(traceArr,leftId,rightId):
    type = 0
    for trace in traceArr:
        if(len(trace[leftId])>len(trace[rightId])):
            if type >= 0:
                type = 1
            else:
                type = -2
                break
        elif (len(trace[leftId])<len(trace[rightId])):
            if type <= 0:
                type = -1
            else:
                type = -2
                break
    return type



def expressionTraceExtend(oldTraces,spec,uncertainExps):
    traces = oldTraces
    clockList = spec.getClockList()
    traceLen = len(traces[0])
    for j in range(len(traces)):
        for i in range(0,len(clockList)-traceLen):
            traces[j].append([-1])
    isChange = True
    while isChange:
        isChange = False
        k = 0
        while k <len(uncertainExps):
            expression = uncertainExps[k]
            expId = spec.getClockId(expression.name)
            if (len(traces[0][expId]) > 0 and traces[0][expId][0] == -1):
                leftId = spec.getClockId(expression.clockArr[0])
                if (expression.type < 4 or expression.type == 6):
                    rightId = spec.getClockId(expression.clockArr[1])
                    if (len(traces[0][leftId]) == 0 or traces[0][leftId][0] != -1) and (
                            len(traces[0][rightId]) == 0 or traces[0][rightId][0] != -1):
                        expTraces = getExpressionClock(expression, traces, spec, traceLen)
                        for j in range(len(traces)):
                            traces[j][expId] = expTraces[j]
                        isChange = True
                        # uncertainExps.remove(expression)
                        del uncertainExps[k]
                        k = k - 1
                elif (expression.type == 4 or expression.type == 5):
                    if (len(traces[0][leftId]) == 0 or traces[0][leftId][0] != -1):
                        expTraces = getExpressionClock(expression, traces, spec, traceLen)
                        for j in range(len(traces)):
                            traces[j][expId] = expTraces[j]
                        isChange = True
                        # uncertainExps.remove(expression)
                        del uncertainExps[k]
                        k = k - 1
            else:
                del uncertainExps[k]
                k = k - 1
            k = k + 1
        for hole in spec.expOptHole:
            if hole.type != -1:
                expId = spec.getClockId(hole.clockArr[0])
                if hole.type >= 4:
                    expression = CCSL.expression(hole.clockArr[0], hole.type, [hole.clockArr[1]])
                    if (len(traces[0][expId]) > 0 and traces[0][expId][0] == -1):
                        leftId = spec.getClockId(hole.clockArr[1])
                        rightId = spec.getClockId(hole.clockArr[1])
                        if (len(traces[0][leftId]) > 0 and traces[0][leftId][0] != -1):
                            expTraces = getExpressionClock(expression, traces, spec, traceLen)
                            for j in range(len(traces)):
                                traces[j][expId] = expTraces[j]
                            isChange = True
                else:
                    expression = CCSL.expression(hole.clockArr[0],hole.type,[hole.clockArr[1],hole.clockArr[2]])
                if hole.type < 5 and (len(traces[0][expId]) > 0 and traces[0][expId][0] == -1):
                    leftId = spec.getClockId(hole.clockArr[1])
                    rightId = spec.getClockId(hole.clockArr[2])
                    if (len(traces[0][leftId]) > 0 and traces[0][leftId][0] != -1) and (
                            len(traces[0][leftId]) > 0 and traces[0][rightId][0] != -1):
                        expTraces = getExpressionClock(expression, traces, spec,traceLen)
                        for j in range(len(traces)):
                            traces[j][expId] = expTraces[j]
                        isChange = True
        for hole in spec.expClkHole:
            if hole.clockArr[1] != "" and hole.clockArr[2] != "":
                expId = spec.getClockId(hole.clockArr[0])
                expression = CCSL.expression(hole.clockArr[0],hole.type,[hole.clockArr[1],hole.clockArr[2]])
                if hole.type < 5 and (len(traces[0][expId]) > 0 and traces[0][expId][0] == -1):
                    leftId = spec.getClockId(hole.clockArr[1])
                    rightId = spec.getClockId(hole.clockArr[2])
                    if (len(traces[0][leftId]) > 0 and traces[0][leftId][0] != -1) and (
                            len(traces[0][rightId]) > 0 and traces[0][rightId][0] != -1):
                        expTraces = getExpressionClock(expression, traces, spec,traceLen)
                        for j in range(len(traces)):
                            traces[j][expId] = expTraces[j]
                        isChange = True
    return traces,uncertainExps

def holeInduction(currentTraces,spec,hole,action,traceLen,orgSpec):
    holeType = hole.holeType
    relationType = hole.type
    result = 1
    dep = 1
    if holeType == 0:
        if not (checkUncertain(hole.clockArr[0],orgSpec) or checkUncertain(hole.clockArr[1],orgSpec)):
            dep = 0
        for trace in currentTraces:
            if action == 5 or action == 6:
                leftClock = trace[spec.getClockId(hole.clockArr[1])]
                rightClock = trace[spec.getClockId(hole.clockArr[0])]
                rel = action - 4
            else:
                leftClock = trace[spec.getClockId(hole.clockArr[0])]

                rightClock = trace[spec.getClockId(hole.clockArr[1])]
                rel = action
            if not checkRelation(leftClock, rightClock, rel):
                return -1,dep
    elif holeType == 1:
        if hole.clockArr[0] == "":
            clkName = hole.clockArr[1]
        else:
            clkName = hole.clockArr[0]
        if not (checkUncertain(spec.getClockList()[action],orgSpec) or checkUncertain(clkName,orgSpec)):
            dep = 0
        for trace in currentTraces:
            if hole.clockArr[0] == "":
                leftClock = trace[action]
            else:
                leftClock = trace[spec.getClockId(hole.clockArr[0])]
            if hole.clockArr[1] == "":
                rightClock = trace[action]
            else:
                rightClock = trace[spec.getClockId(hole.clockArr[1])]
            if not checkRelation(leftClock, rightClock, relationType):
                return -1,dep
    elif holeType == 2:
        # if not (checkUncertain(hole.clockArr[1],orgSpec) or checkUncertain(hole.clockArr[2],orgSpec)):
        #     dep = 0
        expDep = 1
        if len(hole.clockArr) == 2:
            if not (checkUncertain(hole.clockArr[1], orgSpec)):
                expDep = 0
        else:
            if not (checkUncertain(hole.clockArr[1], orgSpec) or checkUncertain(hole.clockArr[2], orgSpec)):
                expDep = 0
        expClockArr= []
        expClockArr.append(hole.clockArr[1])
        if len(hole.clockArr) >2:
            expClockArr.append(hole.clockArr[2])
        expession = CCSL.expression(hole.clockArr[0],action,expClockArr,hole.addition)
        expClock = getExpressionClock(expession,currentTraces,spec,traceLen)
        leftClock = currentTraces[0][spec.getClockId(hole.clockArr[1])]
        if len(hole.clockArr) > 2:
            rightClock = currentTraces[0][spec.getClockId(hole.clockArr[2])]
        if (len(hole.clockArr) >2):
            if (len(leftClock) > 0 and leftClock[0] == -1) or (len(rightClock) > 0 and rightClock[0] == -1):
                result = 0
                return result, dep
        elif(len(hole.clockArr) ==2 and len(leftClock) > 0 and leftClock[0] == -1):
            result = 0
            return result, dep
        for i in range(len(currentTraces)):
            currentTraces[i][spec.getClockId(expession.name)] = expClock[i]
            for relation in hole.relateRelations:
                leftClock = currentTraces[i][spec.getClockId(relation.clockArr[0])]
                rightClock = currentTraces[i][spec.getClockId(relation.clockArr[1])]
                if (len(leftClock) > 0 and leftClock[0] == -1) or (len(rightClock) > 0 and rightClock[0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[0])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[0])][0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[1])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[1])][0] == -1):
                    result = 0
                elif not checkRelation(currentTraces[i][spec.getClockId(relation.clockArr[0])],currentTraces[i][spec.getClockId(relation.clockArr[1])],relation.type):
                    if expDep == 0 and not (checkUncertain(relation.clockArr[0], orgSpec) or checkUncertain(relation.clockArr[1], orgSpec)):
                        dep = 0
                    return -1,dep
            currentTraces[i][spec.getClockId(expession.name)] = expClock[i]
            for relation in hole.addRelations:
                leftClock = currentTraces[i][spec.getClockId(relation.clockArr[0])]
                rightClock = currentTraces[i][spec.getClockId(relation.clockArr[1])]
                if (len(leftClock) > 0 and leftClock[0] == -1) or (len(rightClock) > 0 and rightClock[0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[0])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[0])][0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[1])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[1])][0] == -1):
                    result = 0
                elif not checkRelation(currentTraces[i][spec.getClockId(relation.clockArr[0])],
                                       currentTraces[i][spec.getClockId(relation.clockArr[1])], relation.type):
                    return -1,dep
    else:
        if hole.clockArr[1] == "":
            clkName = hole.clockArr[2]
        else:
            clkName = hole.clockArr[1]
        expDep = 1
        if not (checkUncertain(spec.getClockList()[action],orgSpec) or checkUncertain(clkName,orgSpec)):
            expDep = 0
        clockList = spec.getClockList()
        if hole.clockArr[1] == "":
            leftId = action
            rightId = spec.getClockId(hole.clockArr[2])
        else:
            leftId = spec.getClockId(hole.clockArr[1])
            rightId = action
        expClockArr = []
        expClockArr.append(clockList[leftId])
        expClockArr.append(clockList[rightId])
        expession = CCSL.expression( hole.clockArr[0],relationType, expClockArr)
        expession.addition = hole.addition
        leftClock = currentTraces[0][leftId]
        rightClock = currentTraces[0][rightId]
        if (len(leftClock) > 0 and leftClock[0] == -1) or (len(rightClock) > 0 and rightClock[0] == -1):
            result = 0
            return result,dep
        expClock = getExpressionClock(expession, currentTraces, spec, traceLen)
        for i in range(len(currentTraces)):
            currentTraces[i][spec.getClockId(expession.name)] = expClock[i]
            for relation in hole.relateRelations:
                leftClock = currentTraces[i][spec.getClockId(relation.clockArr[0])]
                rightClock = currentTraces[i][spec.getClockId(relation.clockArr[1])]
                if (len(leftClock) > 0 and leftClock[0] == -1) or (len(rightClock) > 0 and rightClock[0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[0])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[0])][0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[1])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[1])][0] == -1):
                    result = 0
                elif not checkRelation(currentTraces[i][spec.getClockId(relation.clockArr[0])],currentTraces[i][spec.getClockId(relation.clockArr[1])],relation.type):
                    if expDep == 0 and not (checkUncertain(relation.clockArr[0], orgSpec) or checkUncertain(relation.clockArr[1], orgSpec)):
                        dep = 0
                    return -1,dep
            for relation in hole.addRelations:
                leftClock = currentTraces[i][spec.getClockId(relation.clockArr[0])]
                rightClock = currentTraces[i][spec.getClockId(relation.clockArr[1])]
                if (len(leftClock) > 0 and leftClock[0] == -1) or (len(rightClock) > 0 and rightClock[0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[0])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[0])][0] == -1) or (
                        len(currentTraces[i][spec.getClockId(relation.clockArr[1])]) > 0 and
                        currentTraces[i][spec.getClockId(relation.clockArr[1])][0] == -1):
                    result = 0
                elif not checkRelation(currentTraces[i][spec.getClockId(relation.clockArr[0])],currentTraces[i][spec.getClockId(relation.clockArr[1])],relation.type):
                    return -1,dep
    return result,dep