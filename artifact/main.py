#!/usr/bin/env python3

import os, sys
from util.opt import *
from util.conchClient import genConchClientTable
from util.conchCSFacts import genConchCSTable
from util.conchPreTimeTable import genPreTimeTable
from util.conchBar import drawCSCIRatioBar
from util.avgctxTable import genAvgCtxTable
from util.paperUsedData import dumpDataCommandUsedInPaper
from util.variantBar import drawVariantVsConchBar
from util.variantTable import genVariantCITable
import util.Util as Util
import util.benchmark as bm

def invokePTA(analyses, benchmarks):
    cmdList = [sys.executable, 'run.py', '-out=' + PTA_OUTPUT]
    cmdList += benchmarks
    cmdList += analyses
    os.system(' '.join(cmdList))

def genConchClient(allPtaOutputs, benchmarks, clientFile):
    if XMODE == 'dynamic':
        checkAndRunRequiredAnalysis(allPtaOutputs, analysisList, benchmarks, False)
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    genConchClientTable(allPtaOutputs, os.path.join(SCRIPT_OUTPUT, clientFile), benchmarks)

def checkAndRunRequiredAnalysis(allPtaOutputs, analysisList, benchmarks, onlyBloat):
    app2PtaOuts = Util.classifyByAppName(allPtaOutputs)
    for app in benchmarks:
        if app not in app2PtaOuts:
            if onlyBloat == False:
                invokePTA(['-all'], [app])
            invokePTA(['-all', '-cd'], [app])
        else:
            anaName2PtaObj = Util.buildAnalysisNameToObjMap(app2PtaOuts[app])
            for ana in analysisList:
                if onlyBloat == False and ana not in anaName2PtaObj:
                    invokePTA([ana], [app])
                if (ana + '+D') not in anaName2PtaObj:
                    invokePTA([ana, '-cd'], [app])

def genCSFacts(allPtaOutputs, benchmarks, csFile):
    if XMODE == 'dynamic':
        checkAndRunRequiredAnalysis(allPtaOutputs, analysisList, benchmarks, False)
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    genConchCSTable(allPtaOutputs, benchmarks, os.path.join(SCRIPT_OUTPUT, csFile))

def generatePreTimeTable(allPtaOutputs, benchmarks, prefile):
    if XMODE == 'dynamic':
        checkAndRunRequiredAnalysis(allPtaOutputs, ['Z-2o', 'E-2o'], benchmarks, True)
        allPtaOutputs = Util.loadPtaOutputs(['Z-2o+D', 'E-2o+D'], benchmarks, PTA_OUTPUT)
    genPreTimeTable(allPtaOutputs, benchmarks, os.path.join(SCRIPT_OUTPUT, prefile))

def genCSCIRatioBar(allPtaOutputs, benchmarks, ratioFile):
    if XMODE == 'dynamic':
        checkAndRunRequiredAnalysis(allPtaOutputs, ['Z-2o', 'E-2o'], benchmarks, True)
        allPtaOutputs = Util.loadPtaOutputs(['Z-2o+D', 'E-2o+D'], benchmarks, PTA_OUTPUT)
    drawCSCIRatioBar(allPtaOutputs, os.path.join(SCRIPT_OUTPUT,ratioFile), benchmarks)

def generateAvgCtxTable(allPtaOutputs, benchmarks, ctxFile):
    if XMODE == 'dynamic':
        checkAndRunRequiredAnalysis(allPtaOutputs, analysisList, benchmarks, False)
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    genAvgCtxTable(allPtaOutputs, os.path.join(SCRIPT_OUTPUT, ctxFile), benchmarks)

def genDataCommandUsedInPaper(allPtaOutputs, cmdFile, verbose):
    if XMODE == 'dynamic':
        checkAndRunRequiredAnalysis(allPtaOutputs, analysisList, benchmarks, False)
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    dumpDataCommandUsedInPaper(allPtaOutputs, os.path.join(SCRIPT_OUTPUT, cmdFile), verbose)

def genVariantVsConchBar(allPtaOutputs, benchmarks, outfile):
    if XMODE == 'dynamic':
        invokePTA(['2o', '3o', 'E-2o', 'E-3o', 'Z-2o', 'Z-3o', '-cd'], benchmarks)
        invokePTA(['2o', '3o', 'E-2o', 'E-3o', 'Z-2o', 'Z-3o', '-ce'], benchmarks)
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    drawVariantVsConchBar(allPtaOutputs, os.path.join(SCRIPT_OUTPUT, outfile), benchmarks)

