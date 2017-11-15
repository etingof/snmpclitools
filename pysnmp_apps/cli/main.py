#
# This file is part of pysnmp-apps software.
#
# Copyright (c) 2005-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pysnmp.sf.net/license.html
#
import sys
from pysnmp.smi import view
from pysnmp_apps.cli import base
from pysnmp import error
from pysnmp_apps import __version__ as pysnmpAppsVersion

try:
    from pysnmp import __version__ as pysnmpVersion
except ImportError:
    pysnmpVersion = 'N/A'

try:
    from pysmi import __version__ as pysmiVersion
except ImportError:
    pysmiVersion = 'N/A'

try:
    from pyasn1 import __version__ as pyasn1Version
except ImportError:
    pyasn1Version = 'N/A'

try:
    from pysnmp import debug
except ImportError:
    debug = None


def getUsage():
    return """\
Command-line SNMP tools version %s, written by Ilya Etingof <etingof@gmail.com>
Foundation libraries: pysmi %s, pysnmp %s, pyasn1 %s
Python interpreter: %s
Software documentation and support at http://snmplabs.com
   -h                    display this help message
   -V                    software release information
   -d                    dump raw packets
   -D category           enable debugging [%s]
""" % (pysnmpAppsVersion,
     pysmiVersion,
     pysnmpVersion,
     pyasn1Version,
     sys.version.replace('\n', ''),
     debug and ','.join(debug.flagMap.keys()) or "")


# Scanner

class MainScannerMixIn:
    def t_help(self, s):
        r' -h|--help '
        self.rv.append(base.ConfigToken('help'))

    def t_versioninfo(self, s):
        r' -V|--version '
        self.rv.append(base.ConfigToken('versioninfo'))

    def t_dump(self, s):
        r' -d '
        self.rv.append(base.ConfigToken('dump'))

    def t_debug(self, s):
        r' -D|--debug '
        self.rv.append(base.ConfigToken('debug'))

# Parser


class MainParserMixIn:
    initialSymbol = 'Cmdline'

    def error(self, token):
        raise error.PySnmpError(
            'Command-line parser error at token %s\n' % token
        )

    def p_cmdline(self, args):
        '''
        Cmdline ::= Options Agent whitespace Params
        '''

    def p_cmdlineExt(self, args):
        '''
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
        '''

# Generator


class __MainGenerator(base.GeneratorTemplate):
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
    return __MainGenerator().preorder((snmpEngine, ctx), ast)
