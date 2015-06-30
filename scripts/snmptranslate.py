#!/usr/bin/env python
#
# Command-line MIB browser
#
# Copyright 1999-2015 by Ilya Etingof <ilya@glas.net>.
#
import sys, traceback
from pyasn1.type import univ
from pysnmp.entity import engine
from pysnmp.proto import rfc3412
from pysnmp.smi import builder
from pysnmp_apps.cli import main, pdu, mibview, base
from pysnmp.smi.error import NoSuchObjectError
from pysnmp import error
from pyasn1.type import univ

def getUsage():
    return "Usage: %s [OPTIONS] <PARAMETERS>\n\
%s%s\
TRANSLATE options:\n\
   -T TRANSOPTS   Set various options controlling report produced:\n\
              d:  print full details of the given OID\n\
              a:  dump the loaded MIB in a trivial form\n\
              l:  enable labeled OID report\n\
              o:  enable OID report\n\
              s:  enable dotted symbolic report\n\
%s\n" % (sys.argv[0],
         main.getUsage(),
         mibview.getUsage(),
         pdu.getReadUsage())

# Construct c/l interpreter for this app

class Scanner(mibview.MibViewScannerMixIn,
              pdu.ReadPduScannerMixIn,
              main.MainScannerMixIn,
              base.ScannerTemplate):
    def t_transopts(self, s):
        r' -T '
        self.rv.append(base.ConfigToken('transopts'))

class Parser(mibview.MibViewParserMixIn,
             pdu.ReadPduParserMixIn,
             main.MainParserMixIn,
             base.ParserTemplate):
    def p_transOptions(self, args):
        '''
        Cmdline ::= Options whitespace Params
        Cmdline ::= Options Params

        Option ::= TranslateOption

        TranslateOption ::= transopts whitespace string
        TranslateOption ::= transopts string

        '''

class __Generator(base.GeneratorTemplate):
    def n_TranslateOption(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibViewProxy = ctx['mibViewProxy']
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in opt:
            mibViewProxy.translateMassMode = 1            
            if c == 'd':
                mibViewProxy.translateFullDetails = 1
                mibViewProxy.translateMassMode = 0
            elif c == 'a':
                mibViewProxy.translateTrivial = 1
            elif c == 'l':
                mibViewProxy.translateLabeledOid = 1
            elif c == 'o':
                mibViewProxy.translateNumericOid = 1
            elif c == 's':
                mibViewProxy.translateSymbolicOid = 1
            else:
                raise error.PySnmpError('unsupported sub-option \"%s\"' % c)
            
def generator(cbCtx, ast):
    snmpEngine, ctx= cbCtx
    return __Generator().preorder((snmpEngine, ctx), ast)

class MibViewProxy(mibview.MibViewProxy):
    # MIB translate options
    translateFullDetails = 0
    translateTrivial = 0
    translateLabeledOid = 0
    translateNumericOid = 0
    translateSymbolicOid = 0

    # Implies SNMPWALK mode
    translateMassMode = 0
    
    # Override base class defaults
    buildEqualSign = 0

    _null = univ.Null()
    
    def getPrettyOidVal(self, mibViewController, oid, val):
        prefix, label, suffix = mibViewController.getNodeName(oid)
        modName, nodeDesc, _suffix = mibViewController.getNodeLocation(prefix)
        mibNode, = mibViewController.mibBuilder.importSymbols(
            modName, nodeDesc
        )        
        out = ''
        if self.translateFullDetails:
            if suffix:
                out = '%s::%s' % (modName, nodeDesc)
                out = out + ' [ %s ]' % '.'.join([ str(x) for x in suffix ])
                out = out + '\n'
            else:
                out = out + '%s::%s\n%s ::= { %s }' % (
                    modName,
                    nodeDesc,
                    mibNode.asn1Print(),
                    ' '.join(
                        map(lambda x,y: '%s(%s)' % (y, x), prefix, label)
                        )
                    )
        elif self.translateTrivial:
            out = '%s ::= { %s %s' % (
                len(label) > 1 and label[-2] or ".", label[-1], prefix[-1]
            )
            if suffix:
                out = out + ' [ %s ]' % '.'.join([ str(x) for x in suffix ])
            out = out + ' }'
        elif self.translateLabeledOid:
            out = '.' + '.'.join(
                map(lambda x,y: '%s(%s)' % (y, x),  prefix, label)
            )
            if suffix:
                out = out + ' [ %s ]' % '.'.join([ str(x) for x in suffix ])
        elif self.translateNumericOid:
            out = '.' + '.'.join([ str(x) for x in prefix ])
            if suffix:
                out = out + ' [ %s ]' % '.'.join([ str(x) for x in suffix ])
        elif self.translateSymbolicOid:
            out = '.' + '.'.join(label)
            if suffix:
                out = out + ' [ %s ]' % '.'.join([ str(x) for x in suffix ])
        if not out:
            out = mibview.MibViewProxy.getPrettyOidVal(
                self, mibViewController, oid, self._null
            )
        return out

snmpEngine = engine.SnmpEngine()

# Load up MIB texts (DESCRIPTION, etc.)
mibBuilder = snmpEngine.getMibBuilder()
mibBuilder.loadTexts = True

try:
    # Parse c/l into AST
    ast = Parser().parse(
        Scanner().tokenize(' '.join(sys.argv[1:]))
    )

    ctx = {}

    # Apply configuration to SNMP entity
    main.generator((snmpEngine, ctx), ast)
    ctx['mibViewProxy'] = MibViewProxy(ctx['mibViewController'])
    mibview.generator((snmpEngine, ctx), ast)
    pdu.readPduGenerator((snmpEngine, ctx), ast)
    generator((snmpEngine, ctx), ast)

except KeyboardInterrupt:
    sys.stderr.write('Shutting down...\n')

except error.PySnmpError:
    sys.stderr.write('Error: %s\n%s' % (sys.exc_info()[1], getUsage()))
    sys.exit(-1)

except Exception:
    sys.stderr.write('Process terminated: %s\n' % sys.exc_info()[1])
    for line in traceback.format_exception(*sys.exc_info()):
        sys.stderr.write(line.replace('\n', ';'))
    sys.exit(-1)

ctx['mibViewProxy'].buildValue = 0  # disable value printout

for oid, val in ctx['varBinds']:
    while 1:
        if val is None:
            val = univ.Null()
        sys.stdout.write('%s\n' % ctx['mibViewProxy'].getPrettyOidVal(
                ctx['mibViewController'], oid, val
            )
        )
        if not ctx['mibViewProxy'].translateMassMode:
            break
        try:
            oid, label, suffix = ctx['mibViewController'].getNextNodeName(oid)
        except NoSuchObjectError:
            break