def generateVariantCITable(allPtaOutputs, benchmarks, outfile):
    if XMODE == 'dynamic':
        invokePTA(['2o', '-cd'], benchmarks)
        invokePTA(['2o', '-ce'], benchmarks)
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    genVariantCITable(allPtaOutputs, os.path.join(SCRIPT_OUTPUT, outfile), benchmarks)

# by default, we have three runs.
def mergePTAoutputs(runList):
    run1 = runList[0]
    app2tool2ptas1 = Util.buildApp2Tool2PtaOutputMap(run1)
    for i in range(1, len(runList)):
        runi = runList[i]
        app2tool2ptasi = Util.buildApp2Tool2PtaOutputMap(runi)
        app2tool2ptas1 = Util.mergeHelper(app2tool2ptas1, app2tool2ptasi)
    l = len(runList)
    ret = []
    for app in app2tool2ptas1:
        tool2ptas1 = app2tool2ptas1[app]
        for tool in tool2ptas1:
            pta1 = tool2ptas1[tool]
            if pta1.analysisCompleted():
                pta1.analysisTime = pta1.analysisTime / l
                pta1.sparkTime = float(pta1.sparkTime) / l
                pta1.preAnalysisTime = pta1.preAnalysisTime / l
                pta1.conchTime = pta1.conchTime / l
            ret.append(pta1)
            # pta1.dump()
    return ret

'''
Main function part.
'''

OPTIONMESSAGE = 'The valid OPTIONs are:\n' \
                + option('-help|-h', 'print this message.\n') \
                + option('-all', 'generate all tables, figures and data used in the paper.\n') \
                + option('-gclient|-tableII', 'generate client table for conch.\n') \
                + option('-gcsfact|-tableV', 'generate context-sensitive facts table for conch.\n') \
                + option('-gvariantbar', 'generate variant bar.\n') \
                + option('-gvarianttab', 'generate variant table.\n') \
                + option('-pretable|-tableIII', 'generate pre-time table for conch.\n') \
                + option('-dumpdata', 'dump all data used in paper in latex newcommand format.\n') \
                + option('-csciratio|-figure16', 'draw the CS/CI ratio bar for conch.\n') \
                + option('-avgctx|-tableIV', 'draw a scatter plot of average context in a method for conch.\n') \
                + option('-ptaout=<out>', 'specify PTA output path (default value: output).\n') \
                + option('-scriptout=<out>', 'specify output path for this script (default value: result).\n') \
                + option('-Xmode=<static|multi|dynamic>', 'specify script extracting mode (default value: dynamic).\n') \
                + option('<Benchmarks>', 'specify benchmark list.\n')

SCRIPT_OUTPUT = 'result'
PTA_OUTPUT = 'output'
GENMAINTB = False
GENCSFACTS = False
PRETABLE = False
PRE_TB_OUT = 'pretable.tex'
MAIN_TB_OUT = 'clientTable.tex'
CS_TB_OUT = 'CSFactsTable.tex'
DRAWBAR = False
CSCIBAR_OUT = 'csciConch.pdf'
GENAVGCTX = False
AVG_CTX_OUT = 'avgCtxConch.tex'
DRAWVARIANTBAR = False
VARIANT_BAR_OUT = "variant.pdf"
DRAWVARIANTTAB = False
VARIANT_TAB_OUT = "variantTable.tex"
DUMPCMD = False
XMODE = 'dynamic'


analysisList = ['2o', '3o', 'E-2o', 'E-3o', 'Z-2o', 'Z-3o']
# analysisListFull = ['2o', '2o+D', '3o', '3o+D', 'E-2o', 'E-2o+D', 'E-3o', 'E-3o+D', 'Z-2o', 'Z-2o+D', 'Z-3o', 'Z-3o+D']
analysisListFull = ['2o', '2o+D', '2o+E', '3o', '3o+D', '3o+E', 'E-2o', 'E-2o+D', 'E-2o+E', 'E-3o', 'E-3o+D', 'E-3o+E', 'Z-2o', 'Z-2o+D', 'Z-2o+E', 'Z-3o', 'Z-3o+D', 'Z-3o+E']

