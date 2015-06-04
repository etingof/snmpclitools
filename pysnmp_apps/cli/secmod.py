from pysnmp_apps.cli import base
from pysnmp.entity import config
from pysnmp import error

# Usage

def getUsage():
    return "\
SNMPv1/v2c security options:\n\
   -c COMMUNITY          community name\n\
SNMPv3 security options:\n\
   -u SECURITY-NAME      USM user security name\n\
   -l SECURITY-LEVEL     \"noAuthNoPriv\"|\"authNoPriv\"|\"authPriv\"\n\
   -a AUTH-PROTOCOL      \"MD5\"|\"SHA\"\n\
   -A AUTH-KEY           user authentication key\n\
   -x PRIV-PROTOCOL      \"DES\"|\"AES\"\n\
   -X PRIV-KEY           user privacy key\n\
   -E CONTEXT-ENGINE-ID  authoritative context engine ID\n\
   -e ENGINE-ID          authoritative SNMP engine ID (will discover)\n\
   -n CONTEXT-NAME       authoritative context name\n\
   -Z BOOTS,TIME         destination SNMP engine boots/uptime\n\
"

# Scanner

class SMScannerMixIn:
    # SNMPv1/v2
    
    def t_community(self, s):
        r' -c '
        self.rv.append(base.ConfigToken('community'))

    # SNMPv3
    
    def t_authProtocol(self, s):
        r' -a '
        self.rv.append(base.ConfigToken('authProtocol'))

    def t_authKey(self, s):
        r' -A '
        self.rv.append(base.ConfigToken('authKey'))

    def t_privProtocol(self, s):
        r' -x '
        self.rv.append(base.ConfigToken('privProtocol'))

    def t_privKey(self, s):
        r' -X '
        self.rv.append(base.ConfigToken('privKey'))

    def t_securityName(self, s):
        r' -u '
        self.rv.append(base.ConfigToken('securityName'))

    def t_securityLevel(self, s):
        r' -l '
        self.rv.append(base.ConfigToken('securityLevel'))

    def t_engineID(self, s):
        r' -e '
        self.rv.append(base.ConfigToken('engineID'))

    def t_contextEngineId(self, s):
        r' -E '
        self.rv.append(base.ConfigToken('contextEngineId'))

    def t_contextName(self, s):
        r' -n '
        self.rv.append(base.ConfigToken('contextName'))

    def t_engineBoots(self, s):
        r' -Z '
        self.rv.append(base.ConfigToken('engineBoots'))

# Parser

class SMParserMixIn:
    def p_smSpec(self, args):
        '''
        Option ::= SnmpV1Option
        Option ::= SnmpV3Option
        
        SnmpV1Option ::= Community
        Community ::= community string
        Community ::= community whitespace string

        SnmpV3Option ::= AuthProtocol
        SnmpV3Option ::= AuthKey
        SnmpV3Option ::= PrivProtocol
        SnmpV3Option ::= PrivKey
        SnmpV3Option ::= SecurityName
        SnmpV3Option ::= SecurityLevel
        SnmpV3Option ::= EngineID
        SnmpV3Option ::= ContextEngineId
        SnmpV3Option ::= ContextName
        SnmpV3Option ::= EngineBoots

        AuthProtocol ::= authProtocol string
        AuthProtocol ::= authProtocol whitespace string
        AuthKey ::= authKey string
        AuthKey ::= authKey whitespace string
        PrivProtocol ::= privProtocol string
        PrivProtocol ::= privProtocol whitespace string
        PrivKey ::= privKey string
        PrivKey ::= privKey whitespace string
        SecurityName ::= securityName string
        SecurityName ::= securityName whitespace string
        SecurityLevel ::= securityLevel string
        SecurityLevel ::= securityLevel whitespace string
        EngineID ::= engineID string
        EngineID ::= engineID whitespace string
        ContextEngineId ::= contextEngineId string
        ContextEngineId ::= contextEngineId whitespace string
        ContextName ::= contextName string
        ContextName ::= contextName whitespace string
        EngineBoots ::= engineBoots string
        EngineBoots ::= engineBoots whitespace string
        '''
# Generator

class __SMGenerator(base.GeneratorTemplate):
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
        if p.find('MD5') != -1:
            ctx['authProtocol'] = config.usmHMACMD5AuthProtocol
        elif p.find('SHA') != -1:
            ctx['authProtocol'] = config.usmHMACSHAAuthProtocol
        else:
            raise error.PySnmpError('Unknown auth protocol \"%s\"' % p)

    def n_AuthKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if len(node) > 2:
            ctx['authKey'] = node[2].attr
        else:
            ctx['authKey'] = node[1].attr

    def n_PrivProtocol(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if len(node) > 2:
            p = node[2].attr.upper()
        else:
            p = node[1].attr.upper()
        if p.find('DES') != -1:
            ctx['privProtocol'] = config.usmDESPrivProtocol
        elif p.find('AES') != -1:
            ctx['privProtocol'] = config.usmAesCfb128Protocol
        else:
            raise error.PySnmpError('Unknown priv protocol \"%s\"' % p)

    def n_PrivKey(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if len(node) > 2:
            ctx['privKey'] = node[2].attr
        else:
            ctx['privKey'] = node[1].attr

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

    def n_EngineID(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if len(node) > 2:
            ctx['engineID'] = node[2].attr
        else:
            ctx['engineID'] = node[1].attr

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

    def n_EngineBoots(self, cbCtx, node): # XXX
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
    __SMGenerator().preorder(cbCtx, ast)
    # Commit collected data
    if ctx['versionId'] == 3:
        if 'securityName' not in ctx:
            raise error.PySnmpError('Security name not specified')
        if 'securityLevel' not in ctx:
            raise error.PySnmpError('Security level not specified')
        if ctx['securityLevel'] == 'noAuthNoPriv':
            if 'authKey' in ctx: del ctx['authKey']
            if 'privKey' in ctx: del ctx['privKey']
        elif ctx['securityLevel'] == 'authNoPriv':
            if 'privKey' in ctx: del ctx['privKey']
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
            ctx['privKey']
            )
        # edit SNMP engine boots/uptime
        if 'engineBoots' in ctx:
            snmpEngineBoots, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMP-FRAMEWORK-MIB', 'snmpEngineBoots')
            snmpEngineBoots.setSyntax(
                snmpEngineBoots.getSyntax().clone(ctx['engineBoots'])
            )
        if 'engineTime' in ctx:
            snmpEngineTime, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMP-FRAMEWORK-MIB', 'snmpEngineTime')
            snmpEngineTime.setSyntax(
                snmpEngineTime.getSyntax().clone(ctx['engineTime'])
            )
    else: # SNMPv1/v2c
        if 'communityName' not in ctx:
            raise error.PySnmpError('Community name not specified')            
        ctx['securityName'] = 'my-agent'
        ctx['securityLevel'] = 'noAuthNoPriv'            
        config.addV1System(
            snmpEngine,
            ctx['securityName'],
            ctx['communityName']
        )

    ctx['paramsName'] = '%s-params' % ctx['securityName']
    config.addTargetParams(
        snmpEngine, ctx['paramsName'],ctx['securityName'],
        ctx['securityLevel'], ctx['versionId']
        )
