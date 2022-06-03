#!/usr/bin/env python3

import util.Tex as Tex
import util.Util as Util
from util.common import TOOLNAMEMAP

analysisList = ['2o', '2o+D', '3o', '3o+D', '', 'E-2o', 'E-2o+D', 'E-3o', 'E-3o+D', '', 'Z-2o', 'Z-2o+D', 'Z-3o', 'Z-3o+D']

# latex code for table head
def genTableHeadPart():
    headPart = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Context-sensitive facts (in millions). For all the metrics, smaller is better.}",
        r"\label{table:main}",
        r"\addtolength{\tabcolsep}{-1.0ex}",
        r"\scalebox{0.75}{",
        r"\begin{tabular}{@{}c l",
    ]

    ret = "\n".join(headPart)
    for i in range(len(analysisList) + 2):
        if i > len(analysisList) / 3 and i <= 2 * int(len(analysisList) / 3) :
            ret += "  >{\columncolor{lightgray}} r "
        else:
            ret += " r "
    ret += "@{}}	\\toprule \n"
    ret += r" 	  &  	 & \multicolumn{4}{c}{\textbf{Classic \kobj}} 	& & \multicolumn{4}{c}{\textbf{Eagle-guided \kobj}} & \multicolumn{4}{c}{\textbf{Zipper-guided \kobj}}	 \\ \cline{3-6} \cline{8-11} \cline{13-16}"
    ret += r"\textbf{Prog} & \textbf{Metrics}"
    for elem in analysisList:
        if elem == '':
            ret += r"&  "
        else:
            ret += r"& \textbf{" + TOOLNAMEMAP[elem] + r"}  "

    ret += "\\\\ \\midrule\n"
    return ret

def numberToFormatedString(num):
    if num < 0:
        return '-'
    elif num < 100000:
        f = (num * 1.0 / 1000.0)
        return '%.1fK' % f
    else:
        f = (num * 1.0 / 1000000.0)
        return '%.1fM' % f

# generate latex code for table body.
def genTableTexContentForOneApp(app, ptaOutputs):
    # ordered by analysis name
    anaName2Obj = Util.buildAnalysisNameToObjMap(ptaOutputs)
    edges = ['', '\#cs-calls']
    csgpts = ['', '\#cs-gpts']
    cslpts = ['', '\#cs-pts']
    csfpts = ['', '\#cs-fpts']
    sum = ['', 'Total']
    allAnaList = []
    allAnaList.extend(analysisList)
    for elem in allAnaList:
        if elem in anaName2Obj:
            ptaOutput = anaName2Obj[elem]
            edges.append(numberToFormatedString(ptaOutput.csCallEdges))
            csgpts.append(numberToFormatedString(ptaOutput.csGPts))
            cslpts.append(numberToFormatedString(ptaOutput.csLPts))
            csfpts.append(numberToFormatedString(ptaOutput.csFPts))
            sum.append(numberToFormatedString(ptaOutput.csGPts + ptaOutput.csCallEdges + ptaOutput.csLPts + ptaOutput.csFPts))
        elif elem == '':
            edges.append('')
            csgpts.append('')
            cslpts.append('')
            csfpts.append('')
            sum.append('')
        else:
            edges.append('-')
            csgpts.append('-')
            cslpts.append('-')
            csfpts.append('-')
            sum.append('-')

    ret = "\t &".join(csgpts) + "\\\\ \n"
    ret += "\t &".join(cslpts) + "\\\\ \n"
    ret += "\t &".join(csfpts) + "\\\\ \n"
    ret += "\t &".join(edges) + "\\\\ \n"
    ret += '\multirow{-4}{*}{' + app + '}' + "\t &".join(sum) + "\\\\ \\midrule\n"
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


def genConchCSTable(allPtaOutput, benchmarks, outputfile):
    texContent = Tex.genDocHeadPart()
    texContent += genTable(allPtaOutput, benchmarks)
    texContent += Tex.genDocTailPart()
    f = open(outputfile, "w")
    f.write(texContent)
    f.close()
