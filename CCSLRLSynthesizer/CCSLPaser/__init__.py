import re
import os
import CCSL
def readClockList(filename):
    clockList = []
    try:
        f = open(filename, 'r')
        clockName = f.readline()
        while clockName:
            pattern = r"Clock ([A-z|0-9]*)"
            matchObj = re.match(pattern,clockName)
            if matchObj:
                clk = CCSL.clock(0, matchObj.group(1))
                clockList.append(clk)
            clockName = f.readline()

    finally:
        if f:
            f.close()
    return clockList

def readGoldenList(filename):
    goldenList = []
    try:
        f = open(filename, 'r')
        selection = f.readline()

        while selection:
            goldenList.append(int(selection))
            selection = f.readline()

    finally:
        if f:
            f.close()
    return goldenList

from xml.dom.minidom import parse
def readCCSLConfigureXML(filename):
    relations = []
    expressions = []
    holes = []
    domTree = parse(filename)
    rootNode = domTree.documentElement
    rels = rootNode.getElementsByTagName("relations")[0].getElementsByTagName("relation")
    exps = rootNode.getElementsByTagName("expressions")[0].getElementsByTagName("expression")

    for rel in rels:
        type = int(rel.getAttribute("type"))
        leftClock = rel.getAttribute("leftClock")
        rightClock = rel.getAttribute("rightClock")
        if type == -1:
            hole = CCSL.hole(0,[leftClock,rightClock],-1,[],[])
            holes.append(hole)
        elif leftClock == "":
            hole = CCSL.hole(1, ["", rightClock], type, [],[],[])
            holes.append(hole)
        elif rightClock == "":
            hole = CCSL.hole(1, [leftClock, ""], type, [],[],[])
            holes.append(hole)
        else:
            relations.append(CCSL.relation(type,[leftClock,rightClock]))
    for exp in exps:
        name = exp.getAttribute("name")
        type = int(exp.getAttribute("type"))
        leftClock = exp.getAttribute("leftClock")
        rightClock = exp.getAttribute("rightClock")
        addition = -1
        if exp.hasAttribute("addition"):
            if exp.getAttribute("addition") != "":
                addition = int(exp.getAttribute("addition"))
        if type == -1:
            if rightClock == '':
                hole = CCSL.hole(2, [name, leftClock], -1, [], [], [])
                hole.addition = addition
            else:
                hole = CCSL.hole(2,[name,leftClock,rightClock],-1,[],[],[])
                hole.addition = addition
            holes.append(hole)
        elif leftClock == "":
            hole = CCSL.hole(3, [name,"", rightClock], type, [],[],[])
            hole.addition = addition
            holes.append(hole)
        elif rightClock == "" and type != 4 and type != 5:
            hole = CCSL.hole(3, [name,leftClock, ""], type, [],[],[])
            hole.addition = addition
            holes.append(hole)
        else:
            expressions.append(CCSL.expression(name,type,[leftClock,rightClock],addition))
    spec = CCSL.CCSLSpecification()
    spec.refreshExpressions(expressions)
    spec.refreshRelations(relations)
    spec.refreshHole(holes)
    return spec

def readCCSLTraceFile(dictoryPath,clockNum,traceLen,traceNum = 5):
    traceArr = []
    files = os.listdir(dictoryPath)
    files.sort()
    traceCount = traceNum
    count = 0
    for file in files:
        if count >= traceCount:
            break

        if not os.path.isdir(file):
            if file.endswith(".trace"):
                count += 1
                traceArr.append(readCCSLTraceXML(dictoryPath + "/" + file, clockNum, traceLen))
    return traceArr

def readCCSLTraceXML(fileName,clockNum,traceLen):
    traceList = []
    ref = []
    for i in range(0,clockNum):
        traceList.append([])
        ref.append(i)
    domTree = parse(fileName)
    rootNode = domTree.documentElement
    count = 0
    for node in rootNode.getElementsByTagName("references"):
        if count >= clockNum:
            break
        for subNode in node.getElementsByTagName("elementRef"):
            if subNode.hasAttribute("href"):
                href = subNode.getAttribute("href")
                hrefList = href.split("@")
                if len(hrefList) == 3:
                    ref[count] = int((hrefList[2].split("."))[1])
                    count += 1
    for node in rootNode.getElementsByTagName("logicalSteps"):
        i = 0
        stepNum = 0
        if node.hasAttribute("stepNumber"):
            stepNum = int(node.getAttribute("stepNumber"))
        for subNode in node.getElementsByTagName("eventOccurrences"):
            if i <clockNum and not subNode.hasAttribute("eState") and stepNum <= traceLen:
                traceList[ref[i]].append(stepNum)
            i = i+1
    return traceList