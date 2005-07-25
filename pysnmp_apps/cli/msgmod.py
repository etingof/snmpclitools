from pysnmp_apps.cli import base
from pysnmp import error

# Usage

def getUsage():
    return "\
SNMP message processing options:\n\
   -v VERSION             SNMP version: \"1\"|\"2c\"|\"3\"\n\
"

# Scanner

class MPScannerMixIn:
    def t_version(self, s):
        r' -v '
        self.rv.append(base.ConfigToken('version'))

# Parser

class MPParserMixIn:
    def p_mpSpec(self, args):
        '''
        Option ::= SnmpVersionId
        SnmpVersionId ::= version string
        SnmpVersionId ::= version whitespace string
        '''

# Generator

class __MPGenerator(base.GeneratorTemplate):
    _versionIdMap = {
        '1':  0,
        '2':  1,
        '2c': 1,
        '3':  3
        }
    def n_SnmpVersionId(self, (snmpEngine, ctx), node):
        if len(node) > 2:
            versionId = node[2].attr
        else:
            versionId = node[1].attr
        if self._versionIdMap.has_key(versionId):
            ctx['versionId'] = self._versionIdMap[versionId]
        else:
            raise error.PySnmpError('Bad version value %s' % versionId)

def generator((snmpEngine, ctx), ast):
    __MPGenerator().preorder((snmpEngine, ctx), ast)
    # Commit defaults
    if not ctx.has_key('versionId'):
        ctx['versionId'] = 3
