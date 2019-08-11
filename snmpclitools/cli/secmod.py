#
# This file is part of snmpclitools software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpclitools/license.html
#
from pysnmp import error
from pysnmp.entity import config
from pysnmp.proto import rfc1902

from snmpclitools.cli import base

AUTH_PROTOCOLS = {
    'MD5': config.usmHMACMD5AuthProtocol,
    'SHA': config.usmHMACSHAAuthProtocol,
    'SHA224': config.usmHMAC128SHA224AuthProtocol,
    'SHA256': config.usmHMAC192SHA256AuthProtocol,
    'SHA384': config.usmHMAC256SHA384AuthProtocol,
    'SHA512': config.usmHMAC384SHA512AuthProtocol,
    'NONE': config.usmNoAuthProtocol
}

PRIV_PROTOCOLS = {
  'DES': config.usmDESPrivProtocol,
  '3DES': config.usm3DESEDEPrivProtocol,
  'AES': config.usmAesCfb128Protocol,
  'AES128': config.usmAesCfb128Protocol,
  'AES192': config.usmAesCfb192Protocol,
  'AES192BLMT': config.usmAesBlumenthalCfb192Protocol,
  'AES256': config.usmAesCfb256Protocol,
  'AES256BLMT': config.usmAesBlumenthalCfb256Protocol,
  'NONE': config.usmNoPrivProtocol
}


def getUsage():
    return """\
SNMPv1/v2c security options:
   -c COMMUNITY          SNMP community string (e.g. public)
SNMPv3 security options:
   -u SECURITY-NAME      SNMP USM user security name (e.g. bert)
   -l SECURITY-LEVEL     security level (noAuthNoPriv|authNoPriv|authPriv)
   -a AUTH-PROTOCOL      authentication protocol ID (%s)
   -A PASSPHRASE         authentication protocol pass phrase (8+ chars)
   -x PRIV-PROTOCOL      privacy protocol ID (%s)
   -X PASSPHRASE         privacy protocol pass phrase (8+ chars)
   -E CONTEXT-ENGINE-ID  context engine ID (e.g. 800000020109840301)
   -e ENGINE-ID          security SNMP engine ID (e.g. 800000020109840301)
   -n CONTEXT-NAME       SNMP context name (e.g. bridge1)
   -Z BOOTS,TIME         destination SNMP engine boots/time
   -3[MmKk]  0xHEXKEY    keys to be used for authentication (-3m, -3k) and
                         encryption (-3M, -3K). These options allow you to
                         set the master authentication and encryption keys
                         (-3m and -3M respectively) or set the localized
                         authentication and encryption keys (-3k and -3K
                         respectively).
""" % ('|'.join(sorted([x for x in AUTH_PROTOCOLS if x != 'NONE'])),
       '|'.join(sorted([x for x in PRIV_PROTOCOLS if x != 'NONE'])))


# Scanner

class SMScannerMixIn(object):

    # SNMPv1/v2

    def t_community(self, s):
        """ -c """
        self.rv.append(base.ConfigToken('community'))

    # SNMPv3

    def t_authProtocol(self, s):
        """ -a """
        self.rv.append(base.ConfigToken('authProtocol'))

    def t_authKey(self, s):
        """ -A """
        self.rv.append(base.ConfigToken('authKey'))

    def t_privProtocol(self, s):
        """ -x """
        self.rv.append(base.ConfigToken('privProtocol'))

    def t_privKey(self, s):
        """ -X """
        self.rv.append(base.ConfigToken('privKey'))

    def t_securityName(self, s):
        """ -u """
        self.rv.append(base.ConfigToken('securityName'))

    def t_securityLevel(self, s):
        """ -l """
        self.rv.append(base.ConfigToken('securityLevel'))

    def t_securityEngineId(self, s):
        """ -e """
        self.rv.append(base.ConfigToken('securityEngineId'))

    def t_contextEngineId(self, s):
        """ -E """
        self.rv.append(base.ConfigToken('contextEngineId'))

    def t_contextName(self, s):
        """ -n """
        self.rv.append(base.ConfigToken('contextName'))

    def t_engineBoots(self, s):
        """ -Z """
        self.rv.append(base.ConfigToken('engineBoots'))

    def t_masterAuthKey(self, s):
        """ -3m """
        self.rv.append(base.ConfigToken('masterAuthKey'))

    def t_localizedAuthKey(self, s):
        """ -3k """
        self.rv.append(base.ConfigToken('localizedAuthKey'))

    def t_masterPrivKey(self, s):
        """ -3M """
        self.rv.append(base.ConfigToken('masterPrivKey'))

    def t_localizedPrivKey(self, s):
        """ -3K """
        self.rv.append(base.ConfigToken('localizedPrivKey'))


# Parser


