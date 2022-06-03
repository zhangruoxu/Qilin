#!/usr/bin/env python3

import util.Tex as Tex
import util.Util as Util


# input should be a map from app name to ptaoutputs
def buildAppNameToTimeList(name2outputs):
    app2times = {}
    for app in name2outputs:
        xkos = name2outputs[app]
        xkos2 = Util.buildAnalysisNameToObjMap(xkos)
        zipperTime = float(xkos2['Z-2o+D'].preAnalysisTime)
        eagleTime = float(xkos2['E-2o+D'].preAnalysisTime)
        conchTime = float(xkos2['Z-2o+D'].conchTime)
        sparkTime = float(xkos2['Z-2o+D'].sparkTime)
        app2times[app] = [round(sparkTime, 1), round(zipperTime, 1), round(conchTime, 1), round(eagleTime, 1)]
    return app2times


def buildToolNameToTimeByAppOrder(app2times, appOrderList, timeOrderList):
    ret = {}
    for i in range(len(timeOrderList)):
        tool = timeOrderList[i]
        mList = []
        for app in appOrderList:
            mTime = app2times[app][i]
            mList.append(mTime)
        ret[tool] = mList
    return ret


def avgSpeedUp(sparkPreTime, toolPreTime):
    lenList = len(sparkPreTime)
    f = 0.0
    for i in range(0, lenList):
        f = f + (toolPreTime[i] * 1.0) / (sparkPreTime[i] * 1.0)
    return f / lenList


# latex code for table head
def genTableHeadPart(benchmarks):
    headPart = [
        r"\begin{table}[tbp]",
        r"\centering",
        r"\caption{Times spent by \textsc{Spark} and pre-analyses in seconds.}",
        r"\label{table:pretime}",
        r"\scalebox{0.75}{",
        r"\begin{tabular}{@{} c ",
    ]

    ret = "\n".join(headPart)
    for _ in range(len(benchmarks) + 1):
        ret += " r "
    ret += "@{}}	\\toprule \n"
    ret += "\t  \t "
    for elem in benchmarks:
        ret += "& " + elem + " \t "
    # ret += "& Avg \t "
    ret += "\\\\ \\midrule\n"
    return ret


timeOrderList = ['spark', 'zipper', 'conch', 'eagle']


def genTable(tool2appstime, benchmarks):
    # classify by App name.
    texContent = genTableHeadPart(benchmarks)
    sparkPreTime = tool2appstime['spark']
    zipperPreTime = tool2appstime['zipper']
    conchPreTime = tool2appstime['conch']
    eaglePreTime = tool2appstime['eagle']
    texContent += '\\textsc{Spark}'
    for i in sparkPreTime:
        texContent += '&' + str(i)
    # texContent += '&' + "%.1f" % (sum(sparkPreTime) / len(sparkPreTime))
    texContent += '\\\\ \n'

    texContent += '\\rowcolor{lightgray} \\eagle'
    for i in eaglePreTime:
        texContent += '&' + str(i)
    # texContent += '&' + "%.1f" % (sum(zipperPreTime) / len(zipperPreTime))
    texContent += '\\\\ \n'

    texContent += '\\zipper'
    for i in zipperPreTime:
        texContent += '&' + str(i)
    # texContent += '&' + "%.1f" % (sum(zipperPreTime) / len(zipperPreTime))
    texContent += '\\\\ \n'
    texContent += '\\conch'
    for i in conchPreTime:
        texContent += '&' + str(i)
    # texContent += '&' + "%.1f" % (sum(conchPreTime) / len(conchPreTime))
    texContent += '\\\\ \\bottomrule\n'
    texContent += Tex.genTableTailPart()
    return texContent


def genPreTimeTable(allPtaOutputs, benchmarks, outputfile):
    ret = Util.classifyByAppName(allPtaOutputs)
    app2times = buildAppNameToTimeList(ret)
    tool2appstime = buildToolNameToTimeByAppOrder(app2times, benchmarks, timeOrderList)
    texContent = Tex.genDocHeadPart()
    texContent += genTable(tool2appstime, benchmarks)
    texContent += Tex.genDocTailPart()
    f = open(outputfile, "w")
    f.write(texContent)
    f.close()
