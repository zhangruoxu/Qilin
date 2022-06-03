#!/usr/bin/env python3

import util.Util as Util
import util.TerminalColor as tc
import numpy as np
from util.conchPreTimeTable import buildAppNameToTimeList

# includeEagle = False
includeEagle = True

def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))

# calclate precision difference
def precisionDifference(baseLineMetric, compareMetric):
    bm = float(baseLineMetric)
    cm = float(compareMetric)
    return abs(cm - bm) / bm

# compute CI ratio for one app
def computeCIRatio(conchCS, conchCI):
    mret = (conchCI * 1.0 ) / (conchCI + conchCS)
    return mret

def getTexDataCommand(cmdName, cmdValue):
    tex = '\\newcommand{\\' + cmdName + '}{' + cmdValue + '\\xspace}'
    return tex

def toPercentageStr(val, n = 1):
    if n != 1:
        s = '%.' + str(n) + 'f'
        return s % (val * 100) + '\%'
    else:
        return '%.1f' % (val * 100) + '\%'

def buildToolNameToTime(app2times, timeOrderList):
    ret = {}
    for i in range(len(timeOrderList)):
        tool = timeOrderList[i]
        mList = []
        for app in app2times:
            mTime = app2times[app][i]
            mList.append(mTime)
        ret[tool] = mList
    return ret

