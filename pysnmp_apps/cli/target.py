import string, socket
from pysnmp_apps.cli import base
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pysnmp_apps.error import SnmpApplicationError
from pysnmp.entity import config
from pysnmp import error

# Usage

def getUsage():
    return "\
Communication options\n\
   -r RETRIES        number of retries when sending request\n\
   -t TIMEOUT        request timeout (in seconds)\n\
Agent address:\n\
   [<transport-domain>:]<transport-endpoint>\n\
              transport-domain:    \"udp\"|\"udp6\"\n\
              transport-endpoint:  \"IP\"|\"IPv6\"|\"FQDN\"[:\"port\"]\n\
"

# Scanner

class TargetScannerMixIn:
    def t_retries(self, s):
        r' -r '
        self.rv.append(base.ConfigToken('retries'))

    def t_timeout(self, s):
        r' -t '
        self.rv.append(base.ConfigToken('timeout'))

    def t_transport(self, s):
        r' (udp6)|(udp) '
        self.rv.append(base.ConfigToken('transport', s))

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
        Agent ::= Transport semicolon Endpoint
        Agent ::= Endpoint semicolon Format
        Agent ::= Endpoint

        Transport ::= transport
        Endpoint ::= string
        Endpoint ::= lparen IPv6 rparen
        IPv6 ::= string IPv6
        IPv6 ::= semicolon IPv6
        IPv6 ::=
        Format ::= string
        '''
# Generator

if hasattr(socket, 'has_ipv6') and socket.has_ipv6 and \
       hasattr(socket, 'getaddrinfo'):
    _getaddrinfo = socket.getaddrinfo
else:
    def _getaddrinfo(a, b, c, d):
        raise SnmpApplicationError('IPv6 not supported by the system')

class __TargetGeneratorPassOne(base.GeneratorTemplate):
    defPort = '161'
    _snmpDomainMap = {
        'udp': (udp.snmpUDPDomain, udp.UdpSocketTransport, lambda h,p: (socket.gethostbyname(h), string.atoi(p))),
        'udp6': (udp6.snmpUDP6Domain, udp6.Udp6SocketTransport, lambda h,p: (_getaddrinfo(h,p,socket.AF_INET6, socket.SOCK_DGRAM)[0][4]))
        }
    _snmpDomainNameMap = {
        2: 'udp',
        10: 'udp6'
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

    def n_IPv6(self, (msgAndPduDsp, ctx), node):
        if not len(node):
            if not ctx.has_key('transportDomain'):
                ( ctx['transportDomain'],
                  ctx['transportModule'],
                  ctx['addrRewriteFun'] ) = self._snmpDomainMap['udp6']
            return
        if ctx.get('transportAddress') is None:
            ctx['transportAddress'] = ''
        if node[0] == 'semicolon':
            ctx['transportAddress'] = ctx['transportAddress'] + ':'
        else:
            ctx['transportAddress'] = ctx['transportAddress'] + node[0].attr

    def n_Format(self, (msgAndPduDsp, ctx), node):
        ctx['transportFormat'] = node[0].attr

    def n_Agent_exit(self, (msgAndPduDsp, ctx), node):
        if not ctx.has_key('transportDomain'):
            try:
                f = _getaddrinfo(ctx['transportAddress'], 0)[0][0]
            except:
                f = -1
            ( ctx['transportDomain'],
              ctx['transportModule'],
              ctx['addrRewriteFun'] ) = self._snmpDomainMap[
                self._snmpDomainNameMap.get(f, 'udp')
                ]
        if ctx.has_key('transportFormat'):
            ctx['transportAddress'] = (
                ctx['transportAddress'], ctx['transportFormat']
                )
            del ctx['transportFormat']
        else:
            ctx['transportAddress'] = ( ctx['transportAddress'], self.defPort)

class __TargetGeneratorTrapPassOne(__TargetGeneratorPassOne):
    defPort = '162'

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
                ctx['timeout'] = int(node[2].attr)*100
            else:
                ctx['timeout'] = int(node[1].attr)*100
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
            # net-snmp defaults
            ctx.get('timeout', 100),
            ctx.get('retryCount', 5),
            tagList=ctx['transportTag']
            )
        config.addSocketTransport(
            snmpEngine,
            ctx['transportDomain'],
            ctx['transportModule']().openClientMode()
            )

__TargetGeneratorTrapPassTwo = __TargetGeneratorPassTwo

def generator((snmpEngine, ctx), ast):
    __TargetGeneratorPassTwo().preorder(
        __TargetGeneratorPassOne().preorder((snmpEngine, ctx), ast), ast
        )

def generatorTrap((snmpEngine, ctx), ast):
    __TargetGeneratorTrapPassTwo().preorder(
        __TargetGeneratorTrapPassOne().preorder((snmpEngine, ctx), ast), ast
        )
