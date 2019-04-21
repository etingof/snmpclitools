#!/usr/bin/env python
#
# This file is part of snmpclitools software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpclitools/license.html
#
# Command-line MIB browser
#
import os
import sys
import traceback

from pyasn1.type import univ
from pysnmp import error
from pysnmp.entity import engine
from pysnmp.smi.error import NoSuchObjectError

from snmpclitools.cli import base
from snmpclitools.cli import main
from snmpclitools.cli import mibview
from snmpclitools.cli import pdu


def getUsage():
    return """\
Usage: %s [OPTIONS] <PARAMETERS>
%s%s
TRANSLATE options:
   -T TRANSOPTS   Set various options controlling report produced:
              d:  print full details of the given OID
              a:  dump the loaded MIB in a trivial form
              l:  enable labeled OID report
              o:  enable OID report
              s:  enable dotted symbolic report
%s\
""" % (os.path.basename(sys.argv[0]),
       main.getUsage(),
       mibview.getUsage(),
       pdu.getReadUsage())


# Construct c/l interpreter for this app

class Scanner(mibview.MibViewScannerMixIn,
              pdu.ReadPduScannerMixIn,
              main.MainScannerMixIn,
              base.ScannerTemplate):
    def t_transopts(self, s):
        """ -T """
        self.rv.append(base.ConfigToken('transopts'))


class Parser(mibview.MibViewParserMixIn,
             pdu.ReadPduParserMixIn,
             main.MainParserMixIn,
             base.ParserTemplate):
    def p_transOptions(self, args):
        """
        Cmdline ::= Options whitespace Params
        Cmdline ::= Options Params

        Option ::= TranslateOption

        TranslateOption ::= transopts whitespace string
        TranslateOption ::= transopts string

        """


class _Generator(base.GeneratorTemplate):
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
    snmpEngine, ctx = cbCtx
    return _Generator().preorder((snmpEngine, ctx), ast)


class MibViewProxy(mibview.MibViewProxy):
    # MIB translate options
    translateFullDetails = False
    translateTrivial = False
    translateLabeledOid = False
    translateNumericOid = False
    translateSymbolicOid = False

    # Implies SNMPWALK mode
    translateMassMode = False

    # Override base class defaults
    buildEqualSign = False

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
                out += ' [ %s ]' % '.'.join([str(x) for x in suffix])
                out += '\n'

            else:
                out += '%s::%s\n%s ::= { %s }' % (
                    modName,
                    nodeDesc,
                    mibNode.asn1Print(),
                    ' '.join(map(lambda x, y: '%s(%s)' % (y, x), prefix, label))
                )

        elif self.translateTrivial:
            out = '%s ::= { %s %s' % (
                len(label) > 1 and label[-2] or ".", label[-1], prefix[-1]
            )

            if suffix:
                out += ' [ %s ]' % '.'.join([str(x) for x in suffix])

            out += ' }'

        elif self.translateLabeledOid:
            out = '.' + '.'.join(
                map(lambda x, y: '%s(%s)' % (y, x), prefix, label)
            )

            if suffix:
                out += ' [ %s ]' % '.'.join([str(x) for x in suffix])

        elif self.translateNumericOid:
            out = '.' + '.'.join([str(x) for x in prefix])
            if suffix:
                out += ' [ %s ]' % '.'.join([str(x) for x in suffix])

        elif self.translateSymbolicOid:
            out = '.' + '.'.join(label)
            if suffix:
                out += ' [ %s ]' % '.'.join([str(x) for x in suffix])

        if not out:
            out = mibview.MibViewProxy.getPrettyOidVal(
                self, mibViewController, oid, self._null
            )

        return out


snmpEngine = engine.SnmpEngine()

# Load up MIB texts (DESCRIPTION, etc.)
mibBuilder = snmpEngine.getMibBuilder()
mibBuilder.loadTexts = True

ctx = {}

try:
    # Parse c/l into AST
    ast = Parser().parse(
        Scanner().tokenize(' '.join(sys.argv[1:]))
    )

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
    sys.exit(1)

except Exception:
    sys.stderr.write('Process terminated: %s\n' % sys.exc_info()[1])
    for line in traceback.format_exception(*sys.exc_info()):
        sys.stderr.write(line.replace('\n', ';'))
    sys.exit(1)

ctx['mibViewProxy'].buildValue = 0  # disable value printout

for oid, val in ctx['varBinds']:

    while True:
        if val is None:
            val = univ.Null()

        sys.stdout.write(
            '%s\n' % ctx['mibViewProxy'].getPrettyOidVal(
                ctx['mibViewController'], oid, val
            )
        )

        if not ctx['mibViewProxy'].translateMassMode:
            break

        try:
            oid, label, suffix = ctx['mibViewController'].getNextNodeName(oid)

        except NoSuchObjectError:
            break
