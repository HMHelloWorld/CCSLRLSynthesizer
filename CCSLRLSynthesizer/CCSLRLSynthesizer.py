import numpy as np
import copy
import random
import CCSL
import CCSLChecker
import time

def initCountArr(actions):
    countArr = []
    for actionList in actions:
        arr =np.zeros(len(actionList))
        countArr.append(arr)
    return countArr

def relationOptRewardFunction(action,hole):
    relReward = [4.0, 2.0, 1.0, 2.5, 3.0, 2.0, 1.0, -0.1]
    return float(relReward[action]/4)

def relationClkRewardFunction(action,lenArr,hole,spec):
    reward = 0
    if hole.clockArr[0] == "":
        loc = 0
    else:
        loc = 1
    if (spec.getClockId(hole.clockArr[(loc+1)%2])==action):
        return 0.0
    if (loc == 0 and (hole.type == 1 or hole.type == 2)) or (loc == 1 and hole.type == 4):
        control = 0
    else:
        control = 1
    for lenList in lenArr:
        if control == 1:
            reward += float(lenList[action] % len(lenList))
        else:
            reward += float(len(lenList) - lenList[action] % len(lenList))
    return float(reward/(len(lenArr)*len(lenArr[0])))

def expressionOptRewardFunction(action,hole):
    rewardList = [1, 4, 3, 2]
    reward = 0
    if len(hole.clockArr) == 2:
        a = action -4
        rewardList = [4.0,4.0]
        reward = rewardList[a]
    for relation in hole.relateRelations:
        if len(hole.clockArr) > 2:
            if relation.clockArr[0] == hole.clockArr[1] or relation.clockArr[0] == hole.clockArr[2] or \
                    relation.clockArr[1] == hole.clockArr[1] or relation.clockArr[1] == hole.clockArr[2]:
                return -0.8
            else:
                loc = -1
                if hole.clockArr[0] == relation.clockArr[0]:
                    loc = 0
                elif hole.clockArr[0] == relation.clockArr[1]:
                    loc = 1
                else:
                    for exp in hole.relateExps:
                        if exp.name == relation.clockArr[0]:
                            loc = 0
                        elif exp.name == relation.clockArr[1]:
                            loc = 1
                if (loc == 0 and (relation.type == 1 or relation.type == 2)) or (loc == 1 and relation.type == 4):
                    reward += float(rewardList[action])
                else:
                    reward += 5.0 - float(rewardList[action])
    for relation in hole.addRelations:
        if relation.clockArr[0] == hole.clockArr[1] or relation.clockArr[0] == hole.clockArr[2] or relation.clockArr[1] == hole.clockArr[1] or relation.clockArr[1] == hole.clockArr[2]:
            return -0.8
        else:
            loc = -1
            if hole.clockArr[0] == relation.clockArr[0]:
                loc = 0
            elif hole.clockArr[0] == relation.clockArr[1]:
                loc = 1
            else:
                for exp in hole.relateExps:
                    if exp.name == relation.clockArr[0]:
                        loc = 0
                    elif exp.name == relation.clockArr[1]:
                        loc = 1
            if (loc == 0 and (relation.type == 1 or relation.type == 2)) or (loc == 1 and relation.type == 4):
                reward += float(rewardList[action])
            else:
                reward += 5.0 - float(rewardList[action])
    if (len(hole.relateRelations)>0 or len(hole.addRelations)>0):
        reward = float(reward/((len(hole.relateRelations)+len(hole.addRelations))*5.0))
    return reward

