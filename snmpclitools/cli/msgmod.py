#
# This file is part of snmpclitools software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpclitools/license.html
#
from pysnmp import error

from snmpclitools.cli import base


def getUsage():
    return """\
SNMP message processing options:
   -v VERSION            SNMP version (1|2c|3)
"""

# Scanner


class MPScannerMixIn(object):
    def t_version(self, s):
        """ -v """
        self.rv.append(base.ConfigToken('version'))

# Parser


class MPParserMixIn(object):
    def p_mpSpec(self, args):
        """
        Option ::= SnmpVersionId
        SnmpVersionId ::= version string
        SnmpVersionId ::= version whitespace string
        """

# Generator


class _MPGenerator(base.GeneratorTemplate):
    VERSION_ID_MAP = {
        '1':  0,
        '2':  1,
        '2c': 1,
        '3':  3
    }

    def n_SnmpVersionId(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            versionId = node[2].attr

        else:
            versionId = node[1].attr

        if versionId in self.VERSION_ID_MAP:
            ctx['versionId'] = self.VERSION_ID_MAP[versionId]

        else:
            raise error.PySnmpError('Bad version value %s' % versionId)


def generator(cbCtx, ast):
    snmpEngine, ctx = cbCtx
    _MPGenerator().preorder((snmpEngine, ctx), ast)
    # Commit defaults
    if 'versionId' not in ctx:
        ctx['versionId'] = 3
