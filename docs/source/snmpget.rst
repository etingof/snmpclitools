
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

SNMPv3 USM security name
++++++++++++++++++++++++

The *-u* option sets SNMP user name to the User Security Module subsystem. This
is a string from 1 to 32 octets of length. Should be configured in the same way
at both SNMP entities trying to communicate.

SNMPv3 USM security level
+++++++++++++++++++++++++

The *-l* option configures authentication and encryption features to be
used. In SNMP parlance this is known as *Security Level*. Valid values are:

* *noAuthNoPriv*   - no authentication and no encryption
* *authNoPriv*     - use authentication but no encryption
* *authPriv*       - use both authentication and encryption

SNMPv3 authentication protocol
++++++++++++++++++++++++++++++

SNMPv3 messages can be authenticated. The following authentication protocols
can be chosen via the *-a* option:

+--------+----------------+-------------+
| *ID*   | *Algorithm*    | *Reference* |
+--------+----------------+-------------+
| NONE   | -              | RFC3414     |
+--------+----------------+-------------+
| MD5    | HMAC MD5       | RFC3414     |
+--------+----------------+-------------+
| SHA    | HMAC SHA-1 128 | RFC3414     |
+--------+----------------+-------------+
| SHA224 | HMAC SHA-2 224 | RFC7860     |
+--------+----------------+-------------+
| SHA256 | HMAC SHA-2 256 | RFC7860     |
+--------+----------------+-------------+
| SHA384 | HMAC SHA-2 384 | RFC7860     |
+--------+----------------+-------------+
| SHA512 | HMAC SHA-2 512 | RFC7860     |
+--------+----------------+-------------+

SNMPv3 authentication key
+++++++++++++++++++++++++

SNMPv3 message authentication involves a shared secret key known to both SNMP
parties engaged in message exchange. This secret authentication key (AKA
as passphrase) can be conveyed via the *-A* option.

.. note::

   SNMP authentication key must be at least eight octets long.

SNMPv3 encryption protocol
++++++++++++++++++++++++++

SNMPv3 messages can be encrypted (AKA as privacy). The following encryption
protocols can be chosen via the *-x* option:

+------------+------------------------+----------------------+
| *ID*       | *Algorithm*            | *Reference*          |
+------------+------------------------+----------------------+
| NONE       | -                      | RFC3414              |
+------------+------------------------+----------------------+
| DES        | DES                    | RFC3414              |
+------------+------------------------+----------------------+
| AES        | AES CFB 128            | RFC3826              |
+------------+------------------------+----------------------+
| AES192     | AES CFB 192            | RFC Draft            |
+------------+------------------------+----------------------+
| AES256     | AES CFB 256            | RFC Draft            |
+------------+------------------------+----------------------+
| AES192BLMT | AES CFB 192 Blumenthal | RFC Draft            |
+------------+------------------------+----------------------+
| AES256BLMT | AES CFB 256 Blumenthal | RFC Draft            |
+------------+------------------------+----------------------+
| 3DES       | Triple DES EDE         | RFC Draft            |
+------------+------------------------+----------------------+

SNMPv3 encryption key
+++++++++++++++++++++

SNMPv3 message encryption involves a shared secret key known to both SNMP
parties engaged in message exchange. This secret encryption key (AKA
as passphrase) can be conveyed via the *-A* option.

.. note::

   SNMP encryption (e.g. privacy)  key must be at least eight octets long.

SNMPv3 context engine ID
++++++++++++++++++++++++

The *-E* option sets the context engineID used for SNMPv3 REQUEST messages
scopedPdu, given as a hexadecimal string. If not specified, this will
default to the authoritative engineID.

SNMPv3 engine ID
++++++++++++++++

The *-e* option sets the authoritative (security) engineID used for SNMPv3
REQUEST messages, given as a hexadecimal string.  It is typically not
necessary to specify engine ID, as it will usually be discovered
automatically.

SNMPv3 context name
+++++++++++++++++++

The *-n* option sets the SNMPv3 context name to SNMPv3 REQUEST messages.
The default is the empty string. SNMP context name is used to address a
specific instance of SNMP managed objects behind a single SNMP agent.

SNMPv3 engine boots and time
++++++++++++++++++++++++++++

The *-Z* option sets SNMP engine boot counter and its timeline values to
SNMPv3 REQUEST message. These values are used for message authentication.
It is typically not necessary to specify this option, as these values will
usually be discovered automatically.

MIB options
-----------

Pre-load MIBs
+++++++++++++

You may want to pre-load some of the MIB modules to let the tool rendering
SNMP responses in a more meaningful way.

The *-m* option specifies a colon separated list of MIB modules (not files)
to load. The tool will first try to find pre-compiled pysnmp MIB files (by
default in *~/.pysnmp/mibs* in UNIX), then try to find required ASN.1 MIB
file on local filesystem or on Web (by default it will look it up at
*http://mibs.snmplabs.com/asn1/*). If ASN.1 MIB file is found, it will be
compiled into pysnmp form and cached for future use.

The special keyword ALL is used to load all pre-compiled pysnmp MIB modules
in the MIB directory search list.

MIB files search path
+++++++++++++++++++++

The *-M* option specifies a colon separated list of local directories and/or
URLs pointing to remote HTTP/FTP servers where to search for MIBs.

.. note::

   Default MIB search path is *http://mibs.snmplabs.com/asn1/*

Output options
--------------


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