def expressionClkRewardFunction(action,lenArr,hole,spec):
    reward = 0.0
    eqList = CCSLChecker.getEqualClockList(spec)
    actClk = spec.getClockList()[action]
    actEqList = []
    for list in eqList:
        for clk in list:
            if clk == actClk:
                actEqList = list
                break
    if len(actEqList) == 0:
        actEqList.append(actClk)
    for relation in hole.relateRelations:
        for clk in actEqList:
            if relation.clockArr[0] == clk or relation.clockArr[1] == clk:
                return -1.0
        if relation.clockArr[0] == hole.clockArr[1] or relation.clockArr[0] == hole.clockArr[2] or relation.clockArr[1] == hole.clockArr[1] or relation.clockArr[1] == hole.clockArr[2]:
            return -1.0
        else:
            loc = -1
            if hole.clockArr[0] == relation.clockArr[0]:
                loc = 0
            elif hole.clockArr[0] == relation.clockArr[1]:
                loc = 1
            else:
                for exp in hole.relateExps:
                    if exp.name == relation.clockArr[0]:
                        loc = 0
                    elif exp.name == relation.clockArr[1]:
                        loc = 1
            # if relation.type == 0:
            if relation.clockArr[abs(loc - 1)] == spec.getClockList()[action]:
                return 0.0
            if (loc == 0 and (relation.type == 1 or relation.type == 2)) or (loc == 1 and relation.type == 4):
                control = 0
            else:
                control = 1
            for lenList in lenArr:
                if control == 1:
                    reward += float(lenList[spec.getClockId(relation.clockArr[loc])] % len(lenList))
                else:
                    reward += float(len(lenList) - lenList[spec.getClockId(relation.clockArr[loc])] % len(lenList))
    for relation in hole.addRelations:
        for clk in actEqList:
            if relation.clockArr[0] == clk or relation.clockArr[1] == clk:
                return -1.0
        if relation.clockArr[0] == hole.clockArr[1] or relation.clockArr[0] == hole.clockArr[2] or relation.clockArr[1] == hole.clockArr[1] or relation.clockArr[1] == hole.clockArr[2]:
            return -1.0
        else:
            loc = -1
            if hole.clockArr[0] == relation.clockArr[0]:
                loc = 0
            elif hole.clockArr[0] == relation.clockArr[1]:
                loc = 1
            else:
                for exp in hole.relateExps:
                    if exp.name == relation.clockArr[0]:
                        loc = 0
                    elif exp.name == relation.clockArr[1]:
                        loc = 1
            # if relation.type == 0:
            if relation.clockArr[abs(loc - 1)] == spec.getClockList()[action]:
                return 0.0
            if (loc == 0 and (relation.type == 1 or relation.type == 2)) or (loc == 1 and relation.type == 4):
                control = 0
            else:
                control = 1
            for lenList in lenArr:
                if control == 1:
                    reward += float(lenList[spec.getClockId(relation.clockArr[loc])] % len(lenList))
                else:
                    reward += float(len(lenList) - lenList[spec.getClockId(relation.clockArr[loc])] % len(lenList))
    if reward == 0.0:
        return reward
    else:
        return float(reward / (len(lenArr)*len(lenArr[0])*(len(hole.addRelations)+len(hole.relateRelations))))

