#!/usr/bin/env python3
import util.Tex as Tex
import util.Util as Util

def averageCtxOfEachApp(outList, benchmarks):
    app2out = Util.buildAppNameToObjMap(outList)
    ret = []
    for app in benchmarks:
        if app in app2out:
            ret.append(app2out[app].avgctx)
        else:
            print('WHY?' + app + ';;' )
            print(app2out['pmd'])
    return ret


# latex code for table head
def genTableHeadPart(benchmarks):
    headPart = [
        r"\begin{table}[tbp]",
        r"\centering",
        r"\caption{Average number of contexts analyzed for a method by \kobj, \conchobj{k}, \eagleobj{k}, \conchEobj{k}, \zipperobj{k} and \conchZobj{k}, where $k \in \{2,3\}$.}",
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

def specialFloatToString(val):
    if val < 0:
        return '-'
    else:
        return "%.1f" % val

def genAvgCtxTable(ptaOutputs, outputfile, benchmarks):
    tool2outs = Util.classifyByToolName(ptaOutputs)
    Z2objHD = averageCtxOfEachApp(tool2outs['Z-2o+D'], benchmarks)
    Z2objH = averageCtxOfEachApp(tool2outs['Z-2o'], benchmarks)
    E2objHD = averageCtxOfEachApp(tool2outs['E-2o+D'], benchmarks)
    E2objH = averageCtxOfEachApp(tool2outs['E-2o'], benchmarks)
    twoObjHD = averageCtxOfEachApp(tool2outs['2o+D'], benchmarks)
    twoObjH = averageCtxOfEachApp(tool2outs['2o'], benchmarks)
    Z3objHD = averageCtxOfEachApp(tool2outs['Z-3o+D'], benchmarks)
    Z3objH = averageCtxOfEachApp(tool2outs['Z-3o'], benchmarks)
    E3objHD = averageCtxOfEachApp(tool2outs['E-3o+D'], benchmarks)
    E3objH = averageCtxOfEachApp(tool2outs['E-3o'], benchmarks)
    threeObjHD = averageCtxOfEachApp(tool2outs['3o+D'], benchmarks)
    threeObjH = averageCtxOfEachApp(tool2outs['3o'], benchmarks)
    texContent = Tex.genDocHeadPart()
    texContent += genTableHeadPart(benchmarks)
    texContent += '\\textbf{2OBJ}'
    for i in twoObjH:
        texContent += '&' + specialFloatToString(i)
    # texContent += '&' + specialFloatToString(sum(twoObjH) / len(twoObjH))
    texContent += '\\\\ \n'
    texContent += '\\textbf{2OBJ+D}'
    for i in twoObjHD:
        texContent += '&' + specialFloatToString(i)
    # texContent += '&' + specialFloatToString(sum(twoObjHD) / len(twoObjHD))
    texContent += '\\\\ \\midrule\n'

    texContent += '\\rowcolor{lightgray}\\textbf{E2OBJ}'
    for i in E2objH:
        texContent += '&' + specialFloatToString(i)
    # texContent += '&' + specialFloatToString(sum(Z2objH) / len(Z2objH))
    texContent += '\\\\ \n'
    texContent += '\\rowcolor{lightgray}\\textbf{E2OBJ+D}'
    for i in E2objHD:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \\midrule\n'

    texContent += '\\textbf{Z2OBJ}'
    for i in Z2objH:
        texContent += '&' + specialFloatToString(i)
    # texContent += '&' + specialFloatToString(sum(Z2objH) / len(Z2objH))
    texContent += '\\\\ \n'
    texContent += '\\textbf{Z2OBJ+D}'
    for i in Z2objHD:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \\midrule\n'

    texContent += '\\textbf{3OBJ}'
    for i in threeObjH:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \n'
    texContent += '\\textbf{3OBJ+D}'
    for i in threeObjHD:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \\midrule\n'

    texContent += '\\rowcolor{lightgray}\\textbf{E3OBJ}'
    for i in E3objH:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \n'
    texContent += '\\rowcolor{lightgray}\\textbf{E3OBJ+D}'
    for i in E3objHD:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \\midrule\n'

    texContent += '\\textbf{Z3OBJ}'
    for i in Z3objH:
        texContent += '&' + specialFloatToString(i)
    texContent += '\\\\ \n'
    texContent += '\\textbf{Z3OBJ+D}'
    for i in Z3objHD:
        texContent += '&' + specialFloatToString(i)
    # texContent += '&' + specialFloatToString(sum(Z2objHD) / len(Z2objHD))
    texContent += '\\\\ \\bottomrule\n'


    texContent += Tex.genTableTailPart()
    texContent += Tex.genDocTailPart()
    f = open(outputfile, "w")
    f.write(texContent)
    f.close()


