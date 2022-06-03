#!/usr/bin/env python3

import util.Tex as Tex
import util.Util as Util
from util.common import TOOLNAMEMAP

# analysisList = ['2o', '2o+D', '3o', '3o+D', '', 'E-2o', 'E-2o+D', 'E-3o', 'E-3o+D', '', 'Z-2o', 'Z-2o+D', 'Z-3o', 'Z-3o+D']
analysisList = ['2o', '2o+D', '2o+E', '3o', '3o+D', '3o+E', '', 'E-2o', 'E-2o+D', 'E-2o+E', 'E-3o', 'E-3o+D', 'E-3o+E', '', 'Z-2o', 'Z-2o+D', 'Z-2o+E', 'Z-3o', 'Z-3o+D', 'Z-3o+E']
# latex code for table head
def genTableHeadPart():
    headPart = [
        r"\begin{table}[hbtp]",
        r"\centering",
        r"\caption{Main analysis results. In all metrics, smaller is better. The analysis suffixed with ``+D'' means it uses context debloating techniques. \texttt{OoM} stands for ``Out of Memory''.}",
        r"\label{table:main}",
        r"\scalebox{0.75}{",
        r"\addtolength{\tabcolsep}{-1.0ex}",
        r"\begin{tabular}{@{}c l",
    ]

    ret = "\n".join(headPart)
    for i in range(len(analysisList) + 2):
        if i > len(analysisList) / 3 and i <= 2 * int(len(analysisList) / 3) :
            ret += "  >{\columncolor{lightgray}} r "
        else:
            ret += " r "
    ret += "@{}}	\\toprule \n"
    # ret += r" 	  &  	 & \multicolumn{4}{c}{\textbf{Classic \kobj}} 	& & \multicolumn{4}{c}{\textbf{Eagle-guided \kobj}} & \multicolumn{4}{c}{\textbf{Zipper-guided \kobj}}	 \\ \cline{3-6} \cline{8-11} \cline{13-16}"
    ret += r" 	  &  	 & \multicolumn{6}{c}{\textbf{Classic \kobj}} 	& & \multicolumn{6}{c}{\textbf{Eagle-guided \kobj}} & \multicolumn{6}{c}{\textbf{Zipper-guided \kobj}}	 \\ \cline{3-8} \cline{10-15} \cline{17-22}"
    ret += r"\textbf{Prog} & \textbf{Metrics}"
    for elem in analysisList:
        if elem == '':
            ret += r"&  "
        else:
            ret += r"& \textbf{" + TOOLNAMEMAP[elem] + r"}  "

    ret += "\\\\ \\midrule\n"
    return ret

TIMEOUT = {'bloat':['3o'],
           'eclipse':['2o'],
           'checkstyle':['3o']
           }

def getTimeStr(anaName2Obj, elem):
    ptaOutput = anaName2Obj[elem]
    speedupStr = ''
    # if elem in ['2o+D', '3o+D', 'Z-2o+D', 'Z-3o+D', 'E-2o+D', 'E-3o+D']:
    if elem in ['2o+D', '2o+E', '3o+D', '3o+E', 'Z-2o+D', 'Z-2o+E', 'Z-3o+D', 'Z-3o+E', 'E-2o+D', 'E-2o+E', 'E-3o+D', 'E-3o+E']:
        baseline = anaName2Obj[elem[:-2]]
        if baseline.analysisTime > 0:
            speedup = Util.computeSpeedUp(baseline, ptaOutput)
            speedupStr = '\\textcolor{blue}{ (\\textbf{' + Util.toSpeedUpStr(speedup) + '})}'
    if ptaOutput.analysisTime > 0:
        timeStr = '%.1f' % ptaOutput.analysisTime
        timeStr = timeStr + speedupStr
    elif ptaOutput.app in TIMEOUT and ptaOutput.analysisName in TIMEOUT[ptaOutput.app]:
        timeStr = '$>\\textbf{12h}$'
    else:
        timeStr = 'OoM'
    return timeStr

# generate latex code for table body.
def genTableTexContentForOneApp(app, ptaOutputs):
    # ordered by analysis name
    anaName2Obj = Util.buildAnalysisNameToObjMap(ptaOutputs)
    times = ['', 'Time (s)']
    casts = ['', '\#fail-cast']
    edges = ['', '\#call-edges']
    poly = ['', '\#poly-calls']
    # avgpts = ['', '\#avg-pts']
    reachs = ['', '\#reach-mtds']
    allAnaList = []
    allAnaList.extend(analysisList)
    for elem in allAnaList:
        if elem in anaName2Obj:
            ptaOutput = anaName2Obj[elem]
            timeStr = getTimeStr(anaName2Obj, elem)
            times.append(timeStr)
            casts.append(ptaOutput.mayFailCasts)
            edges.append(ptaOutput.callEdges)
            poly.append(ptaOutput.polyCalls)
            pts = ptaOutput.avgPointsToSize
            # avgpts.append(pts[:pts.find('.') + 9])
            reachs.append(ptaOutput.reachMethods)
        else:
            times.append('')
            casts.append('')
            edges.append('')
            poly.append('')
            # avgpts.append('')
            reachs.append('')

    ret = "\t &".join(times) + "\\\\ \n"
    ret += "\t &".join(casts) + "\\\\ \n"
    ret += "\t &".join(edges) + "\\\\ \n"
    ret += "\t &".join(poly) + "\\\\ \n"
    # ret += "\t &".join(reachs) + "\\\\ \n"
    ret += '\multirow{-6}{*}{' + app + '}' + "\t &".join(reachs)+ "\\\\ \\midrule\n"
    return ret


# input should be a list of PTAOutput instances.
def genTable(allPtaOutput, benchmarks):
    # classify by App name.
    texContent = genTableHeadPart()
    ret = Util.classifyByAppName(allPtaOutput)
    for app in benchmarks:
        if app not in ret:
            continue
        ptaOutputs = ret[app]
        texContent += genTableTexContentForOneApp(app, ptaOutputs)
    texContent = 'bottomrule'.join(texContent.rsplit('midrule', 1))
    texContent += Tex.genTableTailPart()
    return texContent


def genConchClientTable(allPtaOutput, outputfile, benchmarks):
    texContent = Tex.genDocHeadPart()
    texContent += genTable(allPtaOutput, benchmarks)
    texContent += Tex.genDocTailPart()
    f = open(outputfile, "w")
    f.write(texContent)
    f.close()