# calculate statistic data for using in the paper.
# argument is of PTAOutput type.
def dumpDataCommandUsedInPaper(allPtaOutput, outputfile, verbose):
    # context-dependent objects percentage data.
    minmaxCiRatioApp = ['unknown', 'unknown']
    ciratio = [1.0, 0.0, 0.0]
    # may-casting, call-edges, poly-calls, reach-mthds, avg-pts.
    precisionDiff2OBJ = [0.0, 0.0, 0.0, 0.0, 0.0]
    precisionDiffz2OBJ = [0.0, 0.0, 0.0, 0.0, 0.0]
    precisionDiffe2OBJ = [0.0, 0.0, 0.0, 0.0, 0.0]
    precisionDiff3OBJ = [0.0, 0.0, 0.0, 0.0, 0.0]
    precisionDiffz3OBJ = [0.0, 0.0, 0.0, 0.0, 0.0]
    precisionDiffe3OBJ = [0.0, 0.0, 0.0, 0.0, 0.0]
    # min, avg, max, geometry mean
    speedUp2OBJ = [100.0, 0.0, 0.0, 1.0]
    minmaxApps2OBJ = ['unknown', 'unknown']
    speedUpz2OBJ = [100.0, 0.0, 0.0, 1.0]
    minmaxAppsz2OBJ = ['unknown', 'unknown']
    speedUpe2OBJ = [100.0, 0.0, 0.0, 1.0]
    minmaxAppse2OBJ = ['unknown', 'unknown']
    speedUp3OBJ = [100.0, 0.0, 0.0, 1.0]
    minmaxApps3OBJ = ['unknown', 'unknown']
    speedUpz3OBJ = [100.0, 0.0, 0.0, 1.0]
    minmaxAppsz3OBJ = ['unknown', 'unknown']
    speedUpe3OBJ = [100.0, 0.0, 0.0, 1.0]
    minmaxAppse3OBJ = ['unknown', 'unknown']
    # avg speedup considering OOM/Timeout.
    # kobj, eagle, zipper.
    avgSpeedUp = [0.0, 0.0, 0.0]
    # zipper/eagle speed up: [k=2, k = 3]
    zeCnt = [0, 0]
    avgSpeedUpZipperOverEagle = [0.0, 0.0]
    avgSpeedUpZipperOverEagleForall = [0.0, 0.0]

    ret = Util.classifyByAppName(allPtaOutput)
    # [0]->#app; [1]->#scale2obj; [2]->#scaleZ2obj; [3]->#scale3obj; [4]->#scaleZ3obj; [5]->#scaleE2obj; [6]->#scaleE3obj;
    cnt = [0, 0, 0, 0, 0, 0, 0]
    # xalan speedup 3Dvs2D
    xalan3vs2D = 0
    for key in ret:
        cnt[0] += 1
        anaName2Obj = Util.buildAnalysisNameToObjMap(ret[key])
        s2o = anaName2Obj['2o']
        s2od = anaName2Obj['2o+D']
        z2o = anaName2Obj['Z-2o']
        z2od = anaName2Obj['Z-2o+D']
        e2o = anaName2Obj['E-2o']
        e2od = anaName2Obj['E-2o+D']
        s3o = anaName2Obj['3o']
        s3od = anaName2Obj['3o+D']
        z3o = anaName2Obj['Z-3o']
        z3od = anaName2Obj['Z-3o+D']
        e3o = anaName2Obj['E-3o']
        e3od = anaName2Obj['E-3o+D']
        if key == 'xalan':
            z3od = anaName2Obj['Z-3o+D']
            xalan3vs2D = Util.computeSpeedUp(z2od, z3od)
        # cs ratio
        mret = computeCIRatio(z2od.conchCS, z2od.conchCI)
        if mret < ciratio[0]:
            ciratio[0] = mret
            minmaxCiRatioApp[0] = key
        if mret > ciratio[2]:
            ciratio[2] = mret
            minmaxCiRatioApp[1] = key
        ciratio[1] += mret
        # compute speedups, and precision difference for 2OBJ
        if s2o.analysisCompleted() and s2od.analysisCompleted():
            cnt[1] += 1
            mret = Util.computeSpeedUp(s2o, s2od)
            if mret < speedUp2OBJ[0]:
                speedUp2OBJ[0] = mret
                minmaxApps2OBJ[0] = key
            if mret > speedUp2OBJ[2]:
                speedUp2OBJ[2] = mret
                minmaxApps2OBJ[1] = key
            speedUp2OBJ[1] += mret
            speedUp2OBJ[3] *= mret
            avgSpeedUp[0] += mret

            precisionDiff2OBJ[0] += precisionDifference(s2o.mayFailCasts, s2od.mayFailCasts)
            precisionDiff2OBJ[1] += precisionDifference(s2o.callEdges, s2od.callEdges)
            precisionDiff2OBJ[2] += precisionDifference(s2o.polyCalls, s2od.polyCalls)
            precisionDiff2OBJ[3] += precisionDifference(s2o.reachMethods, s2od.reachMethods)
            precisionDiff2OBJ[4] += precisionDifference(s2o.avgPointsToSize, s2od.avgPointsToSize)
        else:
            avgSpeedUp[0] += Util.computeSpeedUp(s2o, s2od)

        # compute speedups, and precision difference for Z2OBJ
        if z2o.analysisCompleted() and z2od.analysisCompleted():
            cnt[2] += 1
            mret = Util.computeSpeedUp(z2o, z2od)
            if mret < speedUpz2OBJ[0]:
                speedUpz2OBJ[0] = mret
                minmaxAppsz2OBJ[0] = key
            if mret > speedUpz2OBJ[2]:
                speedUpz2OBJ[2] = mret
                minmaxAppsz2OBJ[1] = key
            speedUpz2OBJ[1] += mret
            speedUpz2OBJ[3] *= mret
            avgSpeedUp[2] += mret

            precisionDiffz2OBJ[0] += precisionDifference(z2o.mayFailCasts, z2od.mayFailCasts)
            precisionDiffz2OBJ[1] += precisionDifference(z2o.callEdges, z2od.callEdges)
            precisionDiffz2OBJ[2] += precisionDifference(z2o.polyCalls, z2od.polyCalls)
            precisionDiffz2OBJ[3] += precisionDifference(z2o.reachMethods, z2od.reachMethods)
            precisionDiffz2OBJ[4] += precisionDifference(z2o.avgPointsToSize, z2od.avgPointsToSize)
        else:
            avgSpeedUp[2] += Util.computeSpeedUp(z2o, z2od)

	    # compute speedups, and precision difference for E2OBJ
        if e2o.analysisCompleted() and e2od.analysisCompleted():
            cnt[5] += 1
            mret = Util.computeSpeedUp(e2o, e2od)
            if mret < speedUpe2OBJ[0]:
                speedUpe2OBJ[0] = mret
                minmaxAppse2OBJ[0] = key
            if mret > speedUpe2OBJ[2]:
                speedUpe2OBJ[2] = mret
                minmaxAppse2OBJ[1] = key
            speedUpe2OBJ[1] += mret
            speedUpe2OBJ[3] *= mret
            avgSpeedUp[1] += mret

            precisionDiffe2OBJ[0] += precisionDifference(e2o.mayFailCasts, e2od.mayFailCasts)
            precisionDiffe2OBJ[1] += precisionDifference(e2o.callEdges, e2od.callEdges)
            precisionDiffe2OBJ[2] += precisionDifference(e2o.polyCalls, e2od.polyCalls)
            precisionDiffe2OBJ[3] += precisionDifference(e2o.reachMethods, e2od.reachMethods)
            precisionDiffe2OBJ[4] += precisionDifference(e2o.avgPointsToSize, e2od.avgPointsToSize)
        else:
            avgSpeedUp[1] += Util.computeSpeedUp(e2o, e2od)

