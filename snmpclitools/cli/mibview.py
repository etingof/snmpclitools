#
# This file is part of snmpclitools software.
#
# Copyright (c) 2005-2018, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpclitools/license.html
#
# C/L interface to MIB variables. Mimics Net-SNMP CLI.
#
import os
from pyasn1.type import univ
from pyasn1.type import namedval
from snmpclitools.cli import base
from pysnmp.proto import rfc1902
from pysnmp.smi import builder, compiler
from pysnmp import error

defaultMibSourceUrl = 'http://mibs.snmplabs.com/asn1/@mib@'
defaultMibBorrowerUrl = 'http://mibs.snmplabs.com/pysnmp/fulltexts/@mib@'


def getUsage():
    return """\
MIB options:
   -m MIB[:...]   load given list of MIBs (ALL loads all compiled MIBs)
   -M DIR[:...]   look in given list of directories for MIBs
   -P MIBOPTS     Toggle various defaults controlling MIB parsing:
              XS: search for ASN.1 MIBs in remote directories specified
                  in URL form. The @mib@ token in the URL is substituted
                  with actual MIB to be downloaded. Default repository
                  address is %s
              XB: search for pysnmp MIBs in remote directories specified
                  in URL form. The @mib@ token in the URL is substituted
                  with actual MIB to be downloaded. Default repository
                  address is %s
   -O OUTOPTS     Toggle various defaults controlling output display:
              q:  removes the equal sign and type information
              Q:  removes the type information
              f:  print full OIDs on output
              s:  print only last symbolic element of OID
              S:  print MIB module-id plus last element
              u:  print OIDs using UCD-style prefix suppression
              n:  print OIDs numerically
              e:  print enums numerically
              b:  do not break OID indexes down
              E:  include a " to escape the quotes in indices
              X:  place square brackets around each index
              T:  print value in hex
              v:  print values only (not OID = value)
              U:  don't print units
              t:  output timeticks values as raw numbers
   -I INOPTS      Toggle various defaults controlling input parsing:
              h:  don't apply DISPLAY-HINTs
              u:  top-level OIDs must have '.' prefix (UCD-style)
""" % (defaultMibSourceUrl, defaultMibBorrowerUrl)

# Scanner


