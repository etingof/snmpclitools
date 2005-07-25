from pysnmp.smi import view
from pysnmp_apps.cli import base
from pysnmp import error, majorVersionId

# Usage

def getUsage():
    return "\
PySNMP library version %s; http://pysnmp.sf.net\n\
   -h                    display this help message\n\
   -V                    software release information\n\
" % majorVersionId
    
# Scanner

class MainScannerMixIn:
    def t_help(self, s):
        r' -h '
        self.rv.append(base.ConfigToken('help'))

    def t_versioninfo(self, s):
        r' -V '
        self.rv.append(base.ConfigToken('versioninfo'))

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

        Options ::= Option whitespace Options
        Options ::= Option
        Options ::=

        Option ::= Help
        Option ::= VersionInfo

        Help ::= help

        VersionInfo ::= versioninfo
        '''
# Generator

class __MainGenerator(base.GeneratorTemplate):
    # SNMPv1/v2
    def n_VersionInfo(self, (snmpEngine, ctx), node):
        raise error.PySnmpError()

    def n_Help(self, (snmpEngine, ctx), node):
        raise error.PySnmpError()

def generator((snmpEngine, ctx), ast):
    ctx['mibViewController'] = view.MibViewController(
        snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        )
    return __MainGenerator().preorder((snmpEngine, ctx), ast)
