#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import util.Util as Util


def drawVariantVsConchBar(ptaOutputs, outputfile, benchmarks):
    # step 1: app to app to a list of PTAOBJ.
    app2tool2ptaouts = Util.buildApp2Tool2PtaOutputMap(ptaOutputs)
    ratio = {}
    ratios = []
    for app in benchmarks:
        tool2ptaouts = app2tool2ptaouts[app]
        mratio = 0.0
        cnt = 0
        dp = tool2ptaouts['2o+D']
        ep = tool2ptaouts['2o+E']
        if dp.analysisCompleted() and ep.analysisCompleted():
            cnt += 1
            mratio += dp.analysisTime / ep.analysisTime

        dp = tool2ptaouts['3o+D']
        ep = tool2ptaouts['3o+E']
        if dp.analysisCompleted() and ep.analysisCompleted():
            cnt += 1
            mratio += dp.analysisTime / ep.analysisTime

        dp = tool2ptaouts['E-2o+D']
        ep = tool2ptaouts['E-2o+E']
        if dp.analysisCompleted() and ep.analysisCompleted():
            cnt += 1
            mratio += dp.analysisTime / ep.analysisTime

        dp = tool2ptaouts['E-3o+D']
        ep = tool2ptaouts['E-3o+E']
        if dp.analysisCompleted() and ep.analysisCompleted():
            cnt += 1
            mratio += dp.analysisTime / ep.analysisTime

        dp = tool2ptaouts['Z-2o+D']
        ep = tool2ptaouts['Z-2o+E']
        if dp.analysisCompleted() and ep.analysisCompleted():
            cnt += 1
            mratio += dp.analysisTime / ep.analysisTime

        dp = tool2ptaouts['Z-3o+D']
        ep = tool2ptaouts['Z-3o+E']
        if dp.analysisCompleted() and ep.analysisCompleted():
            cnt += 1
            mratio += dp.analysisTime / ep.analysisTime

        mratio /= cnt
        ratio[app] = mratio
        ratios.append(mratio)

    mBenchmarks = []
    mBenchmarks += benchmarks
    # mBenchmarks.append('avg.')
    N = len(mBenchmarks)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.5  # the width of the bars: can also be len(x) sequence

    plt.figure(figsize=(9, 4.2))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2)
    p1 = plt.bar(ind, ratios, width, color='silver')
    # p2 = plt.bar(ind, conchCSs, width, bottom=conchCIs, color='silver')

    plt.xticks(ind, mBenchmarks, rotation="10", weight='bold')
    plt.yticks(np.arange(0, 2.8, 0.5), weight='bold')
    plt.axhline(y=1.0, color='r', linestyle=':')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    # plt.legend((p1[0], p2[0]), ('Context-Independent Objects', 'Context-Dependent Objects'), loc='upper center', ncol=4,
    #            bbox_to_anchor=(0.5, 1.16), prop={'weight': 'bold'})
    plt.savefig(outputfile)
    plt.show()
