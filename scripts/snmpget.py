#!/usr/bin/env python
#
# GET command generator
#
# Copyright 1999-2015 by Ilya Etingof <ilya@glas.net>.
#
import sys,traceback
from pysnmp_apps.cli import main, msgmod, secmod, target, pdu, mibview, base
from pysnmp.entity import engine
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp import error

def getUsage():
    return "Usage: %s [OPTIONS] <AGENT> <PARAMETERS>\n\
%s%s%s%s%s%s" % (sys.argv[0],
                 main.getUsage(),
                 msgmod.getUsage(),
                 secmod.getUsage(),
                 mibview.getUsage(),
                 target.getUsage(),
                 pdu.getReadUsage())

# Construct c/l interpreter for this app

class Scanner(msgmod.MPScannerMixIn,
              secmod.SMScannerMixIn,
              mibview.MibViewScannerMixIn,
              target.TargetScannerMixIn,
              pdu.ReadPduScannerMixIn,
              main.MainScannerMixIn,
              base.ScannerTemplate): pass

class Parser(msgmod.MPParserMixIn,
             secmod.SMParserMixIn,
             mibview.MibViewParserMixIn,
             target.TargetParserMixIn,
             pdu.ReadPduParserMixIn,
             main.MainParserMixIn,
             base.ParserTemplate): pass

def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        sys.stderr.write('%s\n' % errorIndication)
    elif errorStatus:
        sys.stderr.write(
            '%s at %s\n' %
            ( errorStatus.prettyPrint(),
              errorIndex and varBinds[int(errorIndex)-1] or '?' )
            )
    else:
        for oid, val in varBinds:
            sys.stdout.write('%s\n' % cbCtx['mibViewProxy'].getPrettyOidVal(
                    cbCtx['mibViewController'], oid, val
                )
            )

# Run SNMP engine

snmpEngine = engine.SnmpEngine()

try:
    # Parse c/l into AST
    ast = Parser().parse(
        Scanner().tokenize(' '.join(sys.argv[1:]))
    )

    ctx = {}

    # Apply configuration to SNMP entity
    main.generator((snmpEngine, ctx), ast)
    msgmod.generator((snmpEngine, ctx), ast)
    secmod.generator((snmpEngine, ctx), ast)    
    mibview.generator((snmpEngine, ctx), ast)
    target.generator((snmpEngine, ctx), ast)
    pdu.readPduGenerator((snmpEngine, ctx), ast)

    cmdgen.GetCommandGenerator().sendVarBinds(
        snmpEngine,
        ctx['addrName'],
        ctx.get('contextEngineId'), ctx.get('contextName', ''),
        ctx['varBinds'],
        cbFun, ctx
    )

    snmpEngine.transportDispatcher.runDispatcher()

except KeyboardInterrupt:
    sys.stderr.write('Shutting down...\n')

except error.PySnmpError:
    sys.stderr.write('Error: %s\n%s' % (sys.exc_info()[1], getUsage()))
    sys.exit(-1)

except Exception:
    sys.stderr.write('Process terminated\n')
    for line in traceback.format_exception(*sys.exc_info()):
        sys.stderr.write(line.replace('\n', ';'))
    sys.exit(-1)
