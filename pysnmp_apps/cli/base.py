# Abstract interface to SNMP objects initializers
from pysnmp_apps.cli.spark import GenericScanner, GenericASTBuilder, \
     GenericASTTraversal, GenericASTTraversalPruningException
from pysnmp_apps.cli.error import IncompleteDataError

__all__ = [ 'ConfigToken', 'ConfigNode', 'AbstractConfigScanner',
            'AbstractConfigParser', 'AbstractConfigGenerator' ]

class ConfigToken:
    # Abstract grammar token
    def __init__(self, type, attr=None):
        self.type = type
        self.attr = attr
    def __cmp__(self, o):
        return cmp(self.type, o)
    def __repr__(self):
        return self.attr or self.type
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
    def __setslice__(self, low, high, seq):
        self._kids[low:high] = seq
    def __cmp__(self, o):
        return cmp(self.type, o)
    def __str__(self):
        if self.attr is None:
            return self.type
        else:
            return '%s(%s)' % (self.type, self.attr)

class ScannerTemplate(GenericScanner):
    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv
    
class ParserTemplate(GenericASTBuilder):
    initialSymbol = None
    def __init__(self, startSymbol=None):
        if startSymbol is None:
            startSymbol = self.initialSymbol
        GenericASTBuilder.__init__(self, ConfigNode, startSymbol)

    def terminal(self, token):
        #  Reduce to homogeneous AST.
        return ConfigNode(token.type, token.attr)

    def nonterminal2(self, type, args):
        #  Flatten AST a bit by not making nodes if there's only
        #  one child.
        if len(args) == 1:
            return args[0]
        return GenericASTBuilder.nonterminal(self, type, args)
        
class GeneratorTemplate(GenericASTTraversal):
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
        except GenericASTTraversalPruningException:
            return client

        for kid in node:
            self.preorder(client, kid)

        name = name + '_exit'
        if hasattr(self, name):
            func = getattr(self, name)
            func(client, node)

        return client
    
    def default(self, client, node):
        pass