class SMParserMixIn(object):
    def p_smSpec(self, args):
        """
        Option ::= SnmpV1Option
        Option ::= SnmpV3Option

        SnmpV1Option ::= Community
        Community ::= community string
        Community ::= community whitespace string

        SnmpV3Option ::= AuthProtocol
        SnmpV3Option ::= AuthKey
        SnmpV3Option ::= MasterAuthKey
        SnmpV3Option ::= LocalizedAuthKey

        SnmpV3Option ::= PrivProtocol
        SnmpV3Option ::= PrivKey
        SnmpV3Option ::= MasterPrivKey
        SnmpV3Option ::= LocalizedPrivKey

        SnmpV3Option ::= SecurityName
        SnmpV3Option ::= SecurityLevel
        SnmpV3Option ::= SecurityEngineId
        SnmpV3Option ::= ContextEngineId
        SnmpV3Option ::= ContextName
        SnmpV3Option ::= EngineBoots

        AuthProtocol ::= authProtocol string
        AuthProtocol ::= authProtocol whitespace string
        AuthKey ::= authKey string
        AuthKey ::= authKey whitespace string
        MasterAuthKey ::= masterAuthKey string
        MasterAuthKey ::= masterAuthKey whitespace string
        LocalizedAuthKey ::= localizedAuthKey string
        LocalizedAuthKey ::= localizedAuthKey whitespace string

        PrivProtocol ::= privProtocol string
        PrivProtocol ::= privProtocol whitespace string
        PrivKey ::= privKey string
        PrivKey ::= privKey whitespace string
        MasterPrivKey ::= masterPrivKey string
        MasterPrivKey ::= masterPrivKey whitespace string
        LocalizedPrivKey ::= localizedPrivKey string
        LocalizedPrivKey ::= localizedPrivKey whitespace string

        SecurityName ::= securityName string
        SecurityName ::= securityName whitespace string
        SecurityLevel ::= securityLevel string
        SecurityLevel ::= securityLevel whitespace string
        SecurityEngineId ::= securityEngineId string
        SecurityEngineId ::= securityEngineId whitespace string
        ContextEngineId ::= contextEngineId string
        ContextEngineId ::= contextEngineId whitespace string
        ContextName ::= contextName string
        ContextName ::= contextName whitespace string
        EngineBoots ::= engineBoots string
        EngineBoots ::= engineBoots whitespace string
        """


# Generator