def rewardFunction(actionList,lenArr,holeList,spec):
    reward = 0
    rewardList = []
    for i in range(len(holeList)):
        holeType = holeList[i].holeType
        hole = copy.copy(holeList[i])
        if holeType == 0:
            relation = CCSL.relation(actionList[i],holeList[i].clockArr)
            if not (CCSLChecker.checkSameRelation(relation,spec) or CCSLChecker.checkChoseRelation(relation, spec,holeList,actionList,i)):
                r = float(relationOptRewardFunction(actionList[i],holeList[i]))
                reward += r
            else:
                r = 0.0
            rewardList.append(r)

        elif holeType == 1:

            clockList = []
            for clock in holeList[i].clockArr:
                if clock == "":
                    clockList.append(spec.getClockList()[actionList[i]])
                else:
                    clockList.append(clock)
            relation = CCSL.relation(holeList[i].type, clockList)
            if not (CCSLChecker.checkSameRelation(relation, spec) or CCSLChecker.checkChoseRelation(relation, spec,holeList,actionList,i)):
                r = float(relationClkRewardFunction(actionList[i],lenArr,holeList[i],spec))
                reward += r
            else:
                r = 0.0
            rewardList.append(r)

        elif holeType == 2:
            for j in range(0,len(holeList)):
                if holeList[j].holeType == 1 and actionList[j] == spec.getClockId(hole.clockArr[0]):
                    clocks = copy.copy(holeList[j].clockArr)
                    if clocks[0] == "":
                        clocks[0] = hole.clockArr[0]
                    else:
                        clocks[1] = hole.clockArr[1]
                    hole.addRelations.append(CCSL.relation(holeList[j].type,clocks))
                elif holeList[j].holeType == 0 and (holeList[j].clockArr[0] == spec.getClockId(hole.clockArr[0]) or holeList[j].clockArr[1] == spec.getClockId(hole.clockArr[0])):
                    clocks = copy.copy(holeList[j].clockArr)
                    hole.addRelations.append(CCSL.relation(actionList[j], clocks))
            r = float(expressionOptRewardFunction(actionList[i], hole))
            reward += r
            rewardList.append(r)
        elif holeType == 3:
            for j in range(len(holeList)):
                if holeList[j].holeType == 1 and actionList[j] == spec.getClockId(hole.clockArr[0]):
                    clocks = copy.copy(holeList[j].clockArr)
                    if clocks[0] == "":
                        clocks[0] = hole.clockArr[0]
                    else:
                        clocks[1] = hole.clockArr[0]
                    hole.addRelations.append(CCSL.relation(holeList[j].type,clocks))
                elif holeList[j].holeType == 0 and (holeList[j].clockArr[0] == spec.getClockId(hole.clockArr[0]) or holeList[j].clockArr[1] == spec.getClockId(hole.clockArr[0])):
                    clocks = copy.copy(holeList[j].clockArr)
                    hole.addRelations.append(CCSL.relation(actionList[j], clocks))
            r = float(expressionClkRewardFunction(actionList[i],lenArr,hole,spec))
            reward += r
            rewardList.append(r)
    return rewardList