#         avgSpeedUpZipperOverEagle = [0.0, 0.0]
#         avgSpeedUpZipperOverEagleForall = [0.0, 0.0]
#         zeCnt = [0, 0]
        if e2o.analysisCompleted() and z2o.analysisCompleted():
            zeCnt[0] += 1
            avgSpeedUpZipperOverEagle[0] += Util.computeSpeedUp(e2o, z2o)
            avgSpeedUpZipperOverEagleForall[0] += Util.computeSpeedUp(e2o, z2o)
        else:
            avgSpeedUpZipperOverEagleForall[0] += Util.computeSpeedUp(e2o, z2o)

        # compute speedups, and precision difference for 3OBJ
        if s3o.analysisCompleted() and s3od.analysisCompleted():
            cnt[3] += 1
            mret = Util.computeSpeedUp(s3o, s3od)
            if mret < speedUp3OBJ[0]:
                speedUp3OBJ[0] = mret
                minmaxApps3OBJ[0] = key
            if mret > speedUp3OBJ[2]:
                speedUp3OBJ[2] = mret
                minmaxApps3OBJ[1] = key
            speedUp3OBJ[1] += mret
            speedUp3OBJ[3] *= mret
            avgSpeedUp[0] += mret

            precisionDiff3OBJ[0] += precisionDifference(s3o.mayFailCasts, s3od.mayFailCasts)
            precisionDiff3OBJ[1] += precisionDifference(s3o.callEdges, s3od.callEdges)
            precisionDiff3OBJ[2] += precisionDifference(s3o.polyCalls, s3od.polyCalls)
            precisionDiff3OBJ[3] += precisionDifference(s3o.reachMethods, s3od.reachMethods)
            precisionDiff3OBJ[4] += precisionDifference(s3o.avgPointsToSize, s3od.avgPointsToSize)
        else:
            avgSpeedUp[0] += Util.computeSpeedUp(s3o, s3od)

        # compute speedups, and precision difference for Z3OBJ
        if z3o.analysisCompleted() and z3od.analysisCompleted():
            cnt[4] += 1
            mret = Util.computeSpeedUp(z3o, z3od)
            if mret < speedUpz3OBJ[0]:
                speedUpz3OBJ[0] = mret
                minmaxAppsz3OBJ[0] = key
            if mret > speedUpz3OBJ[2]:
                speedUpz3OBJ[2] = mret
                minmaxAppsz3OBJ[1] = key
            speedUpz3OBJ[1] += mret
            speedUpz3OBJ[3] *= mret
            avgSpeedUp[2] += mret

            precisionDiffz3OBJ[0] += precisionDifference(z3o.mayFailCasts, z3od.mayFailCasts)
            precisionDiffz3OBJ[1] += precisionDifference(z3o.callEdges, z3od.callEdges)
            precisionDiffz3OBJ[2] += precisionDifference(z3o.polyCalls, z3od.polyCalls)
            precisionDiffz3OBJ[3] += precisionDifference(z3o.reachMethods, z3od.reachMethods)
            precisionDiffz3OBJ[4] += precisionDifference(z3o.avgPointsToSize, z3od.avgPointsToSize)
        else:
            avgSpeedUp[2] += Util.computeSpeedUp(z3o, z3od)

        # compute speedups, and precision difference for E3OBJ
        if e3o.analysisCompleted() and e3od.analysisCompleted():
            cnt[6] += 1
            mret = Util.computeSpeedUp(e3o, e3od)
            if mret < speedUpe3OBJ[0]:
                speedUpe3OBJ[0] = mret
                minmaxAppse3OBJ[0] = key
            if mret > speedUpe3OBJ[2]:
                speedUpe3OBJ[2] = mret
                minmaxAppse3OBJ[1] = key
            speedUpe3OBJ[1] += mret
            speedUpe3OBJ[3] *= mret
            avgSpeedUp[1] += mret

            precisionDiffe3OBJ[0] += precisionDifference(e3o.mayFailCasts, e3od.mayFailCasts)
            precisionDiffe3OBJ[1] += precisionDifference(e3o.callEdges, e3od.callEdges)
            precisionDiffe3OBJ[2] += precisionDifference(e3o.polyCalls, e3od.polyCalls)
            precisionDiffe3OBJ[3] += precisionDifference(e3o.reachMethods, e3od.reachMethods)
            precisionDiffe3OBJ[4] += precisionDifference(e3o.avgPointsToSize, e3od.avgPointsToSize)
        else:
            avgSpeedUp[1] += Util.computeSpeedUp(e3o, e3od)

        if e3o.analysisCompleted() and z3o.analysisCompleted():
            zeCnt[1] += 1
            avgSpeedUpZipperOverEagle[1] += Util.computeSpeedUp(e3o, z3o)
            avgSpeedUpZipperOverEagleForall[1] += Util.computeSpeedUp(e3o, z3o)
        else:
            avgSpeedUpZipperOverEagleForall[1] += Util.computeSpeedUp(e3o, z3o)

    # compute average data
    precisionDiff2OBJ[0] /= cnt[1]
    precisionDiff2OBJ[1] /= cnt[1]
    precisionDiff2OBJ[2] /= cnt[1]
    precisionDiff2OBJ[3] /= cnt[1]
    precisionDiff2OBJ[4] /= cnt[1]

    precisionDiffz2OBJ[0] /= cnt[2]
    precisionDiffz2OBJ[1] /= cnt[2]
    precisionDiffz2OBJ[2] /= cnt[2]
    precisionDiffz2OBJ[3] /= cnt[2]
    precisionDiffz2OBJ[4] /= cnt[2]

    precisionDiffe2OBJ[0] /= cnt[5]
    precisionDiffe2OBJ[1] /= cnt[5]
    precisionDiffe2OBJ[2] /= cnt[5]
    precisionDiffe2OBJ[3] /= cnt[5]
    precisionDiffe2OBJ[4] /= cnt[5]

    precisionDiff3OBJ[0] /= cnt[3]
    precisionDiff3OBJ[1] /= cnt[3]
    precisionDiff3OBJ[2] /= cnt[3]
    precisionDiff3OBJ[3] /= cnt[3]
    precisionDiff3OBJ[4] /= cnt[3]

    precisionDiffz3OBJ[0] /= cnt[4]
    precisionDiffz3OBJ[1] /= cnt[4]
    precisionDiffz3OBJ[2] /= cnt[4]
    precisionDiffz3OBJ[3] /= cnt[4]
    precisionDiffz3OBJ[4] /= cnt[4]

    precisionDiffe3OBJ[0] /= cnt[6]
    precisionDiffe3OBJ[1] /= cnt[6]
    precisionDiffe3OBJ[2] /= cnt[6]
    precisionDiffe3OBJ[3] /= cnt[6]
    precisionDiffe3OBJ[4] /= cnt[6]

    # overallAvgSpeedUp = ( speedUp2OBJ[1] + speedUpz2OBJ[1] + speedUp3OBJ[1] + speedUpz3OBJ[1]) / (cnt[1] + cnt[2] + cnt[3] + cnt[4])
    # overallMaxSpeedUp = max([speedUp2OBJ[2], speedUpz2OBJ[2], speedUp3OBJ[2], speedUpz3OBJ[2]])
    if includeEagle:
        overallAvgSpeedUp = ( speedUp2OBJ[1] + speedUpz2OBJ[1] + speedUp3OBJ[1] + speedUpz3OBJ[1] + speedUpe2OBJ[1] + speedUpe3OBJ[1]) / (cnt[1] + cnt[2] + cnt[3] + cnt[4] + cnt[5] + cnt[6])
        overallAvgGMSpeedUp = ( speedUp2OBJ[3] * speedUpz2OBJ[3] * speedUp3OBJ[3] * speedUpz3OBJ[3] * speedUpe2OBJ[3] * speedUpe3OBJ[3]) **(1.0/(cnt[1] + cnt[2] + cnt[3] + cnt[4] + cnt[5] + cnt[6]))
    else:
        overallAvgSpeedUp = ( speedUp2OBJ[1] + speedUpz2OBJ[1] + speedUp3OBJ[1] + speedUpz3OBJ[1]) / (cnt[1] + cnt[2] + cnt[3] + cnt[4])
        overallAvgGMSpeedUp = ( speedUp2OBJ[3] * speedUpz2OBJ[3] * speedUp3OBJ[3] * speedUpz3OBJ[3] ) **(1.0/(cnt[1] + cnt[2] + cnt[3] + cnt[4]))

    overallMaxSpeedUp = max([speedUp2OBJ[2], speedUpz2OBJ[2], speedUp3OBJ[2], speedUpz3OBJ[2], speedUpe2OBJ[2], speedUpe3OBJ[2]])
    zipperAvgSpeedUp = (speedUpz2OBJ[1] + speedUpz3OBJ[1])/(cnt[2] + cnt[4])
    zipperAvgGMSpeedUp =  (speedUpz2OBJ[3] * speedUpz3OBJ[3]) **(1.0/(cnt[2] + cnt[4]))
    kobjAvgSpeedUp = (speedUp2OBJ[1] + speedUp3OBJ[1]) / (cnt[1] + cnt[3])
    kobjAvgGMSpeedUp = (speedUp2OBJ[3] * speedUp3OBJ[3]) ** (1.0 / (cnt[1] + cnt[3]))
    eagleAvgSpeedUp = (speedUpe2OBJ[1] + speedUpe3OBJ[1]) / (cnt[5] + cnt[6])
    eagleAvgGMSpeedUp = (speedUpe2OBJ[3] * speedUpe3OBJ[3]) ** (1.0 / (cnt[5] + cnt[6]))
    zipperAvgSpeedUpForAll = avgSpeedUp[2] / 24.0
    eagleAvgSpeedUpForAll = avgSpeedUp[1] / 24.0
    kobjAvgSpeedUpForAll = avgSpeedUp[0] / 24.0
    zipperOverEagleAvgSpeedUpForAll = (avgSpeedUpZipperOverEagleForall[0] + avgSpeedUpZipperOverEagleForall[1]) / 24.0
    zipperOverEagleAvgSpeedUp = (avgSpeedUpZipperOverEagle[0] + avgSpeedUpZipperOverEagle[1]) / (zeCnt[0] + zeCnt[1])

    speedUp2OBJGM = speedUp2OBJ[3] ** (1.0 / cnt[1])
    speedUp2OBJ[1] /= cnt[1]
    speedUpz2OBJGM = speedUpz2OBJ[3] ** (1.0 / cnt[2])
    speedUpz2OBJ[1] /= cnt[2]
    speedUpe2OBJGM = speedUpe2OBJ[3] ** (1.0 / cnt[5])
    speedUpe2OBJ[1] /= cnt[5]
    speedUp3OBJGM = speedUp3OBJ[3] ** (1.0 / cnt[3])
    speedUp3OBJ[1] /= cnt[3]
    speedUpz3OBJGM = speedUpz3OBJ[3] ** (1.0 / cnt[4])
    speedUpz3OBJ[1] /= cnt[4]
    speedUpe3OBJGM = speedUpe3OBJ[3] ** (1.0 / cnt[6])
    speedUpe3OBJ[1] /= cnt[6]



    ciratio[1] /= cnt[0]

    # times used by pre-analysis.
    ret = Util.classifyByAppName(allPtaOutput)
    app2times = buildAppNameToTimeList(ret)
    tool2appstime = buildToolNameToTime(app2times, ['spark', 'zipper', 'conch', 'eagle'])
    sparkPreTime = tool2appstime['spark']
    zipperPreTime = tool2appstime['zipper']
    eaglePreTime = tool2appstime['eagle']
    conchPreTime = tool2appstime['conch']
    avgSparkTime = sum(sparkPreTime) / len(sparkPreTime)
    avgZipperTime = sum(zipperPreTime) / len(zipperPreTime)
    avgEagleTime = sum(eaglePreTime) / len(eaglePreTime)
    avgConchTime = sum(conchPreTime) / len(conchPreTime)
    avgSparkTimeGM = np.prod(sparkPreTime) ** (1.0 / len(sparkPreTime))
    avgZipperTimeGM = np.prod(zipperPreTime) ** (1.0 / len(zipperPreTime))
    avgEagleTimeGM = np.prod(eaglePreTime) ** (1.0 / len(eaglePreTime))
    avgConchTimeGM = np.prod(conchPreTime) ** (1.0 / len(conchPreTime))


    if verbose:
        print('average ' + tc.GREEN + 'zipper-2obj+D' + tc.RESET + ' speed up:' + str(speedUpz2OBJ[1]))
        print(minmaxAppsz2OBJ[1] + ' in ' + tc.GREEN + 'zipper-2obj+D' + tc.RESET + ' has the max speed up:' + str(speedUpz2OBJ[2]))
        print(minmaxAppsz2OBJ[0] + ' in ' + tc.GREEN + 'zipper-2obj+D' + tc.RESET + ' has the min speed up:' + str(speedUpz2OBJ[0]))
        print('average ' + tc.GREEN + 'eagle-2obj+D' + tc.RESET + ' speed up:' + str(speedUpe2OBJ[1]))
        print(minmaxAppse2OBJ[1] + ' in ' + tc.GREEN + 'eagle-2obj+D' + tc.RESET + ' has the max speed up:' + str(speedUpe2OBJ[2]))
        print(minmaxAppse2OBJ[0] + ' in ' + tc.GREEN + 'eagle-2obj+D' + tc.RESET + ' has the min speed up:' + str(speedUpe2OBJ[0]))
        print('average ' + tc.GREEN + '2obj+D' + tc.RESET + ' speed up:' + str(speedUp2OBJ[1]))
        print(minmaxApps2OBJ[1] + ' in ' + tc.GREEN + '2obj+D' + tc.RESET + ' has the max speed up:' + str(speedUp2OBJ[2]))
        print(minmaxApps2OBJ[0] + ' in ' + tc.GREEN + '2obj+D' + tc.RESET + ' has the min speed up:' + str(speedUp2OBJ[0]))

        print('average ' + tc.GREEN + 'zipper-3obj+D' + tc.RESET + ' speed up:' + str(speedUpz3OBJ[1]))
        print(minmaxAppsz3OBJ[1] + ' in ' + tc.GREEN + 'zipper-3obj+D' + tc.RESET + ' has the max speed up:' + str(speedUpz3OBJ[2]))
        print(minmaxAppsz3OBJ[0] + ' in ' + tc.GREEN + 'zipper-3obj+D' + tc.RESET + ' has the min speed up:' + str(speedUpz3OBJ[0]))
        print('average ' + tc.GREEN + 'eagle-3obj+D' + tc.RESET + ' speed up:' + str(speedUpe3OBJ[1]))
        print(minmaxAppse3OBJ[1] + ' in ' + tc.GREEN + 'eagle-3obj+D' + tc.RESET + ' has the max speed up:' + str(speedUpe3OBJ[2]))
        print(minmaxAppse3OBJ[0] + ' in ' + tc.GREEN + 'eagle-3obj+D' + tc.RESET + ' has the min speed up:' + str(speedUpe3OBJ[0]))
        print('average ' + tc.GREEN + '3obj+D' + tc.RESET + ' speed up:' + str(speedUp3OBJ[1]))
        print(minmaxApps3OBJ[1] + ' in ' + tc.GREEN + '3obj+D' + tc.RESET + ' has the max speed up:' + str(speedUp3OBJ[2]))
        print(minmaxApps3OBJ[0] + ' in ' + tc.GREEN + '3obj+D' + tc.RESET + ' has the min speed up:' + str(speedUp3OBJ[0]))

        print('precision difference of 2obj over the five metrics:')
        print(precisionDiff2OBJ)
        print('precision difference of z2obj over the five metrics:')
        print(precisionDiffz2OBJ)
        print('precision difference of e2obj over the five metrics:')
        print(precisionDiffe2OBJ)

        print('precision difference of 3obj over the five metrics:')
        print(precisionDiff3OBJ)
        print('precision difference of z3obj over the five metrics:')
        print(precisionDiffz3OBJ)
        print('precision difference of e3obj over the five metrics:')
        print(precisionDiffe3OBJ)

        print('average ci ratio is %.3f' % ciratio[1])
        print('min ci ratio is %.3f for %s' % (ciratio[0], minmaxCiRatioApp[0]))
        print('max ci ratio is %.3f for %s' % (ciratio[2], minmaxCiRatioApp[1]))

        print('xalan\'s speedup of z3objD over z2objD is %.2f' % xalan3vs2D)

        print('average Spark pre-time is %.1f' % avgSparkTime)
        print('average Eagle pre-time is %.1f' % avgEagleTime)
        print('average Zipper pre-time is %.1f' % avgZipperTime)
        print('average Conch pre-time is %.1f' % avgConchTime)
        print('average GM Spark pre-time is %.1f' % avgSparkTimeGM)
        print('average GM Eagle pre-time is %.1f' % avgEagleTimeGM)
        print('average GM Zipper pre-time is %.1f' % avgZipperTimeGM)
        print('average GM Conch pre-time is %.1f' % avgConchTimeGM)

        print('overall average speed up is %.1f' % overallAvgSpeedUp)
        print('overall max speed up is %.1f' % overallMaxSpeedUp)

    # generate tex command for data used in our paper.
    cmdList = []
    cmdList.append(getTexDataCommand('ztwoobjfailCastDiff', toPercentageStr(precisionDiffz2OBJ[0], 2)))
    cmdList.append(getTexDataCommand('ztwoobjpolyCallDiff', toPercentageStr(precisionDiffz2OBJ[1], 2)))
    cmdList.append(getTexDataCommand('ztwoobjcallEdgeDiff', toPercentageStr(precisionDiffz2OBJ[2], 2)))
    cmdList.append(getTexDataCommand('ztwoobjreachMthdDiff', toPercentageStr(precisionDiffz2OBJ[3], 2)))
    cmdList.append(getTexDataCommand('ztwoobjavgPtsDiff', toPercentageStr(precisionDiffz2OBJ[4], 2)))

    cmdList.append(getTexDataCommand('etwoobjfailCastDiff', toPercentageStr(precisionDiffe2OBJ[0], 2)))
    cmdList.append(getTexDataCommand('etwoobjpolyCallDiff', toPercentageStr(precisionDiffe2OBJ[1], 2)))
    cmdList.append(getTexDataCommand('etwoobjcallEdgeDiff', toPercentageStr(precisionDiffe2OBJ[2], 2)))
    cmdList.append(getTexDataCommand('etwoobjreachMthdDiff', toPercentageStr(precisionDiffe2OBJ[3], 2)))
    cmdList.append(getTexDataCommand('etwoobjavgPtsDiff', toPercentageStr(precisionDiffe2OBJ[4], 2)))

    cmdList.append(getTexDataCommand('stwoobjfailCastDiff', toPercentageStr(precisionDiff2OBJ[0], 2)))
    cmdList.append(getTexDataCommand('stwoobjpolyCallDiff', toPercentageStr(precisionDiff2OBJ[1], 2)))
    cmdList.append(getTexDataCommand('stwoobjcallEdgeDiff', toPercentageStr(precisionDiff2OBJ[2], 2)))
    cmdList.append(getTexDataCommand('stwoobjreachMthdDiff', toPercentageStr(precisionDiff2OBJ[3], 2)))
    cmdList.append(getTexDataCommand('stwoobjavgPtsDiff', toPercentageStr(precisionDiff2OBJ[4], 2)))

    cmdList.append(getTexDataCommand('zthreeobjfailCastDiff', toPercentageStr(precisionDiffz3OBJ[0], 2)))
    cmdList.append(getTexDataCommand('zthreeobjpolyCallDiff', toPercentageStr(precisionDiffz3OBJ[1], 2)))
    cmdList.append(getTexDataCommand('zthreeobjcallEdgeDiff', toPercentageStr(precisionDiffz3OBJ[2], 2)))
    cmdList.append(getTexDataCommand('zthreeobjreachMthdDiff', toPercentageStr(precisionDiffz3OBJ[3], 2)))
    cmdList.append(getTexDataCommand('zthreeobjavgPtsDiff', toPercentageStr(precisionDiffz3OBJ[4], 2)))

    cmdList.append(getTexDataCommand('ethreeobjfailCastDiff', toPercentageStr(precisionDiffe3OBJ[0], 2)))
    cmdList.append(getTexDataCommand('ethreeobjpolyCallDiff', toPercentageStr(precisionDiffe3OBJ[1], 2)))
    cmdList.append(getTexDataCommand('ethreeobjcallEdgeDiff', toPercentageStr(precisionDiffe3OBJ[2], 2)))
    cmdList.append(getTexDataCommand('ethreeobjreachMthdDiff', toPercentageStr(precisionDiffe3OBJ[3], 2)))
    cmdList.append(getTexDataCommand('ethreeobjavgPtsDiff', toPercentageStr(precisionDiffe3OBJ[4], 2)))

    cmdList.append(getTexDataCommand('sthreeobjfailCastDiff', toPercentageStr(precisionDiff3OBJ[0], 2)))
    cmdList.append(getTexDataCommand('sthreeobjpolyCallDiff', toPercentageStr(precisionDiff3OBJ[1], 2)))
    cmdList.append(getTexDataCommand('sthreeobjcallEdgeDiff', toPercentageStr(precisionDiff3OBJ[2], 2)))
    cmdList.append(getTexDataCommand('sthreeobjreachMthdDiff', toPercentageStr(precisionDiff3OBJ[3], 2)))
    cmdList.append(getTexDataCommand('sthreeobjavgPtsDiff', toPercentageStr(precisionDiff3OBJ[4], 2)))

    cmdList.append(getTexDataCommand('ztwoobjMinSpeedUp', Util.toSpeedUpStr(speedUpz2OBJ[0])))
    cmdList.append(getTexDataCommand('ztwoobjMinSpeedUpApp', '\\texttt{' + minmaxAppsz2OBJ[0] + '}'))
    cmdList.append(getTexDataCommand('ztwoobjAvgSpeedUp', Util.toSpeedUpStr(speedUpz2OBJ[1])))
    cmdList.append(getTexDataCommand('ztwoobjAvgSpeedUpGM', Util.toSpeedUpStr(speedUpz2OBJGM)))
    cmdList.append(getTexDataCommand('ztwoobjMaxSpeedUp', Util.toSpeedUpStr(speedUpz2OBJ[2])))
    cmdList.append(getTexDataCommand('ztwoobjMaxSpeedUpApp', '\\texttt{' + minmaxAppsz2OBJ[1] + '}'))

    cmdList.append(getTexDataCommand('etwoobjMinSpeedUp', Util.toSpeedUpStr(speedUpe2OBJ[0])))
    cmdList.append(getTexDataCommand('etwoobjMinSpeedUpApp', '\\texttt{' + minmaxAppse2OBJ[0] + '}'))
    cmdList.append(getTexDataCommand('etwoobjAvgSpeedUp', Util.toSpeedUpStr(speedUpe2OBJ[1])))
    cmdList.append(getTexDataCommand('etwoobjAvgSpeedUpGM', Util.toSpeedUpStr(speedUpe2OBJGM)))
    cmdList.append(getTexDataCommand('etwoobjMaxSpeedUp', Util.toSpeedUpStr(speedUpe2OBJ[2])))
    cmdList.append(getTexDataCommand('etwoobjMaxSpeedUpApp', '\\texttt{' + minmaxAppse2OBJ[1] + '}'))

    cmdList.append(getTexDataCommand('stwoobjMinSpeedUp', Util.toSpeedUpStr(speedUp2OBJ[0])))
    cmdList.append(getTexDataCommand('stwoobjMinSpeedUpApp', '\\texttt{' + minmaxApps2OBJ[0] + '}'))
    cmdList.append(getTexDataCommand('stwoobjAvgSpeedUp', Util.toSpeedUpStr(speedUp2OBJ[1])))
    cmdList.append(getTexDataCommand('stwoobjAvgSpeedUpGM', Util.toSpeedUpStr(speedUp2OBJGM)))
    cmdList.append(getTexDataCommand('stwoobjMaxSpeedUp', Util.toSpeedUpStr(speedUp2OBJ[2])))
    cmdList.append(getTexDataCommand('stwoobjMaxSpeedUpApp', '\\texttt{' + minmaxApps2OBJ[1] + '}'))

    cmdList.append(getTexDataCommand('zthreeobjMinSpeedUp', Util.toSpeedUpStr(speedUpz3OBJ[0])))
    cmdList.append(getTexDataCommand('zthreeobjMinSpeedUpApp', '\\texttt{' + minmaxAppsz3OBJ[0] + '}'))
    cmdList.append(getTexDataCommand('zthreeobjAvgSpeedUp', Util.toSpeedUpStr(speedUpz3OBJ[1])))
    cmdList.append(getTexDataCommand('zthreeobjAvgSpeedUpGM', Util.toSpeedUpStr(speedUpz3OBJGM)))
    cmdList.append(getTexDataCommand('zthreeobjMaxSpeedUp', Util.toSpeedUpStr(speedUpz3OBJ[2])))
    cmdList.append(getTexDataCommand('zthreeobjMaxSpeedUpApp', '\\texttt{' + minmaxAppsz3OBJ[1] + '}'))

    cmdList.append(getTexDataCommand('ethreeobjMinSpeedUp', Util.toSpeedUpStr(speedUpe3OBJ[0])))
    cmdList.append(getTexDataCommand('ethreeobjMinSpeedUpApp', '\\texttt{' + minmaxAppse3OBJ[0] + '}'))
    cmdList.append(getTexDataCommand('ethreeobjAvgSpeedUp', Util.toSpeedUpStr(speedUpe3OBJ[1])))
    cmdList.append(getTexDataCommand('ethreeobjAvgSpeedUpGM', Util.toSpeedUpStr(speedUpe3OBJGM)))
    cmdList.append(getTexDataCommand('ethreeobjMaxSpeedUp', Util.toSpeedUpStr(speedUpe3OBJ[2])))
    cmdList.append(getTexDataCommand('ethreeobjMaxSpeedUpApp', '\\texttt{' + minmaxAppse3OBJ[1] + '}'))

    cmdList.append(getTexDataCommand('sthreeobjMinSpeedUp', Util.toSpeedUpStr(speedUp3OBJ[0])))
    cmdList.append(getTexDataCommand('sthreeobjMinSpeedUpApp', '\\texttt{' + minmaxApps3OBJ[0] + '}'))
    cmdList.append(getTexDataCommand('sthreeobjAvgSpeedUp', Util.toSpeedUpStr(speedUp3OBJ[1])))
    cmdList.append(getTexDataCommand('sthreeobjAvgSpeedUpGM', Util.toSpeedUpStr(speedUp3OBJGM)))
    cmdList.append(getTexDataCommand('sthreeobjMaxSpeedUp', Util.toSpeedUpStr(speedUp3OBJ[2])))
    cmdList.append(getTexDataCommand('sthreeobjMaxSpeedUpApp', '\\texttt{' + minmaxApps3OBJ[1] + '}'))

    cmdList.append(getTexDataCommand('overallMaxSpeedUp', Util.toSpeedUpStr(overallMaxSpeedUp)))
    cmdList.append(getTexDataCommand('overallAvgSpeedUp', Util.toSpeedUpStr(overallAvgSpeedUp)))
    cmdList.append(getTexDataCommand('overallAvgGMSpeedUp', Util.toSpeedUpStr(overallAvgGMSpeedUp)))
    cmdList.append(getTexDataCommand('zipperAvgSpeedUp', Util.toSpeedUpStr(zipperAvgSpeedUp)))
    cmdList.append(getTexDataCommand('zipperAvgGMSpeedUp', Util.toSpeedUpStr(zipperAvgGMSpeedUp)))
    cmdList.append(getTexDataCommand('kobjAvgSpeedUp', Util.toSpeedUpStr(kobjAvgSpeedUp)))
    cmdList.append(getTexDataCommand('kobjAvgGMSpeedUp', Util.toSpeedUpStr(kobjAvgGMSpeedUp)))
    cmdList.append(getTexDataCommand('eagleAvgSpeedUp', Util.toSpeedUpStr(eagleAvgSpeedUp)))
    cmdList.append(getTexDataCommand('eagleAvgGMSpeedUp', Util.toSpeedUpStr(eagleAvgGMSpeedUp)))
    cmdList.append(getTexDataCommand('zipperOverEagleAvgSpeedUp', Util.toSpeedUpStr(zipperOverEagleAvgSpeedUp)))

    cmdList.append(getTexDataCommand('zipperAvgSpeedUpForAll', Util.toSpeedUpStr(zipperAvgSpeedUpForAll)))
    cmdList.append(getTexDataCommand('eagleAvgSpeedUpForAll', Util.toSpeedUpStr(eagleAvgSpeedUpForAll)))
    cmdList.append(getTexDataCommand('kobjAvgSpeedUpForAll', Util.toSpeedUpStr(kobjAvgSpeedUpForAll)))
    cmdList.append(getTexDataCommand('zipperOverEagleAvgSpeedUpForAll', Util.toSpeedUpStr(zipperOverEagleAvgSpeedUpForAll)))

    cmdList.append(getTexDataCommand('minCIRatio', toPercentageStr(ciratio[0])))
    cmdList.append(getTexDataCommand('avgCIRatio', toPercentageStr(ciratio[1])))
    cmdList.append(getTexDataCommand('maxCIRatio', toPercentageStr(ciratio[2])))
    cmdList.append(getTexDataCommand('minCIRatioApp', '\\texttt{' + minmaxCiRatioApp[0] + '}'))
    cmdList.append(getTexDataCommand('maxCIRatioApp', '\\texttt{' + minmaxCiRatioApp[1] + '}'))

    cmdList.append(getTexDataCommand('xalanthreevstwoSpeedup', Util.toSpeedUpStr(xalan3vs2D)))

    cmdList.append(getTexDataCommand('sparkAvgPreTime', '%.1f' % (avgSparkTime)))
    cmdList.append(getTexDataCommand('eagleAvgPreTime', '%.1f' % (avgEagleTime)))
    cmdList.append(getTexDataCommand('zipperAvgPreTime', '%.1f' % (avgZipperTime)))
    cmdList.append(getTexDataCommand('toolAvgPreTime', '%.1f' % (avgConchTime)))

    cmdList.append(getTexDataCommand('sparkAvgGMPreTime', '%.1f' % (avgSparkTimeGM)))
    cmdList.append(getTexDataCommand('eagleAvgGMPreTime', '%.1f' % (avgEagleTimeGM)))
    cmdList.append(getTexDataCommand('zipperAvgGMPreTime', '%.1f' % (avgZipperTimeGM)))
    cmdList.append(getTexDataCommand('toolAvgGMPreTime', '%.1f' % (avgConchTimeGM)))
    f = open(outputfile, "w")
    f.write('\n'.join(cmdList))
    f.close()
