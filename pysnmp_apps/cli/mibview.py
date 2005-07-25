# C/L interface to MIB variables. Mimics Net-SNMP CLI.
import os, string
from pyasn1.type import univ
from pysnmp_apps.cli import base
from pysnmp import error

# Usage

def getUsage():
    return "\
MIB options:\n\
   -m MIB[:...]      load given list of MIBs (ALL loads everything)\n\
   -M DIR[:...]      look in given list of directories for MIBs\n\
   -O OUTOPTS        Toggle various defaults controlling output display:\n\
              b:  do not break OID indexes down\n\
              e:  print enums numerically\n\
              f:  print full OIDs on output\n\
              n:  print OIDs numerically\n\
              s:  print only last symbolic element of OID\n\
              S:  print MIB module-id plus last element\n\
              u:  print OIDs using UCD-style prefix suppression\n\
              U:  don't print units\n\
              v:  print values only (not OID = value)\n\
   -I INOPTS         Toggle various defaults controlling input parsing:\n\
              h:  don't apply DISPLAY-HINTs\n\
              u:  top-level OIDs must have '.' prefix (UCD-style)\n\
"

# Scanner

class MibViewScannerMixIn:
    def t_mibfiles(self, s):
        r' -m '
        self.rv.append(base.ConfigToken('mibfiles'))

    def t_mibdirs(self, s):
        r' -M '
        self.rv.append(base.ConfigToken('mibdirs'))

    def t_outputopts(self, s):
        r' -O '
        self.rv.append(base.ConfigToken('outputopts'))

    def t_inputopts(self, s):
        r' -I '
        self.rv.append(base.ConfigToken('inputopts'))

# Parser

class MibViewParserMixIn:
    def p_mibView(self, args):
        '''
        Option ::= GeneralOption
        Option ::= OutputOption
        Option ::= InputOption

        GeneralOption ::= MibDirList
        MibDirList ::= mibdirs MibDirs
        MibDirList ::= mibdirs whitespace MibDirs
        MibDirs ::= MibDir semicolon MibDirs
        MibDirs ::= MibDir
        MibDir ::= string
        GeneralOption ::= MibFileList
        MibFileList ::= mibfiles MibFiles
        MibFileList ::= mibfiles whitespace MibFiles
        MibFiles ::= MibFile semicolon MibFiles
        MibFiles ::= MibFile
        MibFile ::= string

        OutputOption ::= outputopts string
        OutputOption ::= outputopts whitespace string

        InputOption ::= inputopts string
        InputOption ::= inputopts whitespace string
        '''

# Generator