if __name__ == '__main__':
    if len(sys.argv) <= 1 or '-help' in sys.argv or '-h' in sys.argv:
        sys.exit(OPTIONMESSAGE)

    # This is only for convenience.
    # By default, we consider all 12 benchmarks.
    benchmarks = []
    for arg in sys.argv:
        if arg in bm.BENCHMARKS:
            benchmarks.append(arg)
        elif arg.startswith('-ptaout='):
            PTA_OUTPUT = arg[len('-ptaout='):]
        elif arg.startswith('-scriptout='):
            SCRIPT_OUTPUT = arg[len('-scriptout='):]
        elif arg.startswith('-Xmode='):
            XMODE = arg[len('-Xmode='):]
        elif arg.startswith('-gclient') or arg.startswith('-tableII'):
            GENMAINTB = True
        elif arg.startswith('-gcsfact') or arg.startswith('-tableV'):
            GENCSFACTS = True
        elif arg.startswith('-gvariantbar'):
            DRAWVARIANTBAR = True
        elif arg.startswith('-gvariantTab'):
            DRAWVARIANTTAB = True
        elif arg.startswith('-pretable') or arg.startswith('-tableIII'):
            PRETABLE = True
        elif arg.startswith('-csciratio') or arg.startswith('-figure16'):
            DRAWBAR = True
        elif arg.startswith('-avgctx') or arg.startswith('-tableIV'):
            GENAVGCTX = True
        elif arg.startswith('-dumpdata'):
            DUMPCMD = True
        elif arg.startswith('-all'):
            GENMAINTB = True
            GENCSFACTS = True
            PRETABLE = True
            DRAWBAR = True
            GENAVGCTX = True
            DUMPCMD = True
            DRAWVARIANTBAR = True
            DRAWVARIANTTAB = True


    if len(benchmarks) == 0:
        benchmarks = bm.BENCHMARKS

    # allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    if XMODE == 'static':
        allPtaOutputs = Util.loadPtaOutputs(analysisListFull, benchmarks, PTA_OUTPUT)
    elif XMODE == 'multi':
        run1 = Util.loadPtaOutputs(analysisListFull, benchmarks, os.path.join(PTA_OUTPUT, 'run1'))
        run2 = Util.loadPtaOutputs(analysisListFull, benchmarks, os.path.join(PTA_OUTPUT, 'run2'))
        run3 = Util.loadPtaOutputs(analysisListFull, benchmarks, os.path.join(PTA_OUTPUT, 'run3'))
        allPtaOutputs = mergePTAoutputs([run1, run2, run3])
    else:
        # XMODE == 'dynamic'
        allPtaOutputs = []

    try:
        if not os.path.isdir(SCRIPT_OUTPUT):
            if os.path.exists(SCRIPT_OUTPUT):
                raise IOError('FAIL_CREATE_SCRIPT_OUTPUT')
            else:
                os.makedirs(SCRIPT_OUTPUT)
    except 'FAIL_CREATE_SCRIPT_OUTPUT':
        print(
            tc.RED + 'ERROR: ' + tc.RESET + 'CANNOT CREATE OUTPUTDIR: ' + tc.YELLOW + SCRIPT_OUTPUT + tc.RESET + ' ALREADY EXISTS AS A FILE!')

    print('start generating ...')
    if GENMAINTB:
        genConchClient(allPtaOutputs, benchmarks, MAIN_TB_OUT)
    if GENCSFACTS:
        genCSFacts(allPtaOutputs, benchmarks, CS_TB_OUT)
    if PRETABLE:
        generatePreTimeTable(allPtaOutputs, benchmarks, PRE_TB_OUT)
    if DRAWBAR:
        genCSCIRatioBar(allPtaOutputs, benchmarks, CSCIBAR_OUT)
    if GENAVGCTX:
        generateAvgCtxTable(allPtaOutputs, benchmarks, AVG_CTX_OUT)
    if DRAWVARIANTBAR:
        genVariantVsConchBar(allPtaOutputs, benchmarks, VARIANT_BAR_OUT)
    if DRAWVARIANTTAB:
        generateVariantCITable(allPtaOutputs, benchmarks, VARIANT_TAB_OUT)
    if DUMPCMD:
        genDataCommandUsedInPaper(allPtaOutputs, "dataCommand.txt", True)
    print('finish!')
