#!/usr/bin/env python3

BENCHMARKS = ['antlr', 'bloat', 'chart', 'eclipse', 'fop', 'luindex', 'lusearch', 'pmd', 'hsqldb', 'xalan', 'checkstyle', 'JPC',
              'findbugs']

BENCHMARKS2018 = ['avrora', 'batik', 'eclipse2018', 'fop2018', 'h2', 'jython', 'luindex2018', 'lusearch2018', 'pmd2018', 'sunflow', 'tomcat',
                  'tradebeans', 'tradesoap', 'xalan2018']

MAINCLASSES = {
    'antlr': 'dacapo.antlr.Main',
    'bloat': 'dacapo.bloat.Main',
    'chart': 'dacapo.chart.Main',
    'eclipse': 'dacapo.eclipse.Main',
    'fop': 'dacapo.fop.Main',
    'luindex': 'dacapo.luindex.Main',
    'lusearch': 'dacapo.lusearch.Main',
    'pmd': 'dacapo.pmd.Main',
    'hsqldb': 'dacapo.hsqldb.Main',
    'xalan': 'dacapo.xalan.Main',
    'checkstyle': 'com.puppycrawl.tools.checkstyle.Main',
    'findbugs': 'edu.umd.cs.findbugs.FindBugs',
    'JPC': 'org.jpc.j2se.JPCApplication',

    # dacapo 2018
    'avrora': 'Harness',
    'batik': 'Harness',
    'eclipse2018': 'Harness',
    'fop2018': 'Harness',
    'h2': 'Harness',
    'jython': 'Harness',
    'luindex2018': 'Harness',
    'lusearch2018': 'Harness',
    'pmd2018': 'Harness',
    'sunflow': 'Harness',
    'tomcat': 'Harness',
    'tradebeans': 'Harness',
    'tradesoap': 'Harness',
    'xalan2018': 'Harness',
}

APPPATH = {
    'antlr': 'benchmarks/dacapo2006/antlr.jar',
    'bloat': 'benchmarks/dacapo2006/bloat.jar',
    'chart': 'benchmarks/dacapo2006/chart.jar',
    'eclipse': 'benchmarks/dacapo2006/eclipse.jar',
    'fop': 'benchmarks/dacapo2006/fop.jar',
    'luindex': 'benchmarks/dacapo2006/luindex.jar',
    'lusearch': 'benchmarks/dacapo2006/lusearch.jar',
    'pmd': 'benchmarks/dacapo2006/pmd.jar',
    'hsqldb': 'benchmarks/dacapo2006/hsqldb.jar',
    'xalan': 'benchmarks/dacapo2006/xalan.jar',
    'checkstyle': 'benchmarks/applications/checkstyle/checkstyle-5.7-all.jar',
    'findbugs': 'benchmarks/applications/findbugs/findbugs.jar',
    'JPC': 'benchmarks/applications/JPC/JPCApplication.jar',
    # dacapo 2018
    'avrora': 'benchmarks/dacapo2018/avrora.jar',
    'batik': 'benchmarks/dacapo2018/batik.jar',
    'eclipse2018': 'benchmarks/dacapo2018/eclipse.jar',
    'fop2018': 'benchmarks/dacapo2018/fop.jar',
    'h2': 'benchmarks/dacapo2018/h2.jar',
    'jython': 'benchmarks/dacapo2018/jython.jar',
    'luindex2018': 'benchmarks/dacapo2018/luindex.jar',
    'lusearch2018': 'benchmarks/dacapo2018/lusearch.jar',
    'pmd2018': 'benchmarks/dacapo2018/pmd.jar',
    'sunflow': 'benchmarks/dacapo2018/sunflow.jar',
    'tomcat': 'benchmarks/dacapo2018/tomcat.jar',
    'tradebeans': 'benchmarks/dacapo2018/tradebeans.jar',
    'tradesoap': 'benchmarks/dacapo2018/tradesoap.jar',
    'xalan2018': 'benchmarks/dacapo2018/xalan.jar',
}

