#!/usr/bin/env python
#
# Notificaton Originator
#
# Copyright 1999-2014 by Ilya Etingof <ilya@glas.net>.
#
import sys, socket, time, traceback
from pysnmp_apps.cli import main, msgmod, secmod, target, pdu, mibview, base
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntforg, context
from pysnmp.proto.proxy import rfc2576
from pysnmp.proto import rfc1902
from pysnmp.proto.api import v1, v2c
from pysnmp import error

def getUsage():
    return "Usage: %s [OPTIONS] <MANAGER> <PARAMETERS>\n\
%s%s%s%s\
TRAP options:\n\
   -C<TRAPOPT>:   set various application specific behaviours:\n\
              i:  send INFORM-PDU, expect a response\n\
%s\
SNMPv1 TRAP management parameters:\n\
   enterprise-oid agent generic-trap specific-trap uptime <management-params>\n\
   where:\n\
              generic-trap:         coldStart|warmStart|linkDown|linkUp|authenticationFailure|egpNeighborLoss|enterpriseSpecific\n\
SNMPv2/SNMPv3 management parameters:\n\
   uptime trap-oid <management-params>\n\
%s" % (sys.argv[0],
       main.getUsage(),
       msgmod.getUsage(),
       secmod.getUsage(),
       mibview.getUsage(),
       target.getUsage(),
       pdu.getWriteUsage())

# Construct c/l interpreter for this app

class Scanner(msgmod.MPScannerMixIn,
              secmod.SMScannerMixIn,
              mibview.MibViewScannerMixIn,
              target.TargetScannerMixIn,
              pdu.ReadPduScannerMixIn,
              main.MainScannerMixIn,
              base.ScannerTemplate):
    def t_appopts(self, s):
        r' -C '
        self.rv.append(base.ConfigToken('appopts'))

    def t_genericTrap(self, s):
        r' coldStart|warmStart|linkDown|linkUp|authenticationFailure|egpNeighborLoss|enterpriseSpecific '
        self.rv.append(base.ConfigToken('genericTrap', s))
        
class Parser(msgmod.MPParserMixIn,
             secmod.SMParserMixIn,
             mibview.MibViewParserMixIn,
             target.TargetParserMixIn,
             pdu.WritePduParserMixIn,
             main.MainParserMixIn,
             base.ParserTemplate):
    def p_trapParams(self, args):
        '''
        TrapV1Params ::= EnterpriseOid whitespace AgentName whitespace GenericTrap whitespace SpecificTrap whitespace Uptime whitespace VarBinds
        EnterpriseOid ::= string
        AgentName ::= string
        GenericTrap ::= genericTrap
        SpecificTrap ::= string
        Uptime ::= string

        TrapV2cParams ::= Uptime whitespace TrapOid whitespace VarBinds
        TrapOid ::= string
        '''

    def p_paramsSpec(self, args):
        '''
        Params ::= TrapV1Params
        Params ::= TrapV2cParams
        '''

    def p_appOptions(self, args):
        '''
        Option ::= ApplicationOption

        ApplicationOption ::= appopts whitespace string
        ApplicationOption ::= appopts string
        '''

