# C/L interface to MIB variables. Mimics Net-SNMP CLI.
import os
from pyasn1.type import univ
from pysnmp_apps.cli import base
from pysnmp.proto import rfc1902
from pysnmp import error

# Usage

def getUsage():
    return "\
MIB options:\n\
   -m MIB[:...]      load given list of MIBs (ALL loads everything)\n\
   -M DIR[:...]      look in given list of directories for MIBs\n\
   -O OUTOPTS        Toggle various defaults controlling output display:\n\
              q:  removes the equal sign and type information\n\
              Q:  removes the type information\n\
              f:  print full OIDs on output\n\
              s:  print only last symbolic element of OID\n\
              S:  print MIB module-id plus last element\n\
              u:  print OIDs using UCD-style prefix suppression\n\
              n:  print OIDs numerically\n\
              e:  print enums numerically\n\
              b:  do not break OID indexes down\n\
              E:  include a \" to escape the quotes in indices\n\
              X:  place square brackets around each index\n\
              T:  print value in hex\n\
              v:  print values only (not OID = value)\n\
              U:  don't print units\n\
              t:  output timeticks values as raw numbers\n\
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
    def n_MibFile(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        if node[0].attr.lower() == 'all':
            mibBuilder.loadModules()
        else:
            mibBuilder.loadModules(node[0].attr)
            
    def n_MibDir(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder
        mibBuilder.setMibPath(*(node[0].attr,) + mibBuilder.getMibPath())

    def n_OutputOption(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibViewProxy = ctx['mibViewProxy']
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in opt:
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
                raise error.PySnmpError('Option not implemented')
            elif c == 'b':
                mibViewProxy.buildNumericIndices = 1
            elif c == 'E':
                mibViewProxy.buildEscQuotes = 1
            elif c == 'X':
                mibViewProxy.buildSquareBrackets = 1
            elif c == 'T':
                mibViewProxy.buildHexVals = 1
            elif c == 'v':
                mibViewProxy.buildValueOnly = 1
            elif c == 'U':
                mibViewProxy.buildUnits = 0
            elif c == 't':
                mibViewProxy.buildRawTimeTicks = 1
                pass
            elif c == 'R':
                mibViewProxy.buildRawVals = 1
            else:
                raise error.PySnmpError(
                    'Unknown output option %s at %s' % (c, self)
                    )

    def n_InputOption(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibViewProxy = ctx['mibViewProxy']
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in opt:
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

def generator(cbCtx, ast):
    snmpEngine, ctx = cbCtx
    if 'mibViewProxy' not in ctx:
        ctx['mibViewProxy'] = MibViewProxy(ctx['mibViewController'])
    return __MibViewGenerator().preorder((snmpEngine, ctx), ast)

class UnknownSyntax:
    def prettyOut(self, val):
        return str(val)
unknownSyntax = UnknownSyntax()
    
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
    buildSquareBrackets = 0
    buildHexVals = 0
    buildRawVals = 0
    buildRawTimeTicks = 0
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
        if 'PYSNMPOIDPREFIX' in os.environ:
            self.defaultOidPrefix = os.environ['PYSNMPOIDPREFIX']
        if 'PYSNMPMIBS' in os.environ:
            self.defaultMibs = os.environ['PYSNMPMIBS'].split(':')
        if 'PYSNMPMIBDIRS' in os.environ:
            self.defaultMibDirs = os.environ['MIBDIRS'].split(':')
        if self.defaultMibDirs:
            mibViewController.mibBuilder.setMibPath(
                *(self.defaultMibDirs) + mibViewController.mibBuilder.getMibPath()
                )
        if self.defaultMibs:
            mibViewController.mibBuilder.loadModules(*self.defaultMibs)
        self.__oidValue = univ.ObjectIdentifier()
        self.__intValue = univ.Integer()
        self.__timeValue = rfc1902.TimeTicks()
        
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
                out = out + '.'.join([ str(x) for x in name ])
            
            if suffix:
                if suffix == (0,):
                    out = out + '.0'
                else:
                    m, n, s = mibViewController.getNodeLocation(prefix[:-1])
                    rowNode, = mibViewController.mibBuilder.importSymbols(
                        m, n
                        )
                    if self.buildNumericIndices:
                        out = out + '.' + '.'.join([ str(x) for x in suffix ])
                    else:
                        try:
                            for i in rowNode.getIndicesFromInstId(suffix):
                                if self.buildEscQuotes:
                                    out = out + '.\\\"%s\\\"' % i.prettyOut(i)
                                elif self.buildSquareBrackets:
                                    out = out + '.[%s]' % i.prettyOut(i)
                                else:
                                    out = out + '.\"%s\"' % i.prettyOut(i)
                        except AttributeError:
                            out = out + '.' + '.'.join(
                                [ str(x) for x in suffix ]
                                )
            if self.buildEqualSign:
                out = out + ' = '
            else:
                out = out + ' '

        # Value
        if isinstance(val, univ.Null):
            return out + val.prettyPrint()
        mibNode, = mibViewController.mibBuilder.importSymbols(
            modName, nodeDesc
            )
        if hasattr(mibNode, 'syntax'):
            syntax = mibNode.syntax
        else:
            syntax = val
        if syntax is None: # lame Agent may return a non-instance OID
            syntax = unknownSyntax
        if self.buildTypeInfo:
            out = out + '%s: ' % syntax.__class__.__name__
        if self.buildRawVals:
            out = out + str(val)
        elif self.buildHexVals: # XXX make it always in hex?
            if self.__intValue.isSuperTypeOf(val):
                out = out + '%x' % int(val)
            elif self.__oidValue.isSuperTypeOf(val):
                out = out + ' '.join([ '%x' % x for x in tuple(val) ])
            else:
                out = out + ' '.join([ '%.2x' % ord(x) for x in str(val) ])
        elif self.__timeValue.isSameTypeWith(val):
            if self.buildRawTimeTicks:
                out = out + str(int(val))
            else: # TimeTicks is not a TC
                val = int(val)
                d, m = divmod(val, 8640000)
                out = out + '%d days ' % d
                d, m = divmod(m, 360000)
                out = out + '%d:' % d
                d, m = divmod(m, 6000)
                out = out + '%d:' % d
                d, m = divmod(m, 100)
                out = out + '%d.%d' % (d, m)
        elif self.__oidValue.isSuperTypeOf(val):
            oid, label, suffix = mibViewController.getNodeName(val)
            out = out + '.'.join(
                label + tuple([ str(x) for x in suffix ])
                )
        else:
            out = out + syntax.prettyOut(val)

        if self.buildUnits:
            if hasattr(mibNode, 'getUnits'):
                out = out + ' %s' % mibNode.getUnits()
        return out
    
    def setPrettyOidValue(self, oid, val, t):
        return oid, val