class MibViewScannerMixIn:
    def t_mibfiles(self, s):
        r' -m '
        self.rv.append(base.ConfigToken('mibfiles'))

    def t_mibdirs(self, s):
        r' -M '
        self.rv.append(base.ConfigToken('mibdirs'))

    def t_parseropts(self, s):
        r' -P '
        self.rv.append(base.ConfigToken('parseropts'))

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
        Option ::= ParserOption
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

        ParserOption ::= parseropts string
        ParserOption ::= parseropts whitespace string
        ParserOption ::= parseropts string whitespace Url
        ParserOption ::= parseropts whitespace string whitespace Url
        Url ::= string semicolon string

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
        mibBuilder = snmpEngine.getMibBuilder()
        if node[0].attr.lower() == 'all':
            mibBuilder.loadModules()
        else:
            mibBuilder.loadModules(node[0].attr)

    def n_MibDir(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if 'MibDir' not in ctx:
            ctx['MibDir'] = []
        ctx['MibDir'].append(node[0].attr)

    def n_Url(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['Url'] = node[0].attr + ':' + node[2].attr

    def n_ParserOption_exit(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        opt = node[1].attr or node[2].attr
        for c in opt:
            if c == 'XS':
                if 'MibDir' not in ctx:
                    ctx['MibDir'] = []
                if 'Url' not in ctx:
                    raise error.PySnmpError('Missing URL for option')
                ctx['MibDir'].append(ctx['Url'])
                del ctx['Url']
            elif c == 'XB':
                if 'MibBorrowers' not in ctx:
                    ctx['MibBorrowers'] = []
                if 'Url' not in ctx:
                    raise error.PySnmpError('Missing URL for option')
                ctx['MibBorrowers'].append(ctx['Url'])
                del ctx['Url']

    def n_OutputOption(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibViewProxy = ctx['mibViewProxy']
        opt = node[1].attr or node[2].attr
        for c in opt:
            if c == 'q':
                mibViewProxy.buildEqualSign = False
                mibViewProxy.buildTypeInfo = False
            elif c == 'Q':
                mibViewProxy.buildTypeInfo = False
            elif c == 'f':
                mibViewProxy.buildModInfo = False
                mibViewProxy.buildObjectDesc = False
                mibViewProxy.buildAbsoluteName = True
            elif c == 's':
                mibViewProxy.buildModInfo = False
                mibViewProxy.buildObjectDesc = True
            elif c == 'S':
                mibViewProxy.buildObjectDesc = True
            elif c == 'n':
                mibViewProxy.buildObjectDesc = False
                mibViewProxy.buildModInfo = False
                mibViewProxy.buildNumericName = True
                mibViewProxy.buildNumericIndices = True
                mibViewProxy.buildAbsoluteName = True
            elif c == 'e':
                mibViewProxy.buildEnums = False
            elif c == 'b':
                mibViewProxy.buildNumericIndices = True
            elif c == 'E':
                mibViewProxy.buildEscQuotes = True
            elif c == 'X':
                mibViewProxy.buildSquareBrackets = True
            elif c == 'T':
                mibViewProxy.buildHexVals = True
            elif c == 'v':
                mibViewProxy.buildObjectName = False
            elif c == 'U':
                mibViewProxy.buildUnits = False
            elif c == 't':
                mibViewProxy.buildRawTimeTicks = True
                pass
            elif c == 'R':
                mibViewProxy.buildRawVals = True
            else:
                raise error.PySnmpError(
                    'Unknown output option %s at %s' % (c, self)
                )

    def n_InputOption(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        mibViewProxy = ctx['mibViewProxy']
        opt = node[1].attr or node[2].attr
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

    compiler.addMibCompiler(snmpEngine.getMibBuilder())

    snmpEngine, ctx = __MibViewGenerator().preorder((snmpEngine, ctx), ast)

    if 'MibDir' not in ctx:
        ctx['MibDir'] = [defaultMibSourceUrl]
    if 'MibBorrowers' not in ctx:
        ctx['MibBorrowers'] = [defaultMibBorrowerUrl]

    compiler.addMibCompiler(snmpEngine.getMibBuilder(),
                            sources=ctx['MibDir'],
                            borrowers=ctx['MibBorrowers'])
    return snmpEngine, ctx


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
    buildObjectName = True
    buildValue = True
    buildModInfo = True
    buildObjectDesc = True
    buildNumericName = False
    buildAbsoluteName = False
    buildEnums = True
    buildNumericIndices = False
    buildEqualSign = True
    buildTypeInfo = True
    buildEscQuotes = False
    buildSquareBrackets = False
    buildHexVals = False
    buildRawVals = False
    buildRawTimeTicks = False
    buildGuessedStringVals = True
    buildUnits = True

    # MIB input options
    parseAsRandomAccessMib = True
    parseAsRegExp = False
    parseAsRelativeOid = True
    parseAndCheckIndices = True
    parseAsDisplayHint = True

    def __init__(self, mibViewController):
        if 'PYSNMPOIDPREFIX' in os.environ:
            self.defaultOidPrefix = os.environ['PYSNMPOIDPREFIX']
        if 'PYSNMPMIBS' in os.environ:
            self.defaultMibs = os.environ['PYSNMPMIBS'].split(':')
        if 'PYSNMPMIBDIRS' in os.environ:
            self.defaultMibDirs = os.environ['PYSNMPMIBDIRS'].split(':')
        if self.defaultMibDirs:
            mibViewController.mibBuilder.setMibSources(
                *(mibViewController.mibBuilder.getMibSources() +
                  tuple([builder.ZipMibSource(m).init() for m in self.defaultMibDirs]))
            )
        if self.defaultMibs:
            mibViewController.mibBuilder.loadModules(*self.defaultMibs)
        self.__oidValue = univ.ObjectIdentifier()
        self.__intValue = univ.Integer()
        self.__timeValue = rfc1902.TimeTicks()
        self.__bitsValue = rfc1902.Bits()

    def getPrettyOidVal(self, mibViewController, oid, val):
        prefix, label, suffix = mibViewController.getNodeName(oid)
        modName, nodeDesc, _suffix = mibViewController.getNodeLocation(prefix)
        out = ''
        # object name
        if self.buildObjectName:
            if self.buildModInfo:
                out = '%s::' % modName
            if self.buildObjectDesc:
                out += nodeDesc
            else:
                if self.buildNumericName:
                    name = prefix
                else:
                    name = label
                if not self.buildAbsoluteName:
                    name = name[len(self.defaultOidPrefix):]
                out += '.'.join([str(x) for x in name])

            if suffix:
                if suffix == (0,):
                    out += '.0'
                else:
                    m, n, s = mibViewController.getNodeLocation(prefix[:-1])
                    rowNode, = mibViewController.mibBuilder.importSymbols(
                        m, n
                    )
                    if self.buildNumericIndices:
                        out += '.' + '.'.join([str(x) for x in suffix])
                    else:
                        try:
                            for i in rowNode.getIndicesFromInstId(suffix):
                                if self.buildEscQuotes:
                                    out += '.\\\"%s\\\"' % i.prettyOut(i)
                                elif self.buildSquareBrackets:
                                    out += '.[%s]' % i.prettyOut(i)
                                else:
                                    out += '.\"%s\"' % i.prettyOut(i)
                        except Exception:
                            out += '.' + '.'.join(
                                [str(x) for x in suffix]
                            )

        if self.buildObjectName and self.buildValue:
            if self.buildEqualSign:
                out += ' = '
            else:
                out += ' '

        # Value
        if self.buildValue:
            if isinstance(val, univ.Null):
                return out + val.prettyPrint()
            mibNode, = mibViewController.mibBuilder.importSymbols(
                modName, nodeDesc
            )
            if hasattr(mibNode, 'syntax'):
                syntax = mibNode.syntax
            else:
                syntax = val
            if syntax is None:  # lame Agent may return a non-instance OID
                syntax = unknownSyntax
            if self.buildTypeInfo:
                out += '%s: ' % syntax.__class__.__name__
            if self.buildRawVals:
                out += str(val)
            elif self.buildHexVals:  # XXX make it always in hex?
                if self.__intValue.isSuperTypeOf(val):
                    out += '%x' % int(val)
                elif self.__timeValue.isSameTypeWith(val):
                    out += '%x' % int(val)
                elif self.__oidValue.isSuperTypeOf(val):
                    out += ' '.join(['%x' % x for x in tuple(val)])
                else:
                    out += ' '.join(['%.2x' % x for x in val.asNumbers()])
            elif self.__timeValue.isSameTypeWith(val):
                if self.buildRawTimeTicks:
                    out += str(int(val))
                else:  # TimeTicks is not a TC
                    val = int(val)
                    d, m = divmod(val, 8640000)
                    out += '%d days ' % d
                    d, m = divmod(m, 360000)
                    out += '%d:' % d
                    d, m = divmod(m, 6000)
                    out += '%d:' % d
                    d, m = divmod(m, 100)
                    out += '%d.%d' % (d, m)
            elif self.__oidValue.isSuperTypeOf(val):
                oid, label, suffix = mibViewController.getNodeName(val)
                out += '.'.join(
                    label + tuple([str(x) for x in suffix])
                )
            elif (not self.buildEnums and
                      (self.__intValue.isSuperTypeOf(val) or
                       self.__bitsValue.isSuperTypeOf(val))):
                out += syntax.clone(val, namedValues=namedval.NamedValues()).prettyPrint()
            else:
                out += syntax.clone(val).prettyPrint()

            if self.buildUnits:
                if hasattr(mibNode, 'getUnits'):
                    out += ' %s' % mibNode.getUnits()

        return out

    def setPrettyOidValue(self, oid, val, t):
        return oid, val
