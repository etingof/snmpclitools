#
# This file is part of snmpclitools software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpclitools/license.html
#
import sys

from pysnmp import error
from pysnmp.smi import view

try:
    from pysnmp import __version__ as PYSNMP_VERSION

except ImportError:
    PYSNMP_VERSION = 'N/A'

try:
    from pysmi import __version__ as PYSMI_VERSION

except ImportError:
    PYSMI_VERSION = 'N/A'

try:
    from pyasn1 import __version__ as PYASN1_VERSION

except ImportError:
    PYASN1_VERSION = 'N/A'

try:
    from pysnmp import debug

except ImportError:
    debug = None

from snmpclitools import __version__ as PYSNMP_APP_VERSION
from snmpclitools.cli import base


def getUsage():
    return """\
SNMP management tools %s, written by Ilya Etingof <etingof@gmail.com>
Software documentation and support at http://snmplabs.com
Foundation libraries: pysmi %s, pysnmp %s, pyasn1 %s
Python interpreter: %s
Debugging options:
   -h                    display this help message
   -V                    software release information
   -d                    dump raw packets
   -D category           enable debugging [%s]
""" % (PYSNMP_APP_VERSION,
       PYSMI_VERSION,
       PYSNMP_VERSION,
       PYASN1_VERSION,
       sys.version.replace('\n', ''),
       debug and ','.join(debug.flagMap.keys()) or "")


# Scanner

class MainScannerMixIn(object):
    def t_help(self, s):
        """ -h|--help """
        self.rv.append(base.ConfigToken('help'))

    def t_versioninfo(self, s):
        """ -V|--version """
        self.rv.append(base.ConfigToken('versioninfo'))

    def t_dump(self, s):
        """ -d """
        self.rv.append(base.ConfigToken('dump'))

    def t_debug(self, s):
        """ -D|--debug """
        self.rv.append(base.ConfigToken('debug'))


# Parser

class MainParserMixIn(object):
    START_SYMBOL = 'Cmdline'

    def error(self, token):
        raise error.PySnmpError(
            'Command-line parser error at token %s\n' % token
        )

    def p_cmdline(self, args):
        """
        Cmdline ::= Options Agent whitespace Params
        """

    def p_cmdlineExt(self, args):
        """
        Options ::= Option whitespace Options
        Options ::= Option
        Options ::=

        Option ::= Help
        Option ::= VersionInfo
        Option ::= DebugOption

        Help ::= help

        VersionInfo ::= versioninfo

        DebugOption ::= Dump
        DebugOption ::= Debug
        Dump ::= dump
        Debug ::= debug string
        Debug ::= debug whitespace string
        """


# Generator

class _MainGenerator(base.GeneratorTemplate):
    # SNMPv1/v2
    def n_VersionInfo(self, cbCtx, node):
        raise error.PySnmpError()

    def n_Help(self, cbCtx, node):
        raise error.PySnmpError()

    def n_Dump(self, cbCtx, node):
        if debug:
            debug.setLogger(debug.Debug('io'))

    def n_Debug(self, cbCtx, node):
        if debug:
            if len(node) > 2:
                f = node[2].attr
            else:
                f = node[1].attr
            debug.setLogger(debug.Debug(*f.split(',')))


def generator(cbCtx, ast):
    snmpEngine, ctx = cbCtx

    ctx['mibViewController'] = view.MibViewController(
        snmpEngine.getMibBuilder()
    )

    return _MainGenerator().preorder((snmpEngine, ctx), ast)
