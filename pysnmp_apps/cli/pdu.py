import string
from pysnmp_apps.cli import base

# Read class

# Usage

def getReadUsage():
    return "\
Management parameters:\n\
   [\"mib-module\"::]\"object-name\"|\"oid\" ...\n\
              mib-module:           MIB name (such as SNMPv2-MIB)\n\
              object-name:          MIB symbol (sysDescr.0) or OID\n\
"

# Scanner

class ReadPduScannerMixIn: pass

# Parser

class ReadPduParserMixIn:
    def p_readPduSpec(self, args):
        '''
        Params ::= VarBinds

        VarBinds ::= VarBind whitespace VarBinds
        VarBinds ::= VarBind
        VarBinds ::=
        VarBind ::= ModName semicolon semicolon NodeName
        VarBind ::= ModName semicolon semicolon
        VarBind ::= semicolon semicolon NodeName
        VarBind ::= NodeName
        ModName ::= string
        NodeName ::= string
        '''

# Generator

class __ReadPduGenerator(base.GeneratorTemplate):
    def n_ModName(self, (snmpEngine, ctx), node):
        ctx['modName'] = node[0].attr

    def n_NodeName(self, (snmpEngine, ctx), node):
        ctx['nodeName'] = node[0].attr

    def n_VarBind_exit(self, (snmpEngine, ctx), node):
        mibViewCtl = ctx['mibViewController']
        if ctx.has_key('modName'):
            mibViewCtl.mibBuilder.loadModules(ctx['modName'])
        nodeName = []
        if ctx.has_key('nodeName'):
            for subOid in string.split(ctx['nodeName'], '.'):
                if not subOid:
                    continue
                try:
                    nodeName.append(string.atol(subOid))
                except string.atoi_error:
                    nodeName.append(subOid)
        nodeName = tuple(nodeName)

        modName = ctx.get('modName', '')            

        oid, label, suffix = mibViewCtl.getNodeName(nodeName, modName)

        if not ctx.has_key('varBinds'):
            ctx['varBinds'] = [ (oid + suffix, None) ]
        else:
            ctx['varBinds'].append((oid + suffix, None))
                
    def n_VarBinds_exit(self, (mibViewProxy, ctx), node):
        if not ctx.has_key('varBinds') or not ctx['varBinds']:
            ctx['varBinds'] = [ ((1, 3, 6), None) ]

def readPduGenerator((snmpEngine, ctx), ast):
    __ReadPduGenerator().preorder((snmpEngine, ctx), ast)

# Write class

# Scanner

WritePduScannerMixIn = ReadPduScannerMixIn

# Parser

class WritePduParserMixIn(ReadPduParserMixIn):
    def p_writePduSpec(self, args):
        '''
        NodeName ::= VarBind
        VarBind ::= Oid equal Val
        VarBind ::= Oid string Val
        '''

# Generator

class __WritePduGenerator(__ReadPduGenerator):
    def n_NodeName(self, node): pass
    def n_VarBind(self, node):
        # XXX
        mibViewCtl = ctx['mibViewController']
        if ctx.has_key('modName'):
            mibViewCtl.mibBuilder.loadModules(ctx['modName'])
        nodeName = []
        if ctx.has_key('nodeName'):
            for subOid in string.split(ctx['nodeName'], '.'):
                if not subOid:
                    continue
                try:
                    nodeName.append(string.atol(subOid))
                except string.atoi_error:
                    nodeName.append(subOid)
        nodeName = tuple(nodeName)

        modName = ctx.get('modName', '')            

        oid, label, suffix = mibViewCtl.getNodeName(nodeName, modName)

        if node[1].attr == '=':
            val = None # XXX mib resolve
        else:
            val = self._typeMap[node[1].attr].clone(node[2].attr)

        if not ctx.has_key('varBinds'):
            ctx['varBinds'] = [ (oid + suffix, val) ]
        else:
            ctx['varBinds'].append((oid + suffix, val))

def writePduGenerator((snmpEngine, ctx), ast):
    __WritePduGenerator().preorder((snmpEngine, ctx), ast)
