# C/L interface to MIB variables. Mimics Net-SNMP CLI.
from os import environ
from string import split, join
from pysnmp.asn1 import univ

__all__ = [ 'MibViewProxy' ]

class MibViewProxy:
    # Implements C/L interface to MIB objects I/O

    # Defaults
    defaultOidPrefix = (
        'iso', 'org', 'dod', 'internet', 'mgmt', 'mib-2', 'system'
        )
    defaultMibs = ('SNMPv2-MIB',)
    defaultMibDirs = ()

    # MIB parsing options
    # currently N/A
    
    # MIB output options
    buildModInfo = 1
    buildObjectDesc = 1
    buildNumericName = 0
    buildAbsoluteName = 0
    buildNumericIndices = 0
    buildEqualSign = 1
    buildTypeInfo = 1
    buildEscQuotes = 0
    buildRawVals = 0
    buildGuessedStringVals = 1
    buildValueOnly = 0
    buildUnits = 1
    
    # MIB input options
    parseAsRandomAccessMib = 1
    parseAsRegExp = 0
    parseAsRelativeOid = 1
    parseAndCheckIndices = 1
    parseAsDisplayHint = 1
    
    def __init__(self, mibViewController):
        self.mibViewController = mibViewController
        if environ.has_key('PYSNMPOIDPREFIX'):
            self.defaultOidPrefix = environ['PYSNMPOIDPREFIX']
        if environ.has_key('PYSNMPMIBS'):
            self.defaultMibs = split(environ['PYSNMPMIBS'], ':')
        if environ.has_key('PYSNMPMIBDIRS'):
            self.defaultMibDirs = split(environ['MIBDIRS'], ':')
        if self.defaultMibDirs:
            apply(self.mibViewController.mibBuilder.setMibPath,
                  (self.defaultMibDirs) + \
                  self.mibViewController.mibBuilder.getMibPath())
        if self.defaultMibs:
            apply(self.mibViewController.mibBuilder.loadModules, self.defaultMibs)
        self.__oidValue = univ.ObjectIdentifier()
            
    def getPrettyOidVal(self, (oid, val)):
        prefix, label, suffix = self.mibViewController.getNodeName(oid)
        modName, nodeDesc = self.mibViewController.getNodeLocation(prefix)
        out = ''
        # object name
        if not self.buildValueOnly:        
            if self.buildModInfo:
                out = '%s::' % modName
            if self.buildObjectDesc:
                out = out + nodeDesc
            else:
                if self.buildNumericName:
                    name = prefix
                else:
                    name = label
                if not self.buildAbsoluteName:
                    name = name[len(self.defaultOidPrefix):]
                out = out + join(map(lambda x: str(x), name), '.')
            
            if suffix:
                if suffix == (0,):
                    out = out + '.0'
                else:
                    rowNode, = apply(
                        self.mibViewController.mibBuilder.importSymbols,
                        self.mibViewController.getNodeLocation(prefix[:-1])
                        )
                    if self.buildNumericIndices:
                        out = out+'.'+join(map(lambda x: str(x), suffix), '.')
                    else:
                        try:
                            for i in rowNode.getIndicesFromInstId(suffix):
                                out = out + '.\'%s\'' % i
                        except AttributeError:
                            out = out + '.' + join(
                                map(lambda x: str(x), suffix), '.'
                                )
            if self.buildEqualSign:
                out = out + ' = '
            else:
                out = out + ' '
        # Value
        mibNode, = self.mibViewController.mibBuilder.importSymbols(
            modName, nodeDesc
            )
        if self.buildTypeInfo:
            out = out + '%s: ' % val.__class__.__name__
        try:
            syntax = mibNode.getSyntaxClone()
        except AttributeError:
            syntax = None
        if syntax is None or self.buildRawVals:
            out = out + str(val)
        else:
            try:
                out = out + syntax.prettyGet(val)
            except AttributeError:
                if self.__oidValue.isSubtype(val):
                    oid, label, suffix = self.mibViewController.getNodeName(
                        tuple(val)
                        )
                    out = out + join(label+tuple(
                        map(lambda x: str(x), suffix)), '.'
                                     )
                else:
                    try:
                        out = out + str(syntax.set(val))
                    except:  # XXX handle constraints violation
                        out = out + str(val)
            except:
                out = out + str(val)

            if self.buildUnits:
                try:
                    out = out + ' %s' % mibNode.getUnits()
                except:
                    pass
        return out
    
    def setPrettyOidValue(self, (oid, val, t)):
        return oid, val
    
if __name__ == '__main__':
    from pysnmp.smi import builder, view
    from pysnmp.asn1.univ import Integer

    p = MibViewProxy(view.MibViewController(builder.MibBuilder()))

    print p.getPrettyOidVal((1, 3, 6, 1, 2, 1, 1), Integer(1))