def ccslReinforcemenceLarning(round,epsilon,spec,traces,traceLen):
    # time_start = time.time()
    q_table,initTra,uncertainExps = CCSLChecker.holeNetworkInit(traces, spec)
    actions = copy.deepcopy(q_table)
    countArr = initCountArr(actions)
    # reverse_q_table = copy.deepcopy(q_table)
    maxReward= 0
    maxList = np.zeros(len(spec.getHoleList()))
    maxChooseList = []
    inductionMap = copy.deepcopy(q_table)
    # preTrain = min(round / 2, 100 * len(spec.getHoleList()))
    preTrain = round * 0.3
    for i in range(round):
        initTracesArr = copy.deepcopy(initTra)
        resultSpec = copy.deepcopy(spec)
        unExps = copy.deepcopy(uncertainExps)
        currentTraces = initTracesArr
        needCheckActionId = []
        needCheckHoles = []
        chooseList = []
        holeList = resultSpec.getHoleList()

        isOk = True
        if i<preTrain:
            eps = 0.9
        else:
            eps = epsilon
        # eps = epsilon

        mustGreedy = False
        if (random.uniform(0, 1) > 0.95 and i > preTrain):
            mustGreedy = True


        for j in range(len(holeList)):

            if (random.uniform(0, 1) > eps) and not mustGreedy:
                isGreedy = False
            else:
                isGreedy = True
            hole = holeList[j]
            if i == round - 1 or mustGreedy:
                action = actionChoose(q_table[j], True, countArr[j])
            elif i < preTrain:
                # action = actionCuriosityChoose(q_table[j], isGreedy, countArr[j], i, round)
                # action = actionCuriosityChoose(actions[j],isGreedy,countArr[j],i,round)
                # action = actionChoose(q_table[j], isGreedy, countArr[j])
                isUseGreedy = random.uniform(0, 1)
                if isUseGreedy > 0.5:
                    action = actionCuriosityChoose(q_table[j], isGreedy, countArr[j], i, round)
                else:
                    action = actionCuriosityChoose(actions[j], isGreedy, countArr[j], i, round)
                # action = actionChoose(actions[j], isGreedy, countArr[j])
            else:
                if (random.uniform(0, 1) > 0.9) and len(maxChooseList) == len(holeList):
                    action = maxChooseList[j]
                    if hole.holeType == 2 and len(hole.clockArr) == 2:
                        action -= 4
                else:
                    # action = actionCuriosityChoose(q_table[j], isGreedy,countArr[j],i,round)
                    # action = actionChoose(q_table[j], isGreedy, countArr[j])
                    isUseGreedy = random.uniform(0, 1)
                    if isUseGreedy > 0.1:
                        action = actionCuriosityChoose(q_table[j], isGreedy, countArr[j], i, round)
                    else:
                        action = actionCuriosityChoose(actions[j], isGreedy, countArr[j], i, round)
            # action = actionChoose(q_table[j], isGreedy)
            result = inductionMap[j][action]
            # if j == 0 and action == 10:
            #     print chooseList
            if hole.holeType == 2 and len(hole.clockArr) == 2:
                action += 4
            if result == 0:
                result,dep = CCSLChecker.holeInduction(currentTraces, resultSpec, hole, action, traceLen,spec)
                if dep == 0:
                    inductionMap[j][action] = result
            resultFin = result
            chooseList.append(action)
            isFill = False

            if result == 0:
                resultSpec.fillHole(hole, action)
                isFill = True
                if hole.holeType == 2 or hole.holeType == 3:
                    resultSpec.fillHole(hole, action)
                    currentTraces,unExps = CCSLChecker.expressionTraceExtend(currentTraces, resultSpec,unExps)
                    result,dep = CCSLChecker.holeInduction(currentTraces, resultSpec, hole, action,traceLen,spec)
                    resultFin = result
            if result == 0:
                needCheckHoles.append(hole)
                needCheckActionId.append(action)
            elif result == 1:
                if not isFill:
                    resultSpec.fillHole(hole, action)
                if hole.holeType == 2 or hole.holeType == 3:

                    currentTraces,unExps = CCSLChecker.expressionTraceExtend(currentTraces, resultSpec,unExps)
                    isStop = False
                    while not isStop:
                        isStop = True
                        k = 0
                        length = (len(needCheckHoles))
                        while k < length:
                            needCheckHole = needCheckHoles[k]
                            subResult,dep = CCSLChecker.holeInduction(currentTraces, resultSpec, needCheckHole, needCheckActionId[k],traceLen,spec)
                            if subResult == -1:
                                resultFin = -1
                                break
                            elif subResult == 1:
                                isStop = False
                                del needCheckHoles[k]
                                del needCheckActionId[k]
                                currentTraces,unExps = CCSLChecker.expressionTraceExtend(currentTraces,resultSpec,unExps)
                                k=-1
                                length -= 1
                            k+=1
            if resultFin == -1:
                isOk = False
                length = len(chooseList)
                if result == -1:
                    if hole.holeType == 0:
                        if not (CCSLChecker.checkUncertain(hole.clockArr[0],
                                                                  resultSpec) or CCSLChecker.checkUncertain(
                                hole.clockArr[1], resultSpec)):
                            q_table[j][action] = -1
                            actions[j][action] = -1
                            continue
                    elif hole.holeType == 1:
                        if hole.clockArr[0] == "":
                            relClock = hole.clockArr[1]
                        else:
                            relClock = hole.clockArr[0]
                        if not (CCSLChecker.checkUncertain(relClock, resultSpec) or CCSLChecker.checkUncertain(
                                spec.getClockList()[action], resultSpec)):
                            q_table[j][action] = -1
                            actions[j][action] = -1
                            isOk = False
                            continue
                    elif hole.holeType == 2:
                        expName = hole.clockArr[0]
                        isUncertain = True
                        if len(hole.clockArr) > 2:
                            if not (CCSLChecker.checkUncertain(hole.clockArr[1],
                                                               resultSpec) or CCSLChecker.checkUncertain(
                                    hole.clockArr[2], resultSpec)):
                                for relation in hole.relateRelations:
                                    if not (CCSLChecker.checkExpressionUncertain(relation.clockArr[0], spec,
                                                                                 spec.getClockId(hole.clockArr[
                                                                                                     0])) or CCSLChecker.checkExpressionUncertain(
                                            relation.clockArr[1], spec, spec.getClockId(hole.clockArr[0]))):
                                        isUncertain = False
                                        break
                                    # clkName = ""
                                    # if relation.clockArr[0] == expName:
                                    #     clkName = relation.clockArr[1]
                                    # elif relation.clockArr[1] == expName:
                                    #     clkName = relation.clockArr[0]
                                    # if clkName != "":
                                    #     if CCSLChecker.checkUncertain(clkName, resultSpec):
                                    #         isUncertain = True
                                    #     else:
                                    #         isUncertain = False
                                    #         break
                                if not isUncertain:
                                    q_table[j][action] = -1
                                    actions[j][action] = -1
                                    continue
                    elif hole.holeType == 3:
                        expName = hole.clockArr[0]
                        if hole.clockArr[1] == "":
                            expClk = hole.clockArr[2]
                        else:
                            expClk = hole.clockArr[1]
                        if not (CCSLChecker.checkUncertain(expClk, resultSpec) and CCSLChecker.checkUncertain(spec.getClockList()[action], resultSpec)):
                            isContinue = False
                            for relation in hole.relateRelations:
                                if relation.clockArr[0] == expName:
                                    clkName = relation.clockArr[1]
                                else:
                                    clkName = relation.clockArr[0]
                                if not CCSLChecker.checkUncertain(clkName, resultSpec):
                                    q_table[j][action] = -1
                                    actions[j][action] = -1
                                    isContinue =True
                                    break
                            if isContinue:
                                continue

                    for cnt in range(length):
                        if hole.holeType == 2 and len(hole.clockArr) == 2:
                            tag = chooseList[cnt]-4
                        else:
                            tag = chooseList[cnt]
                        q_table[cnt][tag] = float((q_table[cnt][tag]*0.99 ))
                        # if i < preTrain:
                        #     actions[count][chooseList[count]] = float(
                        #     (actions[count][chooseList[count]] * (countArr[count][chooseList[count]]) - 0.0001) / (
                        #                 countArr[count][chooseList[count]] + 1))
                        countArr[cnt][tag] += 1
                    # q_table[length - 1][chooseList[length - 1]] = float(
                    #     (q_table[length - 1][chooseList[length - 1]] * 0.99 - 0.1 / round))
                    # if i < preTrain:
                    #     # actions[length - 1][chooseList[length - 1]] = float(
                    #     #     (actions[length - 1][chooseList[length - 1]] * (
                    #     [length - 1][chooseList[length - 1]]) - 0.0002) / (
                    #     #             countArr[length - 1][chooseList[length - 1]] + 1))
                    #     countArr[length - 1][chooseList[length - 1]] += 1

                else:
                    for count in range(length):
                        q_table[count][chooseList[count]] = float( (q_table[count][chooseList[count]]*0.99 - 0.1/round))
                        # if i < preTrain:
                            # actions[count][chooseList[count]] = float(
                            # (actions[count][chooseList[count]] * (countArr[count][chooseList[count]]) - 0.0001) / (
                            #             countArr[count][chooseList[count]] + 1))
                        countArr[count][chooseList[count]] += 1
                        isOk =False

        if isOk and len(unExps) > 0:
            isOk = False
            length = len(chooseList)
            for count in range(length - 1):
                q_table[count][chooseList[count]] = float(
                    (q_table[count][chooseList[count]] * 0.99))
                # if i < preTrain:
                    # actions[count][chooseList[count]] = float(
                    #     (actions[count][chooseList[count]] * (countArr[count][chooseList[count]]) - 0.0001) / (
                    #             countArr[count][chooseList[count]] + 1))
                countArr[count][chooseList[count]] += 1
            q_table[length - 1][chooseList[length - 1]] = float(
                (q_table[length - 1][chooseList[length - 1]] * 0.99))
            # if i < preTrain:
                # actions[length - 1][chooseList[length - 1]] = float(
                #     (actions[length - 1][chooseList[length - 1]] * (
                #     countArr[length - 1][chooseList[length - 1]]) - 0.0002) / (
                #             countArr[length - 1][chooseList[length - 1]] + 1))
                # countArr[length - 1][chooseList[length - 1]] += 1

        if isOk:

            lenArr = CCSLChecker.clockLengthSort(currentTraces)
            rList=rewardFunction(chooseList,lenArr,holeList,spec)
            revSumReward = 0.0
            for j in range(len(rList)-1,-1,-1):
                tag = chooseList[j]
                if len(actions[j]) < tag:
                    tag = tag - 4
                revSumReward += rList[j]
                # if i < preTrain:
                    # actions[j][chooseList[j]] = float(
                    # (actions[j][chooseList[j]] * countArr[j][chooseList[j]] + rList[j]) / (countArr[j][chooseList[j]] + 1))
                actions[j][tag] = max(actions[j][tag] , rList[j] )
                countArr[j][tag] += 1
            isMax = False
            if revSumReward >= maxReward:
                maxReward = revSumReward
                isMax = True
                maxChooseList = chooseList
            sumReward = 0.0
            for j in range(len(rList)-1,-1,-1):
                sumReward += rList[j]
                if isMax:
                    alpha = 0.98
                elif rList[j] >= maxList[j]:
                    maxList[j] = rList[j]
                    alpha = 0.1
                    if i < round / 2:
                        alpha = 0.8
                else:
                    alpha = 0.1
                    if i > round / 2:
                        alpha = 0.01
                # if i < round/4:
                #     alpha = 0.5
                tag = chooseList[j]
                if len(actions[j]) < tag:
                    tag = tag - 4
                q_table[j][tag] = float((q_table[j][tag] + (sumReward - q_table[j][tag])*alpha))
                # reverse_q_table[j][chooseList[j]] = float(
                #     (reverse_q_table[j][chooseList[j]] + (revSumReward - reverse_q_table[j][chooseList[j]]) * alpha))
    # time_end = time.time()
    # sumTime = time_end - time_start
    # print(sumTime)
    chooseList = []
    chooseList = maxChooseList
    # print (maxChooseList)
    #choose
    if maxChooseList == []:
        for j in range(len(q_table)):
            list = q_table[j]
            # rlist = reverse_q_table[j]
            theMax = -1
            tag = 0
            for i in range(len(list)):
                if list[i] > theMax:
                    theMax = list[i]
                    tag = i
            chooseList.append(tag)

    # for list in q_table:
    #     theMax = -1
    #     tag = 0
    #     for i in range(len(list)):
    #         if list[i] >= theMax:
    #             max = list[i]
    #             tag = i
    #     chooseList.append(tag)
    # goldenList = [0, 4, 1, 1, 4, 1, 1, 1, 1, 1]
    # if not chooseList == goldenList:
    # for k in range(len(q_table)):
    #     print(q_table[k])
    specResult = CCSL.CCSLSpecification()
    specResult.clocks = copy.copy(spec.clocks)
    specResult.relations = copy.copy(spec.relations)
    specResult.expressions = copy.copy(spec.expressions)

    for i in range(len(spec.getHoleList())):
        hole = spec.getHoleList()[i]
        if hole.holeType == 0:
            rel = CCSL.relation(chooseList[i], hole.clockArr)
            specResult.relations.append(rel)
        elif hole.holeType == 1:
            clkList = []
            if hole.clockArr[0] == "":
                clkList.append(spec.getClockList()[chooseList[i]])
                clkList.append(hole.clockArr[1])
            else:
                clkList.append(hole.clockArr[0])
                clkList.append(spec.getClockList()[chooseList[i]])
            rel = CCSL.relation(hole.type, clkList)
            specResult.relations.append(rel)
        elif hole.holeType == 2:
            clkList = []
            clkList.append(hole.clockArr[1])
            if len(hole.clockArr) > 2:
                clkList.append(hole.clockArr[2])
            exp = CCSL.expression(hole.clockArr[0], chooseList[i], clkList)
            specResult.expressions.append(exp)
        elif hole.holeType == 3:
            clkList = []
            if hole.clockArr[1] == "":
                clkList.append(spec.getClockList()[chooseList[i]])
                clkList.append(hole.clockArr[2])
            else:
                clkList.append(hole.clockArr[1])
                clkList.append(spec.getClockList()[chooseList[i]])
            exp = CCSL.expression(hole.clockArr[0], hole.type, clkList)
            specResult.expressions.append(exp)
    return specResult,chooseList


