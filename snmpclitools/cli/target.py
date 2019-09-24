#
# This file is part of snmpclitools software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpclitools/license.html
#
import socket

from pysnmp import error
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.carrier.asynsock.dgram import udp6
from pysnmp.entity import config

from snmpclitools.cli import base
from snmpclitools.error import SnmpApplicationError


def getUsage():
    return """\
General communication options
   -r RETRIES        number of retries when sending request
   -t TIMEOUT        request timeout (in seconds)
Agent address:
   [<transport-domain>:]<transport-endpoint|[transport-endpoint]>
              transport-domain:    (udp|udp6)
              transport-endpoint:  (IP|IPv6|FQDN[:port])

   Note: IPv6 address should be surrounded by square brackets
   to be parsed correctly e.g. udp6:[::1]161

"""


# Scanner

class TargetScannerMixIn(object):
    def t_retries(self, s):
        """ -r """
        self.rv.append(base.ConfigToken('retries'))

    def t_timeout(self, s):
        """ -t """
        self.rv.append(base.ConfigToken('timeout'))

    def t_transport(self, s):
        """ (udp6)|(udp) """
        self.rv.append(base.ConfigToken('transport', s))


# Parser

class TargetParserMixIn(object):
    def p_targetSpec(self, args):
        """
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
        """


# Generator

if (hasattr(socket, 'has_ipv6') and socket.has_ipv6 and
        hasattr(socket, 'getaddrinfo')):
    _getaddrinfo = socket.getaddrinfo

else:
    def _getaddrinfo(a, b, c, d):
        raise SnmpApplicationError('IPv6 not supported by the system')


class _TargetGeneratorPassOne(base.GeneratorTemplate):
    DEFAULT_PORT = '161'
    SNMP_DOMAIN_MAP = {
        'udp': (udp.snmpUDPDomain,
                udp.UdpSocketTransport,
                lambda h, p: (socket.gethostbyname(h), int(p))),
        'udp6': (udp6.snmpUDP6Domain,
                 udp6.Udp6SocketTransport,
                 lambda h, p: (_getaddrinfo(h, p, socket.AF_INET6, socket.SOCK_DGRAM)[0][4]))
    }
    SNMP_DOMAIN_NAME_MAP = {
        2: 'udp',
        10: 'udp6'
    }

    def n_Transport(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if node[0].attr in self.SNMP_DOMAIN_MAP:
            (ctx['transportDomain'],
             ctx['transportModule'],
             ctx['addrRewriteFun']) = self.SNMP_DOMAIN_MAP[node[0].attr]

        else:
            raise error.PySnmpError(
                'Unsupported transport domain %s' % node[0].attr
            )

    def n_Endpoint(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['transportAddress'] = node[0].attr

    def n_IPv6(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if not len(node):
            if 'transportDomain' not in ctx:
                (ctx['transportDomain'],
                 ctx['transportModule'],
                 ctx['addrRewriteFun']) = self.SNMP_DOMAIN_MAP['udp6']
            return

        if ctx.get('transportAddress') is None:
            ctx['transportAddress'] = ''

        if node[0] == 'semicolon':
            ctx['transportAddress'] = ctx['transportAddress'] + ':'

        else:
            ctx['transportAddress'] = ctx['transportAddress'] + node[0].attr

    def n_Format(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['transportFormat'] = node[0].attr

    def n_Agent_exit(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if 'transportDomain' not in ctx:
            try:
                f = _getaddrinfo(ctx['transportAddress'], 0)[0][0]

            except Exception:
                f = -1

            (ctx['transportDomain'],
             ctx['transportModule'],
             ctx['addrRewriteFun']) = self.SNMP_DOMAIN_MAP[
                self.SNMP_DOMAIN_NAME_MAP.get(f, 'udp')
            ]
        if 'transportFormat' in ctx:
            ctx['transportAddress'] = (
                ctx['transportAddress'], ctx['transportFormat']
            )
            del ctx['transportFormat']

        else:
            ctx['transportAddress'] = (ctx['transportAddress'], self.DEFAULT_PORT)


class _TargetGeneratorTrapPassOne(_TargetGeneratorPassOne):
    DEFAULT_PORT = '162'


class _TargetGeneratorPassTwo(base.GeneratorTemplate):
    def n_Retries(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        try:
            if len(node) > 2:
                ctx['retryCount'] = int(node[2].attr)

            else:
                ctx['retryCount'] = int(node[1].attr)

        except ValueError:
            raise error.PySnmpError('Bad retry value')

    def n_Timeout(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        try:
            if len(node) > 2:
                ctx['timeout'] = int(node[2].attr) * 100

            else:
                ctx['timeout'] = int(node[1].attr) * 100

        except Exception:
            raise error.PySnmpError('Bad timeout value')

    def n_Agent_exit(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['addrName'] = ctx['paramsName']

        config.addTargetAddr(
            snmpEngine,
            ctx['addrName'],
            ctx['transportDomain'],
            ctx['addrRewriteFun'](*ctx['transportAddress']),
            ctx['paramsName'],
            # net-snmp defaults
            ctx.get('timeout', 100),
            ctx.get('retryCount', 5),
            tagList=ctx.get('transportTag', '')
        )

        config.addSocketTransport(
            snmpEngine,
            ctx['transportDomain'],
            ctx['transportModule']().openClientMode()
        )


_TargetGeneratorTrapPassTwo = _TargetGeneratorPassTwo


def generator(cbCtx, ast):
    snmpEngine, ctx = cbCtx
    _TargetGeneratorPassTwo().preorder(
        _TargetGeneratorPassOne().preorder((snmpEngine, ctx), ast), ast
    )


def generatorTrap(cbCtx, ast):
    snmpEngine, ctx = cbCtx
    _TargetGeneratorTrapPassTwo().preorder(
        _TargetGeneratorTrapPassOne().preorder((snmpEngine, ctx), ast), ast
    )
