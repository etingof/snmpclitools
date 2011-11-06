# Abstract interface to SNMP objects initializers
import sys
from pysnmp_apps.cli import spark

# AST

class ConfigToken:
    # Abstract grammar token
    def __init__(self, type, attr=None):
        self.type = type
        self.attr = attr
    def __eq__(self, other): return self.type == other
    def __ne__(self, other): return self.type != other
    def __lt__(self, other): return self.type < other
    def __le__(self, other): return self.type <= other
    def __gt__(self, other): return self.type > other
    def __ge__(self, other): return self.type >= other
    def __repr__(self): return self.attr or self.type
    def __str__(self):
        if self.attr is None:
            return '%s' % self.type
        else:
            return '%s(%s)' % (self.type, self.attr)
    
class ConfigNode:
    # AST node class -- N-ary tree
    def __init__(self, type, attr=None):
        self.type, self.attr = type, attr
        self._kids = []
    def __getitem__(self, i):
        return self._kids[i]
    def __len__(self):
        return len(self._kids)
    if sys.version_info[0] < 3:
        def __setslice__(self, low, high, seq):
            self._kids[low:high] = seq
    else:
        def __setitem__(self, idx, seq):
            self._kids[idx] = seq
    def __eq__(self, other): return self.type == other
    def __ne__(self, other): return self.type != other
    def __lt__(self, other): return self.type < other
    def __le__(self, other): return self.type <= other
    def __gt__(self, other): return self.type > other
    def __ge__(self, other): return self.type >= other
    def __str__(self):
        if self.attr is None:
            return self.type
        else:
            return '%s(%s)' % (self.type, self.attr)

# Scanner

class __ScannerTemplate(spark.GenericScanner):
    def tokenize(self, input):
        self.rv = []
        spark.GenericScanner.tokenize(self, input)
        return self.rv

class __FirstLevelScanner(__ScannerTemplate):
    def t_string(self, s):
        r' [!#\$%&\'\(\)\*\+,\.//0-9<=>\?@A-Z\\\^_`a-z\{\|\}~][!#\$%&\'\(\)\*\+,\-\.//0-9<=>\?@A-Z\\\^_`a-z\{\|\}~]* '
        self.rv.append(ConfigToken('string', s))

class __SecondLevelScanner(__FirstLevelScanner):
    def t_semicolon(self, s):
        r' : '
        self.rv.append(ConfigToken('semicolon'))

    def t_lparen(self, s):
        r' \[ '
        self.rv.append(ConfigToken('lparen'))

    def t_rparen(self, s):
        r' \] '
        self.rv.append(ConfigToken('rparen'))

    def t_quote(self, s):
        r' \" '
        self.rv.append(ConfigToken('quote'))

    def t_whitespace(self, s):
        r' \s+ '
        self.rv.append(ConfigToken('whitespace'))

ScannerTemplate = __SecondLevelScanner

# Parser

class ParserTemplate(spark.GenericASTBuilder):
    initialSymbol = None
    def __init__(self, startSymbol=None):
        if startSymbol is None:
            startSymbol = self.initialSymbol
        spark.GenericASTBuilder.__init__(self, ConfigNode, startSymbol)

    def terminal(self, token):
        #  Reduce to homogeneous AST.
        return ConfigNode(token.type, token.attr)

# Generator

class GeneratorTemplate(spark.GenericASTTraversal):
    def __init__(self): pass  # Skip superclass constructor

    def typestring(self, node):
        return node.type

    def preorder(self, client, node):
        try:
            name = 'n_' + self.typestring(node)
            if hasattr(self, name):
                func = getattr(self, name)
                func(client, node)
            else:
                self.default(client, node)
        except spark.GenericASTTraversalPruningException:
            return client

        for kid in node:
            self.preorder(client, kid)

        name = name + '_exit'
        if hasattr(self, name):
            func = getattr(self, name)
            func(client, node)

        return client
    
    def default(self, client, node): pass
