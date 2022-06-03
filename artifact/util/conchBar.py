#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import util.Util as Util


def drawCSCIRatioBar(ptaOutputs, outputfile, benchmarks):
    tool2ptaoutputs = Util.classifyByToolName(ptaOutputs)
    t2opoMap = Util.buildAppNameToObjMap(tool2ptaoutputs['Z-2o+D'])
    CS = []
    CI = []
    for app in benchmarks:
        CS.append(float(t2opoMap[app].conchCS))
        CI.append(float(t2opoMap[app].conchCI))

    conchCSs = []
    conchCIs = []
    # averageCI = 0.0
    for i in range(len(benchmarks)):
        ciRatio = CI[i] / (CI[i] + CS[i])
        csRatio = CS[i] / (CI[i] + CS[i])
        conchCIs.append(ciRatio)
        conchCSs.append(csRatio)
    #     averageCI += ciRatio
    # averageCI /= len(benchmarks)
    # averageCS = 1.0 - averageCI
    # conchCSs.append(averageCS)
    # conchCIs.append(averageCI)
    mBenchmarks = []
    mBenchmarks += benchmarks
    # mBenchmarks.append('avg.')
    N = len(mBenchmarks)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.5  # the width of the bars: can also be len(x) sequence

    plt.figure(figsize=(9, 4.2))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2)
    p1 = plt.bar(ind, conchCIs, width, color='gray')
    p2 = plt.bar(ind, conchCSs, width, bottom=conchCIs, color='silver')

    plt.xticks(ind, mBenchmarks, rotation="10", weight='bold')
    plt.yticks(np.arange(0, 1.1, 0.2), weight='bold')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.legend((p1[0], p2[0]), ('Context-Independent Objects', 'Context-Dependent Objects'), loc='upper center', ncol=4,
               bbox_to_anchor=(0.5, 1.16), prop={'weight': 'bold'})
    plt.savefig(outputfile)
    # plt.show()
