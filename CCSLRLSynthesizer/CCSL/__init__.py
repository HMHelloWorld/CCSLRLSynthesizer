import copy
class expression:
    def __init__(self, name= "", type = -1, clockArr=None, addition=-1):
        if clockArr is None:
            clockArr = []
        self.name = name
        self.type = type
        self.clockArr = clockArr
        self.addition = addition
    def __copy__(self):
        expression.name = copy.deepcopy(self.name)
        expression.type = copy.deepcopy(self.type)
        expression.clockArr = copy.deepcopy(self.clockArr)
        expression.addition = copy.deepcopy(self.addition)
        return expression
    def __str__(self):
        if self.type == 4 or self.type == 5:
            return self.name + " = " + self.clockArr[0] + " " + getExpressionSymbol(self.type) + " " + str(self.addition)
        elif self.type == 6:
            return self.name + " = " + self.clockArr[0] + " " + getExpressionSymbol(self.type) + " " + str(self.addition) + " on " + self.clockArr[1]
        return self.name + " = " + self.clockArr[0] + " " + getExpressionSymbol(self.type) + " " + self.clockArr[1]
def getExpressionSymbol(expType):
    if expType == 0:
        return "+"
    elif expType == 1:
        return "*"
    elif expType == 2:
        return "&"
    elif expType == 3:
        return "|"
    elif expType == 4:
        return "$"
    elif expType == 5:
        return "periodic"
    elif expType == 6:
        return "$"
    else:
        return "irrelevant"

class relation:
    def __init__(self, type = -1, clockArr=None):
        if clockArr is None:
            clockArr = []
        self.type = type
        self.clockArr = clockArr
    def __copy__(self):
        relation.type = copy.deepcopy(self.type)
        relation.clockArr = copy.deepcopy(self.clockArr)
        return relation
    def __str__(self):
        return self.clockArr[0] + " " + getRelationSymbol(self.type) + " " + self.clockArr[1]

def getRelationSymbol(type):
    if type == 0:
        return "=="
    elif type == 1:
        return "<"
    elif type == 2:
        return "<="
    elif type == 3:
        return "#"
    elif type == 4:
        return "is subclock of"
    elif type == 5:
        return "alternative"
    else:
        return "irrelevant"

class hole:
    def __init__(self, holeType=0, clock_arr=None, type=-1, relate_relations=None, add_relations=None, relate_exps=None):
        if relate_exps is None:
            relate_exps = []
        if add_relations is None:
            add_relations = []
        if relate_relations is None:
            relate_relations = []
        if clock_arr is None:
            clock_arr = []
        self.holeType = holeType
        self.relateRelations = relate_relations
        self.clockArr = clock_arr
        self.type = type
        self.addRelations = add_relations
        self.relateExps = relate_exps
        self.addition = -1
    def __copy__(self):
        return hole(copy.deepcopy(self.holeType),copy.deepcopy(self.clockArr),copy.deepcopy(self.type),copy.deepcopy(self.relateRelations),copy.deepcopy(self.addRelations),copy.deepcopy(self.relateExps))
    def addRelation(self,rel):
        self.relateRelations.append(rel)
    def addExp(self,exp):
        self.relateExps.append(exp)
    def __str__(self):
        if self.holeType == 0:
            return self.clockArr[0] + " ?? " + self.clockArr[1]
        elif self.holeType == 1:
            if self.clockArr[0] == "":
                return "?? " + getRelationSymbol(self.type) + " " + self.clockArr[1]
            else:
                return self.clockArr[0] + " " + getRelationSymbol(self.type) + " ??"
        elif self.holeType == 2:
            if self.clockArr[2] == "":
                return self.clockArr[0] + " = " + self.clockArr[1] + " " + "??" + " " + self.addition
            return self.clockArr[0] + " = " + self.clockArr[1] + " " + "??" + " " + self.clockArr[2]
        else:
            if self.clockArr[1] == "":
                return self.clockArr[0] + " = " + "?? " + getExpressionSymbol(self.type) + " " + self.clockArr[2]
            else:
                return self.clockArr[0] + " = " + self.clockArr[1] + " " + getExpressionSymbol(self.type) + " ??"
