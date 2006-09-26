import string, socket
from pysnmp_apps.cli import base
from pysnmp.entity import config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp import error

# Usage

def getUsage():
    return "\
Communication options\n\
   -r RETRIES        number of retries when sending request\n\
   -t TIMEOUT        request timeout (in seconds)\n\
Agent address:\n\
   [<transport-domain>:]<transport-endpoint>\n\
              transport-domain:    \"udp\"\n\
              transport-endpoint:  \"IP\"|\"FQDN\"[:\"port\"]\n\
"

# Scanner

class TargetScannerMixIn:
    def t_retries(self, s):
        r' -r '
        self.rv.append(base.ConfigToken('retries'))

    def t_timeout(self, s):
        r' -t '
        self.rv.append(base.ConfigToken('timeout'))
        
# Parser

class TargetParserMixIn:
    def p_targetSpec(self, args):
        '''
        Option ::= CommOption
        
        CommOption ::= Retries
        Retries ::= retries string
        Retries ::= retries whitespace string

        CommOption ::= Timeout
        Timeout ::= timeout string
        Timeout ::= timeout whitespace string

        Agent ::= Transport semicolon Endpoint semicolon Format
        Agent ::= Endpoint semicolon Format
        Agent ::= Endpoint

        Transport ::= string
        Endpoint ::= string
        Format ::= string        
        '''
# Generator

class __TargetGeneratorPassOne(base.GeneratorTemplate):
    _snmpDomainMap = {
        'udp': (udp.snmpUDPDomain, udp.UdpSocketTransport(),
                lambda h,p='161': (socket.gethostbyname(h), string.atoi(p)))
        }
    def n_Transport(self, (msgAndPduDsp, ctx), node):
        if self._snmpDomainMap.has_key(node[0].attr):
            ( ctx['transportDomain'],
              ctx['transportModule'],
              ctx['addrRewriteFun'] ) = self._snmpDomainMap[node[0].attr]
        else:
            raise error.PySnmpError(
                'Unsupported transport domain %s' % node[0].attr
                )
    def n_Endpoint(self, (msgAndPduDsp, ctx), node):
        ctx['transportAddress'] = node[0].attr

    def n_Format(self, (msgAndPduDsp, ctx), node):
        ctx['transportFormat'] = node[0].attr

    def n_Agent_exit(self, (msgAndPduDsp, ctx), node):
        if ctx.has_key('transportFormat'):
            ctx['transportAddress'] = (
                ctx['transportAddress'], ctx['transportFormat']
                )
            del ctx['transportFormat']
        else:
            ctx['transportAddress'] = ( ctx['transportAddress'], )
        if not ctx.has_key('transportDomain'):
            ( ctx['transportDomain'],
              ctx['transportModule'],
              ctx['addrRewriteFun'] ) = self._snmpDomainMap['udp']

class __TargetGeneratorPassTwo(base.GeneratorTemplate):
    def n_Retries(self, (snmpEngine, ctx), node):
        try:
            if len(node) > 2:
                ctx['retryCount'] = int(node[2].attr)
            else:
                ctx['retryCount'] = int(node[1].attr)
        except ValueError:
            raise error.PySnmpError('Bad retry value')

    def n_Timeout(self, (snmpEngine, ctx), node):
        try:
            if len(node) > 2:
                ctx['timeout'] = int(node[2].attr)*1000
            else:
                ctx['timeout'] = int(node[1].attr)*1000
        except:
            raise error.PySnmpError('Bad timeout value')

    def n_Agent_exit(self, (snmpEngine, ctx), node):
        ctx['addrName'] = '%s-name' % ctx['paramsName']
        ctx['transportTag'] = '%s-tag' % ctx['addrName']
        config.addTargetAddr(
            snmpEngine,
            ctx['addrName'],
            ctx['transportDomain'],
            apply(ctx['addrRewriteFun'], ctx['transportAddress']),
            ctx['paramsName'],
            ctx.get('timeout'),
            ctx.get('retryCount'),
            tagList=ctx['transportTag']
            )
        config.addSocketTransport(
            snmpEngine,
            ctx['transportDomain'],
            ctx['transportModule'].openClientMode()
            )
    
def generator((snmpEngine, ctx), ast):
    __TargetGeneratorPassTwo().preorder(
        __TargetGeneratorPassOne().preorder((snmpEngine, ctx), ast), ast
        )