def actionChoose(actionList,isGreedy,countList):
    chooseList = []
    count = 0
    theMax = 0
    # rev_max = 0
    index = 0
    # revInd = 0
    # rank = 0.0
    # rankList = []
    for i in range(len(actionList)):
        action = actionList[i]
        # revAction = recActionList[i]
        if action > -0.9:
            if theMax < action:
                theMax = action
                index = count
            # if rev_max < revAction:
            #     rev_max = revAction
            #     revInd = count
            count += 1
            chooseList.append(i)
            # rank = countList[i] + 1.0
            # rankList.append(1.0/(rank ** 0.5))

    if isGreedy:
        choose = index
    else:
        choose = int(random.uniform(0, count))
    return chooseList[choose]

def actionCuriosityChoose(actionList,isGreedy,countList,iter,round):
    chooseList = []
    count = 0
    theMax = 0
    # rev_max = 0
    index = 0
    # revInd = 0
    rank = 0.0
    rankList = []
    lamda = (1.0 * iter)/round
    # lamda = float(iter/round)
    for i in range(len(actionList)):
        action = actionList[i]
        # revAction = recActionList[i]
        if action > -0.9:
            rank_i = 1.0 / ((countList[i] + 1.0) ** 0.5)
            phi = 1.0
            phi_a = 1.0
            phi = 1.0 * (1 - lamda)
            phi_a = 1.0 * lamda  # *lamda
            # if lamda < 0.4:
            #     phi = 1.0 * (1-lamda)
            #     phi_a = 1.0 * lamda #*lamda
            # elif lamda < 0.6:
            #     phi = 4.0*(1-lamda)*(1-lamda)
            # else:
            #     lamda = 1.0
            # elif lamda < 0.5:
            #     phi = 1.0 # (1-lamda)*(1-lamda)
            #     phi_a = lamda #* lamda
            # if lamda > 0.5:
            #     phi = 0
            # elif lamda < 0.25:
            #     phi = 10
            # elif lamda < 0.5:
            #     phi = 4
            # if theMax < action + rank_i*(1-lamda)*phi:
            #     theMax = action + rank_i*(1-lamda)*phi
            #     index = count
            if theMax < action*phi_a + rank_i*phi:
                theMax = action*phi_a + rank_i*phi
                index = count
            # if rev_max < revAction:
            #     rev_max = revAction
            #     revInd = count
            count += 1
            chooseList.append(i)
            rank += rank_i
            rankList.append(rank_i)

    if isGreedy:
        choose = index
    else:
        if lamda < 1.1:
            rank = random.uniform(0, rank)
            choose = -1
            while rank >= 0:
                choose += 1
                rank -= rankList[choose]
        else:
            choose = int(random.uniform(0, count))
    action = chooseList[choose]
    return action