class CCSLSpecification:
    def __init__(self):
        self.expressions = []
        self.clocks = []
        self.relations = []
        self.relClkHole = []
        self.relOptHole = []
        self.expClkHole = []
        self.expOptHole = []

    def __copy__(self):
        spec = CCSLSpecification()
        spec.expressions = copy.deepcopy(self.expressions)
        spec.clocks = copy.deepcopy(self.clocks)
        spec.relations = copy.deepcopy(self.relations)
        spec.relClkHole = copy.deepcopy(self.relClkHole)
        spec.relOptHole = copy.deepcopy(self.relOptHole)
        spec.expClkHole = copy.deepcopy(self.expClkHole)
        spec.expOptHole = copy.deepcopy(self.expOptHole)
        return spec
    def refreshClockList(self,clockArr):
        self.clocks = clockArr
    def getClockId(self,clockName):
        for i in range(0,len(self.clocks)):
            clock = self.clocks[i]
            if clock.name == clockName:
                return i
        for i in range(0,len(self.expressions)):
            expression = self.expressions[i]
            if expression.name == clockName:
                return i + len(self.clocks)
        for i in range(0,len(self.expOptHole)):
            expName = self.expOptHole[i].clockArr[0]
            if expName == clockName:
                return i + len(self.clocks) + len(self.expressions)
        for i in range(0,len(self.expClkHole)):
            expName = self.expClkHole[i].clockArr[0]
            if expName == clockName:
                return i + len(self.clocks) + len(self.expressions) + len(self.expOptHole)
        return -1
    def getClockList(self):
        clockList = []
        for i in range(0,len(self.clocks)):
            clockList.append(self.clocks[i].name)
        for i in range(0,len(self.expressions)):
            expression = self.expressions[i]
            clockList.append(expression.name)
        for i in range(0, len(self.expOptHole)):
            expName = self.expOptHole[i].clockArr[0]
            clockList.append(expName)
        for i in range(0,len(self.expClkHole)):
            expName = self.expClkHole[i].clockArr[0]
            clockList.append(expName)
        return clockList
    def fillHole(self,hole,fillId):
        if hole.holeType == 0:
            self.relations.append(relation(fillId,hole.clockArr))
        elif hole.holeType == 1:
            clockArr = []
            if hole.clockArr[0] == "":
                clockArr.append(self.getClockList()[fillId])
            else:
                clockArr.append(hole.clockArr[0])
            if hole.clockArr[1] == "":
                clockArr.append(self.getClockList()[fillId])
            else:
                clockArr.append(hole.clockArr[1])
            self.relations.append(relation(hole.type,clockArr))
        elif hole.holeType == 2:
            for exphole in self.expOptHole:
                if exphole.clockArr[0] == hole.clockArr[0]:
                    exphole.type = fillId
                    break
        else:
            for exphole in self.expClkHole:
                if exphole.clockArr[0] == hole.clockArr[0]:
                    for i in range(1,len(exphole.clockArr)):
                        if exphole.clockArr[i] == "":
                            exphole.clockArr[i] = self.getClockList()[fillId]
                            break
                    break
    def getHoleList(self):
        holeList = self.expClkHole + self.expOptHole + self.relOptHole + self.relClkHole
        return holeList
    def refreshExpressions(self,expArr):
        self.expressions = expArr
    def refreshRelations(self,relArr):
        self.relations = relArr
    def refreshHole(self,holes):
        for hole in holes:
            if hole.holeType == 0:
                self.relOptHole.append(hole)
            elif hole.holeType == 1:
                self.relClkHole.append(hole)
            elif hole.holeType == 2:
                for expression in self.expressions:
                    if expression.clockArr[0] == hole.clockArr[0]:
                        hole.addExp(expression)
                    elif len(expression.clockArr) > 1:
                        if expression.clockArr[1] == hole.clockArr[0]:
                            hole.addExp(expression)
                i = 0
                while i < len(hole.relateExps):
                    for expression in self.expressions:
                        relExp = hole.relateExps[i]
                        if expression.clockArr[0] == relExp.name:
                            hole.addExp(expression)
                        elif len(expression.clockArr) > 1:
                            if expression.clockArr[1] == relExp.name:
                                hole.addExp(expression)
                    i = i + 1
                for relation in self.relations:
                    if relation.clockArr[0] == hole.clockArr[0] or relation.clockArr[1] == hole.clockArr[0]:
                        hole.addRelation(relation)
                    for relExp in hole.relateExps:
                        if relation.clockArr[0] == relExp.name or relation.clockArr[1] == relExp.name:
                            hole.addRelation(relation)
                self.expOptHole.append(hole)
            else:
                for expression in self.expressions:
                    if expression.clockArr[0] == hole.clockArr[0]:
                        hole.addExp(expression)
                    elif len(expression.clockArr) > 1:
                        if expression.clockArr[1] == hole.clockArr[0]:
                            hole.addExp(expression)
                i = 0
                while i < len(hole.relateExps):
                    for expression in self.expressions:
                        relExp = hole.relateExps[i]
                        if expression.clockArr[0] == relExp.name:
                            hole.addExp(expression)
                        elif len(expression.clockArr) > 1:
                            if expression.clockArr[1] == relExp.name:
                                hole.addExp(expression)
                    i = i+1
                for relation in self.relations:
                    if relation.clockArr[0] == hole.clockArr[0] or relation.clockArr[1] == hole.clockArr[0]:
                        hole.addRelation(relation)
                    for relExp in hole.relateExps:
                        if relation.clockArr[0] == relExp.name or relation.clockArr[1] == relExp.name:
                            hole.addRelation(relation)
                self.expClkHole.append(hole)
    def __str__(self):
        str = ""
        for relation in self.relations:
            str += relation.__str__() + '\n'
        for expression in self.expressions:
            str += expression.__str__() + '\n'
        for hole in self.relOptHole:
            str += hole.__str__() + '\n'
        for hole in self.relClkHole:
            str += hole.__str__() + '\n'
        for hole in self.expOptHole:
            str += hole.__str__() + '\n'
        for hole in self.expClkHole:
            str += hole.__str__() + '\n'
        return str

    def getClockCount(self):
        return len(self.clocks) + len(self.expressions) + len(self.expOptHole) + len(self.expClkHole)

class clock:
    def __init__(self,type = -1,name = ""):
        self.name = name
        self.type = type
    def __copy__(self):
        clock.type = copy.deepcopy(self.type)
        clock.name = copy.deepcopy(self.name)
        return clock
    def __str__(self):
        return self.name