class _SMGenerator(base.GeneratorTemplate):
    # SNMPv1/v2
    def n_Community(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['communityName'] = node[2].attr

        else:
            ctx['communityName'] = node[1].attr

    # SNMPv3
    def n_AuthProtocol(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr.upper()

        else:
            p = node[1].attr.upper()

        try:
            ctx['authProtocol'] = AUTH_PROTOCOLS[p]

        except KeyError:
            raise error.PySnmpError('Unknown authentication protocol "%s"' % p)

    def n_AuthKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr

        else:
            p = node[1].attr

        if len(p) < 8:
            raise error.PySnmpError('Short authentication key (8+ chars required)')

        ctx['authKey'] = p

    def n_MasterAuthKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr

        else:
            p = node[1].attr

        if len(p) < 8:
            raise error.PySnmpError(
                'Short master authentication key (8+ chars required)')

        ctx['masterAuthKey'] = p

    def n_LocalizedAuthKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr

        else:
            p = node[1].attr

        if len(p) < 8:
            raise error.PySnmpError(
                'Short localized authentication key (8+ chars required)')

        ctx['localizedAuthKey'] = p

    def n_PrivProtocol(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr.upper()

        else:
            p = node[1].attr.upper()

        try:
            ctx['privProtocol'] = PRIV_PROTOCOLS[p]

        except KeyError:
            raise error.PySnmpError('Unknown privacy protocol "%s"' % p)

    def n_PrivKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr

        else:
            p = node[1].attr

        if len(p) < 8:
            raise error.PySnmpError('Short privacy key (8+ chars required)')

        ctx['privKey'] = p

    def n_MasterPrivKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr

        else:
            p = node[1].attr

        if len(p) < 8:
            raise error.PySnmpError(
                'Short master privacy key (8+ chars required)')

        ctx['masterPrivKey'] = p

    def n_LocalizedPrivKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            p = node[2].attr

        else:
            p = node[1].attr

        if len(p) < 8:
            raise error.PySnmpError(
                'Short localized privacy key (8+ chars required)')

        ctx['localizedPrivKey'] = p

    def n_SecurityName(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['securityName'] = node[2].attr

        else:
            ctx['securityName'] = node[1].attr

    def n_SecurityLevel(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['securityLevel'] = node[2].attr

        else:
            ctx['securityLevel'] = node[1].attr

    def n_SecurityEngineId(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['securityEngineId'] = node[2].attr

        else:
            ctx['securityEngineId'] = node[1].attr

    def n_ContextEngineId(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['contextEngineId'] = node[2].attr

        else:
            ctx['contextEngineId'] = node[1].attr

    def n_ContextName(self, cbCtx, node):
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['contextName'] = node[2].attr

        else:
            ctx['contextName'] = node[1].attr

    def n_EngineBoots(self, cbCtx, node):  # XXX
        snmpEngine, ctx = cbCtx

        if len(node) > 2:
            ctx['engineBoots'] = node[2].attr

        else:
            ctx['engineBoots'] = node[1].attr

        if ',' in ctx['engineBoots']:
            ctx['engineBoots'], ctx['engineTime'] = ctx['engineBoots'].split(',', 1)

        else:
            ctx['engineTime'] = 0


def generator(cbCtx, ast):
    snmpEngine, ctx = cbCtx

    _SMGenerator().preorder(cbCtx, ast)

    # Commit collected data
    if ctx['versionId'] == 3:

        def _unhexKey(key):
            if key.lower().startswith('0x'):
                key = key[2:]

            return rfc1902.OctetString(hexValue=key)

        if 'securityName' not in ctx:
            raise error.PySnmpError('Security name not specified')

        if 'securityLevel' not in ctx:
            raise error.PySnmpError('Security level not specified')

        if 'securityEngineId' in ctx:
            securityEngineId = _unhexKey(ctx['securityEngineId'])

        else:
            securityEngineId = None

        if 'contextEngineId' in ctx:
            ctx['contextEngineId'] = _unhexKey(ctx['contextEngineId'])

        else:
            ctx['contextEngineId'] = None

        if 'localizedAuthKey' in ctx:
            ctx['authKey'] = _unhexKey(ctx.pop('localizedAuthKey'))
            authKeyType = config.usmKeyTypeLocalized

        elif 'masterAuthKey' in ctx:
            ctx['authKey'] = _unhexKey(ctx.pop('masterAuthKey'))
            authKeyType = config.usmKeyTypeMaster

        else:
            authKeyType = config.usmKeyTypePassphrase

        if 'localizedPrivKey' in ctx:
            ctx['privKey'] = _unhexKey(ctx.pop('localizedPrivKey'))
            privKeyType = config.usmKeyTypeLocalized

        elif 'masterPrivKey' in ctx:
            ctx['privKey'] = _unhexKey(ctx.pop('masterPrivKey'))
            privKeyType = config.usmKeyTypeMaster

        else:
            privKeyType = config.usmKeyTypePassphrase

        if (authKeyType == config.usmKeyTypeLocalized or
                privKeyType == config.usmKeyTypeLocalized):
            # Wildcard security engine ID assocciating localized keys
            # with any authoritative SNMP engine
            securityEngineId = rfc1902.OctetString(hexValue='0000000000')

        ctx['securityEngineId'] = securityEngineId

        if ctx['securityLevel'] == 'noAuthNoPriv':
            if 'authKey' in ctx:
                del ctx['authKey']

            if 'privKey' in ctx:
                del ctx['privKey']

        elif ctx['securityLevel'] == 'authNoPriv':
            if 'privKey' in ctx:
                del ctx['privKey']

        if 'authKey' in ctx:
            if 'authProtocol' not in ctx:
                ctx['authProtocol'] = config.usmHMACMD5AuthProtocol

        else:
            ctx['authProtocol'] = config.usmNoAuthProtocol
            ctx['authKey'] = None

        if 'privKey' in ctx:
            if 'privProtocol' not in ctx:
                ctx['privProtocol'] = config.usmDESPrivProtocol

        else:
            ctx['privProtocol'] = config.usmNoPrivProtocol
            ctx['privKey'] = None

        config.addV3User(
            snmpEngine,
            ctx['securityName'],
            ctx['authProtocol'],
            ctx['authKey'],
            ctx['privProtocol'],
            ctx['privKey'],
            securityEngineId=securityEngineId,
            securityName=ctx['securityName'],
            authKeyType=authKeyType,
            privKeyType=privKeyType
        )

        # edit SNMP engine boots/uptime

        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

        if 'engineBoots' in ctx:
            snmpEngineBoots, = mibBuilder.importSymbols(
                '__SNMP-FRAMEWORK-MIB', 'snmpEngineBoots')
            snmpEngineBoots.setSyntax(
                snmpEngineBoots.getSyntax().clone(ctx['engineBoots'])
            )

        if 'engineTime' in ctx:
            snmpEngineTime, = mibBuilder.importSymbols(
                '__SNMP-FRAMEWORK-MIB', 'snmpEngineTime')
            snmpEngineTime.setSyntax(
                snmpEngineTime.getSyntax().clone(ctx['engineTime'])
            )

    else:  # SNMPv1/v2c
        if 'communityName' not in ctx:
            raise error.PySnmpError('Community name not specified')

        ctx['securityName'] = 'my-agent'
        ctx['securityLevel'] = 'noAuthNoPriv'

        config.addV1System(
            snmpEngine,
            ctx['securityName'],
            ctx['communityName']
        )

    ctx['paramsName'] = ctx['securityName']

    config.addTargetParams(
        snmpEngine, ctx['paramsName'], ctx['securityName'],
        ctx['securityLevel'], ctx['versionId']
    )