class __Generator(base.GeneratorTemplate):
    def n_ApplicationOption(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        if len(node) > 2:
            opt = node[2].attr
        else:
            opt = node[1].attr
        for c in opt:
            if c == 'i':
                ctx['informMode'] = 1
            else:
                raise error.PySnmpError('bad -C option - "%s"' % c)

    def n_EnterpriseOid(self, cbCtx, node):
        snmpEngine, ctx= cbCtx
        ctx['EnterpriseOid'] = node[0].attr

    def n_AgentName(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        try:
            ctx['AgentName'] = socket.gethostbyname(node[0].attr)
        except socket.error:
            raise error.PySnmpError(
                'Bad agent name %s: %s' % (node[0].attr, sys.exc_info()[1])
                )

    def n_GenericTrap(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['GenericTrap'] = node[0].attr

    def n_SpecificTrap(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['SpecificTrap'] = node[0].attr

    def n_Uptime(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['Uptime'] = int(node[0].attr)

    def n_TrapV1Params_exit(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        # Hack SNMP engine's uptime
        sysUpTime, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols(
            '__SNMPv2-MIB', 'sysUpTime'
            )
        sysUpTime.syntax.createdAt = time.time() - float(ctx['Uptime'])/100
        # Initialize v1 PDU with passed params, then proxy it into v2c PDU
        v1Pdu = v1.TrapPDU()
        v1.apiTrapPDU.setDefaults(v1Pdu)
        if 'EnterpriseOid' in ctx:
            v1.apiTrapPDU.setEnterprise(v1Pdu, ctx['EnterpriseOid'])
        if 'AgentName' in ctx:
            v1.apiTrapPDU.setAgentAddr(v1Pdu, ctx['AgentName'])
        if 'GenericTrap' in ctx:
            v1.apiTrapPDU.setGenericTrap(v1Pdu, ctx['GenericTrap'])
        if 'SpecificTrap' in ctx:
            v1.apiTrapPDU.setSpecificTrap(v1Pdu, ctx['SpecificTrap'])
        if 'Uptime' in ctx:
            v1.apiTrapPDU.setTimeStamp(v1Pdu, ctx['Uptime'])
        v2cPdu = rfc2576.v1ToV2(v1Pdu)

        # Drop first two var-binds of v2c PDU as they are set internally by
        # SNMP engine
        varBinds = v2c.apiPDU.getVarBinds(v2cPdu)
        if 'varBinds' not in ctx:
            ctx['varBinds'] = []        
        ctx['varBinds'] = varBinds[2:] + ctx['varBinds']
        # Extract TrapOid from proxied PDU
        ctx['TrapOid' ] = varBinds[1][1].prettyPrint()
        
    def n_TrapOid(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        ctx['TrapOid'] = node[0].attr

    def n_TrapV2cParams_exit(self, cbCtx, node):
        snmpEngine, ctx = cbCtx
        # Hack SNMP engine's uptime
        sysUpTime, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'sysUpTime')
        sysUpTime.syntax.createdAt = time.time() - float(ctx['Uptime'])/100
        
def generator(cbCtx, ast):
    snmpEngine, ctx = cbCtx
    return __Generator().preorder((snmpEngine, ctx), ast)
    
# Run SNMP engine

def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        sys.stderr.write('%s\n' % errorIndication)
        return

snmpEngine = engine.SnmpEngine()

try:
    # Parse c/l into AST
    ast = Parser().parse(
        Scanner().tokenize(' '.join(sys.argv[1:]))
    )

    ctx = {}

    ctx['notificationName'] = 'myNotifyName'
    ctx['transportTag'] = 'mytag'

    # Apply configuration to SNMP entity
    main.generator((snmpEngine, ctx), ast)
    msgmod.generator((snmpEngine, ctx), ast)
    secmod.generator((snmpEngine, ctx), ast)    
    mibview.generator((snmpEngine, ctx), ast)
    target.generatorTrap((snmpEngine, ctx), ast)
    pdu.writePduGenerator((snmpEngine, ctx), ast)
    generator((snmpEngine, ctx), ast)

    snmpContext = context.SnmpContext(snmpEngine)

    # Agent-side VACM setup
    config.addContext(snmpEngine, '')
    config.addVacmUser(snmpEngine, 1, ctx['securityName'],
                       'noAuthNoPriv', (), (), (1,3,6),
                       contextName=ctx.get('contextName', '')) # v1
    config.addVacmUser(snmpEngine, 2, ctx['securityName'],
                       'noAuthNoPriv', (), (), (1,3,6),
                       contextName=ctx.get('contextName', '')) # v2c
    config.addVacmUser(snmpEngine, 3, ctx['securityName'],
                       'authPriv', (), (), (1,3,6),
                       contextName=ctx.get('contextName', '')) # v3
    config.addVacmUser(snmpEngine, 3, ctx['securityName'],
                       'authNoPriv', (), (), (1,3,6),
                       contextName=ctx.get('contextName', '')) # v3
    config.addVacmUser(snmpEngine, 3, ctx['securityName'],
                       'noAuthNoPriv', (), (), (1,3,6),
                       contextName=ctx.get('contextName', '')) # v3

    if ctx.get('contextName', ''):
        snmpContext.registerContextName(
            ctx['contextName'],
            # ref to base MIB instrum
            snmpEngine.msgAndPduDsp.mibInstrumController
        )

    config.addNotificationTarget(
        snmpEngine, ctx['notificationName'], ctx['paramsName'],
        ctx['transportTag'], 'informMode' in ctx and 'inform' or 'trap'
    )

    ntforg.NotificationOriginator(snmpContext).sendVarBinds(
        snmpEngine,
        ctx['notificationName'],
        snmpContext,
        ctx.get('contextName', ''),
        ctx['TrapOid'],
        # managed objects instance index  XXX TODO
        None,
        ctx['varBinds'],
        cbFun, ctx
    )

    snmpEngine.transportDispatcher.runDispatcher()

except KeyboardInterrupt:
    sys.stderr.write('Shutting down...\n')

except error.PySnmpError:
    sys.stderr.write('Error: %s\n%s' % (sys.exc_info()[1], getUsage()))
    sys.exit(-1)

except Exception:
    sys.stderr.write('Process terminated: %s\n' % sys.exc_info()[1])
    for line in traceback.format_exception(*sys.exc_info()):
        sys.stderr.write(line.replace('\n', ';'))
    sys.exit(-1)