LIBPATH = {
    'antlr': 'benchmarks/dacapo2006/antlr-deps.jar',
    'bloat': 'benchmarks/dacapo2006/bloat-deps.jar',
    'chart': 'benchmarks/dacapo2006/chart-deps.jar',
    'eclipse': 'benchmarks/dacapo2006/eclipse-deps.jar',
    'fop': 'benchmarks/dacapo2006/fop-deps.jar',
    'luindex': 'benchmarks/dacapo2006/luindex-deps.jar',
    'lusearch': 'benchmarks/dacapo2006/lusearch-deps.jar',
    'pmd': 'benchmarks/dacapo2006/pmd-deps.jar',
    'hsqldb': 'benchmarks/dacapo2006/hsqldb-deps.jar',
    'xalan': 'benchmarks/dacapo2006/xalan-deps.jar',
    'checkstyle': 'benchmarks/applications/checkstyle/',
    'findbugs': 'benchmarks/applications/findbugs/',
    'JPC': 'benchmarks/applications/JPC/',

    # dacapo 2018
    'batik': 'benchmarks/dacapo2018/batik-deps',
    'fop2018': 'benchmarks/dacapo2018/fop-deps',
    'h2': 'benchmarks/dacapo2018/h2-deps',
    'jython': 'benchmarks/dacapo2018/jython-deps',
    'luindex2018': 'benchmarks/dacapo2018/luindex-deps',
    'lusearch2018': 'benchmarks/dacapo2018/lusearch-deps',
    'pmd2018': 'benchmarks/dacapo2018/pmd-deps',
    'sunflow': 'benchmarks/dacapo2018/sunflow-deps',
    'tomcat': 'benchmarks/dacapo2018/tomcat-deps',
    'tradebeans': 'benchmarks/dacapo2018/tradebeans-deps',
    'tradesoap': 'benchmarks/dacapo2018/tradesoap-deps',
    'xalan2018': 'benchmarks/dacapo2018/xalan-deps',
}

TAMIFLEXLOG = {
    'antlr': 'benchmarks/dacapo2006/antlr-refl.log',
    'bloat': 'benchmarks/dacapo2006/bloat-refl.log',
    'chart': 'benchmarks/dacapo2006/chart-refl.log',
    'eclipse': 'benchmarks/dacapo2006/eclipse-refl.log',
    'fop': 'benchmarks/dacapo2006/fop-refl.log',
    'luindex': 'benchmarks/dacapo2006/luindex-refl.log',
    'lusearch': 'benchmarks/dacapo2006/lusearch-refl.log',
    'pmd': 'benchmarks/dacapo2006/pmd-refl.log',
    'hsqldb': 'benchmarks/dacapo2006/hsqldb-refl.log',
    'xalan': 'benchmarks/dacapo2006/xalan-refl.log',
    'checkstyle': 'benchmarks/applications/checkstyle/checkstyle-refl.log',
    'findbugs': 'benchmarks/applications/findbugs/findbugs-refl.log',
    'JPC': 'benchmarks/applications/JPC/JPC-refl.log',

    # dacapo 2018
    'avrora': 'benchmarks/dacapo2018/avrora-refl.log',
    'batik': 'benchmarks/dacapo2018/batik-refl.log',
    'eclipse2018': 'benchmarks/dacapo2018/eclipse-refl.log',
    'fop2018': 'benchmarks/dacapo2018/fop-refl.log',
    'h2': 'benchmarks/dacapo2018/h2-refl.log',
    'jython': 'benchmarks/dacapo2018/jython-refl.log',
    'luindex2018': 'benchmarks/dacapo2018/luindex-refl.log',
    'lusearch2018': 'benchmarks/dacapo2018/lusearch-refl.log',
    'pmd2018': 'benchmarks/dacapo2018/pmd-refl.log',
    'sunflow': 'benchmarks/dacapo2018/sunflow-refl.log',
    'tomcat': 'benchmarks/dacapo2018/tomcat-refl.log',
    'tradebeans': 'benchmarks/dacapo2018/tradebeans-refl.log',
    'tradesoap': 'benchmarks/dacapo2018/tradesoap-refl.log',
    'xalan2018': 'benchmarks/dacapo2018/xalan-refl.log',
}

JREVERSION = {
    'antlr': 'jre1.6.0_45',
    'bloat': 'jre1.6.0_45',
    'chart': 'jre1.6.0_45',
    'eclipse': 'jre1.6.0_45',
    'fop': 'jre1.6.0_45',
    'luindex': 'jre1.6.0_45',
    'lusearch': 'jre1.6.0_45',
    'pmd': 'jre1.6.0_45',
    'hsqldb': 'jre1.6.0_45',
    'xalan': 'jre1.6.0_45',
    'checkstyle': 'jre1.6.0_45',
    'findbugs': 'jre1.6.0_45',
    'JPC': 'jre1.6.0_45',

    # dacapo 2018
    'avrora': 'jre1.8.0_312',
    'batik': 'jre1.8.0_312',
    'eclipse2018': 'jre1.8.0_312',
    'fop2018': 'jre1.8.0_312',
    'h2': 'jre1.8.0_312',
    'jython': 'jre1.8.0_312',
    'luindex2018': 'jre1.8.0_312',
    'lusearch2018': 'jre1.8.0_312',
    'pmd2018': 'jre1.8.0_312',
    'sunflow': 'jre1.8.0_312',
    'tomcat': 'jre1.8.0_312',
    'tradebeans': 'jre1.8.0_312',
    'tradesoap': 'jre1.8.0_312',
    'xalan2018': 'jre1.8.0_312',
}
