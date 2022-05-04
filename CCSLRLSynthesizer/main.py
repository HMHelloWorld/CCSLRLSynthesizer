import CCSLRLSynthesizer
import CCSLPaser
import time
import sys, getopt

def main(argv):
    clockListPath = ''
    specPath = ''
    tracePath = ''
    isTest = False
    traceLen = 50
    traceNum = 5
    round = 500
    times = 1
    try:
        opts, args = getopt.getopt(argv, "h", ["clocklist=", "spec=","trace_directory=","round=","trace_length=","trace_number=","test=","test_times="])
    except getopt.GetoptError:
        print 'Error: illegal command'
        print 'Command: main.py --clocklist <clocklistfile> --spec <specfile> --trace_directory <trace_directory>'
        print 'Optional: using \'--trace_length\' to set the length of traces.'
        print 'Optional: using \'--trace_number\' to set the number of traces.'
        print 'Optional: using \'--round\' to set reinforcement round.'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Command: main.py --clocklist <clocklistfile> --spec <specfile> --trace_directory <trace_directory>'
            print 'Optional: using \'--trace_length\' to set the length of traces.'
            print 'Optional: using \'--trace_number\' to set the number of traces.'
            print 'Optional: using \'--round\' to set reinforcement round.'
            sys.exit()
        if opt == ("--clocklist"):
            clockListPath = arg
            print "Clocklist file path: ", clockListPath
        if opt == ("--spec"):
            specPath = arg
            print "Specification file path: ", specPath
        if opt == ("--trace_directory"):
            tracePath = arg
            print "Trace directory path: ", tracePath
        if opt == "--test":
            goldenFile = arg
            isTest = True
            goldenList = CCSLPaser.readGoldenList(goldenFile)
            print "Golden list file path: ", tracePath
        if opt == "--test_times":
            times = int(arg)
        if opt == ("--trace_length"):
            traceLen = int(arg)
        if opt == ("--trace_number"):
            traceNum = int(arg)
        if opt == ("--round"):
            round = int(arg)
    if clockListPath == '':
        print 'Error: Missing clock list file!!!'
        print 'main.py -clocklist <clocklistfile> -spec <specfile> -trace_directory <trace_directory>'
        return
    if specPath == '':
        print 'Error: Missing specification file!!!'
        print 'main.py -clocklist <clocklistfile> -spec <specfile> -trace_directory <trace_directory>'
        return
    if tracePath == '':
        print 'Error: Missing trace file!!!'
        print 'main.py -clocklist <clocklistfile> -spec <specfile> -trace_directory <trace_directory>'
        return


    clockLst = CCSLPaser.readClockList(clockListPath)
    spec = CCSLPaser.readCCSLConfigureXML(specPath)
    spec.refreshClockList(clockLst)
    traces = CCSLPaser.readCCSLTraceFile(tracePath, len(clockLst), traceLen, traceNum)
    # round = 1000
    epsilon = 0.9

    rightCount = 0
    t = 0
    for i in range(times):
        time_start = time.time()
        specResult, chooseList = CCSLRLSynthesizer.ccslReinforcemenceLarning(round, epsilon, spec, traces, traceLen)
        time_end = time.time()
        sumTime = time_end - time_start
        t = t + sumTime
        # print(specResult)
        print(chooseList)
        if isTest:
            if chooseList == goldenList:
                rightCount += 1
                acc = float(rightCount) / float(i+1)
                print ("round: %d/%d accuracy: %f%%" % (i+1,times,acc*100))
        # else:
        # print specResult
        #     print(chooseList)
        # if i % 50 == 49:
        #     print("rightCount :%d" % (rightCount))
    if isTest:
        acc = float(rightCount) / float(times)
        # print(rightCount)
        # print(" round:%d traceNum:%d accuracy :%f" % (round, traceNum, acc))
        print("round: %d\ntrace number: %d\ntrace length: %d\nrun time: %f\naccuracy: %f%%" % (round, traceNum, traceLen,(t / times), acc*100))
        # print(" round:%d  \n time :%f" % (round, t / times))
    else:
        print("round: %d\ntrace number: %d\ntrace length: %d" % (round, traceNum, traceLen))
        print specResult
    # traceNum = traceNum + 1
    # traceLen = traceLen + 10
    # if r < 1000:
    #     r = r+ 100
    # else:
    #     r = r + 1000

if __name__ == "__main__":
   main(sys.argv[1:])