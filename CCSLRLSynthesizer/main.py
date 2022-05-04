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

            # if isTest:
    # goldenFile = "./CCSLExample/case_timeSquare/example10/golden_t1"
    # goldenList = CCSLPaser.readGoldenList(goldenFile)
    # clockListPath = "./CCSLExample/case_timeSquare/example10/clocklist"
    # specPath = "./CCSLExample/case_timeSquare/example10/configure_t1.xml"
    # tracePath = "./CCSLExample/case_timeSquare/example10/trace"

    goldenFile = "./CCSLExample/WSP/golden_t1"
    goldenList = CCSLPaser.readGoldenList(goldenFile)
    clockListPath = "./CCSLExample/WSP/clocklist"
    specPath = "./CCSLExample/WSP/configure_t1.xml"
    tracePath = "./CCSLExample/WSP/trace"

    # goldenFile = "./CCSLBenchmark/Spec2/golden_spec2_2"
    # goldenList = CCSLPaser.readGoldenList(goldenFile)
    # clockListPath = "./CCSLBenchmark/Spec2/clocklist"
    # specPath = "./CCSLBenchmark/Spec2/Spec2_2.xml"
    # tracePath = "./CCSLBenchmark/Spec2/trace"

    clockLst = CCSLPaser.readClockList(clockListPath)
    spec = CCSLPaser.readCCSLConfigureXML(specPath)
    spec.refreshClockList(clockLst)
    traces = CCSLPaser.readCCSLTraceFile(tracePath, len(clockLst), traceLen, traceNum)
    round = 1000
    epsilon = 0.9
    # goldenList = [0]
    # goldenList = [0, 1, 1, 4, 1, 3, 1, 3, 4, 25, 7, 7, 11, 13, 23, 18, 19]
    # goldenList = [0, 2, 1]  # case 1 t2  spec1_1
    # goldenList = [4, 0, 2]  # case 1 t4  spec1_2
    # goldenList = [0, 4, 1, 1, 4, 1, 1, 1, 1, 1] #case 5 t1  spec2_1
    # goldenList = [7, 12, 0, 4, 12, 13, 14, 11, 0, 14] #case 5 t3
    # goldenList = [1, 0, 1, 1, 1, 1, 13, 11, 12, 3]  # case 5 t4  spec2_2
    # goldenList = [0, 0, 1, 1, 1, 4, 1, 4, 3, 1, 3, 3, 4, 1, 1, 1] #case6 t1
    # goldenList =[4, 21, 23, 7, 7, 6, 10, 10, 11, 11, 12, 17, 14, 25, 18, 19]
    # goldenList = [0, 1, 1, 4, 1, 3, 1, 3, 4, 25, 7, 7, 11, 13, 23, 18, 19] #case6 t3  spec3_1
    # goldenList = [1, 1, 4, 1, 4, 3, 1, 3, 3, 4, 1, 20, 7, 7, 18, 18] #case6 t4  spec3_2
    # goldenList = [1, 1, 3, 2] #new_case_1 t2  spec4_1
    # goldenList =[7, 8, 1, 4, 9, 5, 12] #new_case_1 t3  spec4_2
    # goldenList = [1,0,4] #case_base t1
    # goldenList = [1, 1, 0] #case_base t3
    # goldenList =[1, 2, 0, 3, 3, 3, 3, 3, 3, 1, 2, 0, 3, 3, 3, 3, 3, 1, 2, 0, 3, 3, 3, 3, 1, 2, 0, 3, 3, 3, 1, 2, 0, 3, 3, 1, 2, 0, 3, 1, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3]
    # goldenList = [1, 0, 1, 1, 1] #LandGear t1
    # goldenList = [1, 3, 3, 3, 3, 0] #LandGear t2
    # goldenList = [41, 1, 3, 3, 3, 3, 0] #LandGear t3
    # goldenList = [7, 10, 8, 1] #LandGear t4
    # print(spec)
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