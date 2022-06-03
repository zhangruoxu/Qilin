#!/usr/bin/env python3

import util.Tex as Tex
import util.Util as Util

# latex code for table head
def genTableHeadPart(benchmarks):
    headPart = [
        r"\begin{table}[tbp]",
        r"\centering",
        r"\caption{Increased number (ratio) of Context-independent objects identified by $\tool^*$ over $\tool$.}",
        r"\label{table:varianttable}",
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


def genTable(app2increasedCI, app2incratio, benchmarks):
    # classify by App name.
    texContent = genTableHeadPart(benchmarks)
    texContent += '\#INC CI'
    for app in benchmarks:
        texContent += '&' + str(app2increasedCI[app])
    # texContent += '&' + "%.1f" % (sum(sparkPreTime) / len(sparkPreTime))
    texContent += '\\\\ \n'

    texContent += 'INC ratio'
    for app in benchmarks:
        texContent += '&' + '{:.2%}'.format(app2incratio[app]).replace('%', '\%')
    # texContent += '&' + "%.1f" % (sum(conchPreTime) / len(conchPreTime))
    texContent += '\\\\ \\bottomrule\n'
    texContent += Tex.genTableTailPart()
    return texContent


def genVariantCITable(allPtaOutputs, outputfile, benchmarks):
    app2tool2ptaouts = Util.buildApp2Tool2PtaOutputMap(allPtaOutputs)
    app2increasedCI = {}
    app2incratio = {}
    for app in benchmarks:
        tool2ptaouts = app2tool2ptaouts[app]
        dp = tool2ptaouts['2o+D']
        ep = tool2ptaouts['2o+E']
        app2increasedCI[app] = ep.conchCI - dp.conchCI
        app2incratio[app] = (app2increasedCI[app] * 1.0) / (dp.conchCI + dp.conchCS)
    texContent = Tex.genDocHeadPart()
    texContent += genTable(app2increasedCI, app2incratio, benchmarks)
    texContent += Tex.genDocTailPart()
    f = open(outputfile, "w")
    f.write(texContent)
    f.close()
