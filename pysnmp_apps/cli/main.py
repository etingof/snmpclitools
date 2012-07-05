from pysnmp.smi import view
from pysnmp_apps.cli import base
from pysnmp import error
from pysnmp import __version__ as pysnmpVersion
from pysnmp_apps import __version__ as pysnmpAppsVersion
try:
    from pysnmp import debug
except ImportError:
    debug = None

# Usage

def getUsage():
    return "\
PySNMP apps version %s, library version %s ; http://pysnmp.sf.net\n\
   -h                    display this help message\n\
   -V                    software release information\n\
   -d                    dump raw packets\n\
   -D category           enable debugging [%s]\n\
" % (pysnmpAppsVersion, pysnmpVersion, debug and ','.join(debug.flagMap.keys()) or "")
    
# Scanner

class MainScannerMixIn:
    def t_help(self, s):
        r' -h '
        self.rv.append(base.ConfigToken('help'))

    def t_versioninfo(self, s):
        r' -V '
        self.rv.append(base.ConfigToken('versioninfo'))

    def t_dump(self, s):
        r' -d '
        self.rv.append(base.ConfigToken('dump'))

    def t_debug(self, s):
        r' -D '
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
        snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        )
    return __MainGenerator().preorder((snmpEngine, ctx), ast)
