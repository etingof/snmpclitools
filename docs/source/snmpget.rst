
SNMP GET command
================

The *snmpget.py* tool implements SNMP GET command generator. Its usage it tightly
aligned with its `Net-SNMP <http://www.net-snmp.org/docs/man/snmpget.html>`_ prototype.

Common options
--------------

Release information
+++++++++++++++++++

The *-V* flag reports version information for the SNMP tools and its underlying
libraries.

Debug mode
++++++++++

The *-d* option prints out raw SNMP packets in hex.

The *-D* option lets you debug one or more specific SNMP sub-systems. The required
argument can be one or more (comma-separated) tokens:

* *io*         - report input/output activity and raw data being exchanged
* *dsp*        - report high-level SNMP engine operation
* *msgproc*    - report SNMP message processing subsystem operation
* *secmod*     - report SNMP security subsystem operation
* *mibbuild*   - report MIB files loading and processing
* *mibview*    - report MIB browser initialization and operation (manager role MIB use)
* *mibinstrum* - report MIB instrumentation operation (agent role MIB use)
* *acl*        - report MIB access control subsystem operation
* *proxy*      - report built-in SNMP proxy operation
* *app*        - report SNMP standard application operation
* *all*        - all of the above (verbose!)

You can also negate the token by prepending it with the *!* sign.

Protocol options
----------------

The following options have direct influence on SNMP engine operation.

SNMP version
++++++++++++

The *-v* option specifies SNMP version to be used:

* *1*  - SNMP version 1
* *2c* - SNMP version 2c
* *3*  - SNMP version 3

SNMP community
++++++++++++++

The *-c* option sets SNMP v1/v2c community name. It serves like a shared secret and
identification token between SNMP parties.

.. note::

   The community name is never encrypted on the wire so it's highly insecure.
   This is the sole reason why SNMP is sometimes jokingly referred to as
   *Security -- Not My Problem*.

SNMP USM security name
++++++++++++++++++++++

The *-u* option sets SNMP user name to the User Security Module subsystem. This
is a string from 1 to 32 octets of length. Should be configured in the same way
at both SNMP entities trying to communicate.

SNMP USM security level
+++++++++++++++++++++++

The *-l* option configures authentication and encryption features to be used.

* *noAuthNoPriv*   - no authentication and no encryption
* *authNoPriv*     - use authentication but no encryption
* *authPriv*       - use both authentication and encryption



   -l SECURITY-LEVEL     security level (noAuthNoPriv|authNoPriv|authPriv)
   -a AUTH-PROTOCOL      authentication protocol ID (MD5|SHA|SHA224|SHA256|SHA384|SHA512)
   -A PASSPHRASE         authentication protocol pass phrase (8+ chars)
   -x PRIV-PROTOCOL      privacy protocol ID (3DES|AES|AES128|AES192|AES192BLMT|AES256|AES256BLMT|DES)
   -X PASSPHRASE         privacy protocol pass phrase (8+ chars)
   -E CONTEXT-ENGINE-ID  context engine ID (e.g. 800000020109840301)
   -e ENGINE-ID          security SNMP engine ID (e.g. 800000020109840301)
   -n CONTEXT-NAME       SNMP context name (e.g. bridge1)
   -Z BOOTS,TIME         destination SNMP engine boots/time
MIB options:
   -m MIB[:...]   load given list of MIBs (ALL loads all compiled MIBs)
   -M DIR[:...]   look in given list of directories for MIBs
   -P MIBOPTS     Toggle various defaults controlling MIB parsing:
              XS: search for ASN.1 MIBs in remote directories specified
                  in URL form. The @mib@ token in the URL is substituted
                  with actual MIB to be downloaded. Default repository
                  address is http://mibs.snmplabs.com/asn1/@mib@
              XB: search for pysnmp MIBs in remote directories specified
                  in URL form. The @mib@ token in the URL is substituted
                  with actual MIB to be downloaded. Default repository
                  address is http://mibs.snmplabs.com/pysnmp/fulltexts/@mib@
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
General communication options
   -r RETRIES        number of retries when sending request
   -t TIMEOUT        request timeout (in seconds)
Agent address:
   [<transport-domain>:]<transport-endpoint>
              transport-domain:    (udp|udp6)
              transport-endpoint:  (IP|IPv6|FQDN[:port])
Management parameters:
   [mib-module::]object-name|oid ...
              mib-module:           MIB name (e.g. SNMPv2-MIB)
              object-name:          MIB symbol (e.g. sysDescr.0) or OID
