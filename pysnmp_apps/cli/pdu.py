import string, types
from pyasn1.type import univ
from pyasn1.error import PyAsn1Error
from pysnmp.proto import rfc1902
from pysnmp import error
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
    def p_varBindSpec(self, args):
        '''
        VarBind ::= VarName
        VarType ::= string
        VarValue ::= string        
        '''
    
    def p_pduSpec(self, args):
        '''
        Params ::= VarBinds

        VarBinds ::= VarBind whitespace VarBinds
        VarBinds ::= VarBind
        VarBinds ::=
        VarName ::= ModName semicolon semicolon NodeName
        VarName ::= ModName semicolon semicolon
        VarName ::= semicolon semicolon NodeName
        VarName ::= NodeName
        ModName ::= string
        NodeName ::= ObjectName ObjectIndices
        ObjectName ::= string
        ObjectIndices ::= ObjectIndex string ObjectIndices
        ObjectIndices ::= ObjectIndex ObjectIndices
        ObjectIndices ::= ObjectIndex
        ObjectIndices ::=
        ObjectIndex ::= quote string quote        
        '''

# Generator

class __ReadPduGenerator(base.GeneratorTemplate):
    def n_ModName(self, (snmpEngine, ctx), node):
        ctx['modName'] = node[0].attr

    def n_ObjectName(self, (snmpEngine, ctx), node):
        objectName = []
        for subOid in string.split(node[0].attr, '.'):
            if not subOid:
                continue
            try:
                objectName.append(string.atol(subOid))
            except string.atoi_error:
                objectName.append(subOid)
        ctx['objectName'] = tuple(objectName)
        
    def n_ObjectIndex(self, (snmpEngine, ctx), node):
        if not ctx.has_key('objectIndices'):
            ctx['objectIndices'] = []
        ctx['objectIndices'].append(node[1].attr)

    def n_VarName_exit(self, (snmpEngine, ctx), node):
        mibViewCtl = ctx['mibViewController']
        if ctx.has_key('modName'):
            mibViewCtl.mibBuilder.loadModules(ctx['modName'])
        if ctx.has_key('objectName'):
            objectName = ctx['objectName']
        else:
            objectName = None

        modName = ctx.get('modName', '')            

        if objectName:
            oid, label, suffix = mibViewCtl.getNodeName(objectName, modName)
        else:
            oid, label, suffix = mibViewCtl.getFirstNodeName(modName)
        if filter(None, map(lambda x: type(x) not in
                            (types.LongType, types.IntType), suffix)):
            raise error.PySnmpError(
                'Cant resolve object at: %s' % (suffix,)
                )            
        modName, nodeDesc, _suffix = mibViewCtl.getNodeLocation(oid)
        mibNode, = mibViewCtl.mibBuilder.importSymbols(modName, nodeDesc)
        if not hasattr(self, '_MibTableColumn'):
            self._MibTableColumn, = mibViewCtl.mibBuilder.importSymbols(
                'SNMPv2-SMI', 'MibTableColumn'
                )
        if isinstance(mibNode, self._MibTableColumn):
            # Table column
            if ctx.has_key('objectIndices'):
                modName, nodeDesc, _suffix = mibViewCtl.getNodeLocation(
                    mibNode.name[:-1]
                    )
                mibNode, = mibViewCtl.mibBuilder.importSymbols(
                    modName, nodeDesc
                    )
                suffix = suffix + apply(
                    mibNode.getInstIdFromIndices, ctx['objectIndices']
                    )
        else:
            if ctx.has_key('objectIndices'):
                raise error.PySnmpError(
                    'Cant resolve indices: %s' % (ctx['objectIndices'],)
                    )
        ctx['varName'] = oid + suffix
        if ctx.has_key('objectName'):
            del ctx['objectName']
        if ctx.has_key('objectIndices'):
            del ctx['objectIndices']

    def n_VarBind_exit(self, (snmpEngine, ctx), node):
        if not ctx.has_key('varBinds'):
            ctx['varBinds'] = [ (ctx['varName'], None) ]
        else:
            ctx['varBinds'].append((ctx['varName'], None))
        del ctx['varName']
        
    def n_VarBinds_exit(self, (mibViewProxy, ctx), node):
        if not ctx.has_key('varBinds') or not ctx['varBinds']:
            ctx['varBinds'] = [ ((1, 3, 6), None) ]

def readPduGenerator((snmpEngine, ctx), ast):
    __ReadPduGenerator().preorder((snmpEngine, ctx), ast)

# Write class

def getWriteUsage():
    return "\
Management parameters:\n\
   <[\"mib-module\"::]\"object-name\"|\"oid\" \"type\"|\"=\" value> ...\n\
              mib-module:           MIB name (such as SNMPv2-MIB)\n\
              object-name:          MIB symbol (sysDescr.0) or OID\n\
              type:                 MIB value type\n\
                    i               integer\n\
                    u               unsigned integer\n\
                    s               string\n\
                    n               NULL\n\
                    o               ObjectIdentifier\n\
                    t               TimeTicks\n\
                    a               IP address\n\
              =:                    use MIB for value type lookup\n\
              value:                value to write\n\
"                  

# Scanner

WritePduScannerMixIn = ReadPduScannerMixIn

# Parser

class WritePduParserMixIn(ReadPduParserMixIn):
    def p_varBindSpec(self, args):
        '''
        VarBind ::= VarName whitespace VarType whitespace VarValue
        VarType ::= string
        VarValue ::= string        
        '''

# Generator

class __WritePduGenerator(__ReadPduGenerator):
    _typeMap = {
        'i': rfc1902.Integer(),
        'u': rfc1902.Integer32(),
        's': rfc1902.OctetString(),
        'n': univ.Null(),
        'o': univ.ObjectIdentifier(),
        't': rfc1902.TimeTicks(),
        'a': rfc1902.IpAddress()
        }

    def n_VarType(self, (snmpEngine, ctx), node):
        ctx['varType'] = node[0].attr

    def n_VarValue(self, (snmpEngine, ctx), node):
        ctx['varValue'] = node[0].attr

    def n_VarBind_exit(self, (snmpEngine, ctx), node):
        mibViewCtl = ctx['mibViewController']
        if ctx['varType'] == '=':
            modName, nodeDesc, suffix = mibViewCtl.getNodeLocation(ctx['varName'])
            mibNode, = mibViewCtl.mibBuilder.importSymbols(modName, nodeDesc)
            if hasattr(mibNode, 'syntax'):
                if suffix != (0,):
                    raise error.PySnmpError(
                        'Found MIB scalar %s but non-scalar given %s' %
                        (mibNode.name + (0,), ctx['varName'])
                        )
                else:
                    val = mibNode.syntax
            else:
                raise error.PySnmpError(
                    'Variable %s has no syntax' % (ctx['varName'],)
                    )
        else:
            val = self._typeMap[ctx['varType']]
        try:
            val = val.clone(ctx['varValue'])
        except PyAsn1Error, why:
            raise error.PySnmpError(why)
        
        if not ctx.has_key('varBinds'):
            ctx['varBinds'] = [ (ctx['varName'], val) ]
        else:
            ctx['varBinds'].append((ctx['varName'], val))

def writePduGenerator((snmpEngine, ctx), ast):
    __WritePduGenerator().preorder((snmpEngine, ctx), ast)