class __MibViewGenerator(base.GeneratorTemplate):
    # Load MIB modules
    def n_MibFile(self, (snmpEngine, ctx), node):
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        if lower(node[0].attr) == 'all':
            mibBuilder.loadModules()
        else:
            mibBuilder.loadModules(node[0].attr)
            
    def n_MibDir(self, (mibViewProxy, ctx), node):
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        apply(mibBuilder.setMibPath, (node[0].attr,) + mibBuilder.getMibPath())

    def n_OutputOption(self, (snmpEngine, ctx), node):
        mibViewProxy = ctx['mibViewProxy']
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in map(None, opt):
            if c == 'q':
                mibViewProxy.buildEqualSign = 0
                mibViewProxy.buildTypeInfo = 0
            elif c == 'Q':
                mibViewProxy.buildTypeInfo = 0
            elif c == 'f':
                mibViewProxy.buildModInfo = 0
                mibViewProxy.buildObjectDesc = 0
                mibViewProxy.buildAbsoluteName = 1
            elif c == 's':
                mibViewProxy.buildModInfo = 0
                mibViewProxy.buildObjectDesc = 1
            elif c == 'S':
                mibViewProxy.buildObjectDesc = 1
            elif c == 'u':
                pass
            elif c == 'n':
                mibViewProxy.buildObjectDesc = 0
                mibViewProxy.buildModInfo = 0
                mibViewProxy.buildNumericName = 1
                mibViewProxy.buildNumericIndices = 1
                mibViewProxy.buildAbsoluteName = 1
            elif c == 'e':
                pass
            elif c == 'b':
                mibViewProxy.buildNumericIndices = 1
            elif c == 'E':
                pass
            elif c == 'X':
                pass
            elif c == 'a':
                pass
            elif c == 'x':
                pass
            elif c == 'T':
                pass
            elif c == 'v':
                mibViewProxy.buildValueOnly = 1
            elif c == 'U':
                mibViewProxy.buildUnits = 0
            elif c == 't':
                pass
            elif c == 'R':
                mibViewProxy.buildRawVals = 1
            else:
                raise error.PySnmpError(
                    'Unknown output option %s at %s' % (c, self)
                    )

    def n_InputOption(self, (snmpEngine, ctx), node):
        mibViewProxy = ctx['mibViewProxy']
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in map(None, opt):
            if c == 'R':
                pass
            elif c == 'b':
                pass
            elif c == 'u':
                mibViewProxy.defaultOidPrefix = (
                    'iso', 'org', 'dod', 'internet', 'mgmt', 'mib-2'
                    )
            elif c == 'r':
                pass
            elif c == 'h':
                pass
            else:
                raise error.PySnmpError(
                    'Unknown input option %s at %s' % (c, self)
                    )

def generator((snmpEngine, ctx), ast):
    ctx['mibViewProxy'] = MibViewProxy(ctx['mibViewController'])
    return __MibViewGenerator().preorder((snmpEngine, ctx), ast)

#  Proxy MIB view

class MibViewProxy:
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
        if os.environ.has_key('PYSNMPOIDPREFIX'):
            self.defaultOidPrefix = os.environ['PYSNMPOIDPREFIX']
        if os.environ.has_key('PYSNMPMIBS'):
            self.defaultMibs = string.split(os.environ['PYSNMPMIBS'], ':')
        if os.environ.has_key('PYSNMPMIBDIRS'):
            self.defaultMibDirs = string.split(os.environ['MIBDIRS'], ':')
        if self.defaultMibDirs:
            apply(mibViewController.mibBuilder.setMibPath,
                  (self.defaultMibDirs) + \
                  mibViewController.mibBuilder.getMibPath())
        if self.defaultMibs:
            apply(mibViewController.mibBuilder.loadModules,
                  self.defaultMibs)
        self.__oidValue = univ.ObjectIdentifier()
            
    def getPrettyOidVal(self, mibViewController, oid, val):
        prefix, label, suffix = mibViewController.getNodeName(oid)
        modName, nodeDesc, _suffix = mibViewController.getNodeLocation(prefix)
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
                out = out + string.join(map(lambda x: str(x), name), '.')
            
            if suffix:
                if suffix == (0,):
                    out = out + '.0'
                else:
                    rowNode, = apply(
                        mibViewController.mibBuilder.importSymbols,
                        mibViewController.getNodeLocation(prefix[:-1])
                        )
                    if self.buildNumericIndices:
                        out = out+'.'+string.join(
                            map(lambda x: str(x), suffix), '.'
                            )
                    else:
                        try:
                            for i in rowNode.getIndicesFromInstId(suffix):
                                out = out + '.\'%s\'' % i
                        except AttributeError:
                            out = out + '.' + string.join(
                                map(lambda x: str(x), suffix), '.'
                                )
            if self.buildEqualSign:
                out = out + ' = '
            else:
                out = out + ' '
        # Value
        mibNode, = mibViewController.mibBuilder.importSymbols(
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
                if self.__oidValue.isSuperTypeOf(val):
                    oid, label, suffix = mibViewController.getNodeName(val)
                    out = out + string.join(
                        label+tuple(map(lambda x: str(x), suffix)), '.'
                        )
                else:
                    try:
                        out = out + str(syntax.clone(val))
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
