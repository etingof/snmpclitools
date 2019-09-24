
.. _snmpwalk.py:

.. |SNMPTOOL| replace:: *snmpwalk.py*

SNMP GETNEXT command
====================

The |SNMPTOOL| tool implements SNMP GETNEXT command generator. Its usage
is tightly aligned with its
`Net-SNMP prototype <http://www.net-snmp.org/docs/man/snmpwalk.html>`_.

Command line syntax is as follows:

|SNMPTOOL| [:ref:`options <snmpwalk-options>`] <:ref:`peer-address <snmpwalk-peer-address>`> <:ref:`mib-object <snmpwalk-mib-objects>` [:ref:`mib-object <snmpwalk-mib-objects>` [...]]>

Options always start with dash (-), other parameters are positional.

.. _snmpwalk-options:

Options can be categorized by the part they are tackling e.g.

* :ref:`SNMP protocol <snmpwalk-options-protocol>`
* :ref:`MIB modules <snmpwalk-options-mibs>`
* :ref:`input <snmpwalk-options-input>`/:ref:`output <snmpwalk-options-output>` formatting
* :ref:`network I/O <snmpwalk-options-network>`
* :ref:`SNMP GETNEXT <options-getnext>` command specifics

Past these named options, mandatory positional parameters follow:

* :ref:`SNMP peer address <snmpwalk-peer-address>`
* :ref:`MIB object(s) to work on <snmpwalk-mib-objects>`

.. _snmpwalk-options-protocol:

.. include:: options-protocol-rst.inc

.. _snmpwalk-options-mibs:

.. include:: options-mib-rst.inc

.. _snmpwalk-options-input:

.. include:: options-input-rst.inc

.. _snmpwalk-options-output:

.. include:: options-output-rst.inc

.. _snmpwalk-options-network:

.. include:: options-network-rst.inc

.. _options-getnext:

GETNEXT options
---------------

The following one-letter options following the *-C* option modify
the way how |SNMPTOOL| tool behaves. These options are mostly specific
to |SNMPTOOL|'s operation logic.

Ensure increasing OIDs
++++++++++++++++++++++

The *-Cc* option disables the built-in check for ever increasing response
OIDs. SNMP agent returning an out-of-order OID may cause infinite loop
between SNMP agent and SNMP manager walking it.

Report time taken
+++++++++++++++++

The *-Ct* option makes |SNMPTOOL| reporting wall-clock time taken to
complete SNMP agent walk.

Report responses count
++++++++++++++++++++++

The *-Cp* option makes |SNMPTOOL| reporting the total count of fetched and
reported MIB objects during its walk.

.. include:: options-debug-rst.inc

.. _snmpwalk-peer-address:

SNMP peer address
-----------------

The first positional parameter specifies SNMP peer address on the network
and, optionally, network protocol to use.

The network protocol can be either *udp* for UDP-over-IPv4 or *udp6* for
UDP-over-IPv6.

The network address is either IPv4 or IPv6 address or a fully qualified
domain name optionally followed by a colon-separated port number. The
default for port is 161.

.. note::

   Numeric IPv6 addresses should be surrounded by square brackets to
   be parsed correctly. The entire token (address in brackets) might
   need to be quored to avoid shell expansion.
   Example: *'udpv6:[::1]:161'*

.. _snmpwalk-mib-objects:

MIB objects specification
-------------------------

The rest of positional parameters specify SNMP managed objects to walk by.
Each object can be either:

* *[MIB-name::]object-name[.index[.index]...]*
* *MIB-name*
* *object-identifier*

.. note::

   The MIB object(s) specified are interpreted as a starting point for
   "walking" the SNMP agent. The SNMP agent will return zero or one *next*
   object past the one you've asked for.

When MIB name or object-name is referenced, the |SNMPTOOL| tool will try to
locate and load the corresponding MIB module. The OID specification does not
require MIB access.

.. code-block:: bash

    $ snmpwalk.py -v2c -c public demo.snmplabs.com TCP-MIB::tcpRtoMin
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    $
    $ snmpwalk.py -v2c -c public demo.snmplabs.com 1.3.6.1.2.1.6.2
    1.3.6.1.2.1.6.2.0 = Integer32: 200 milliseconds
    $
    $ snmpwalk.py  -v2c -c public demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"
    TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389" = Integer32: 'established'

If only MIB name is given, the first MIB object in that MIB will be taken
as object name

.. code-block:: bash

    $ snmpwalk.py -v2c -c public demo.snmplabs.com TCP-MIB::
    TCP-MIB::tcpRtoAlgorithm.0 = Integer32: 'other'
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    ...

You can query many MIB objects by a single SNMP GETNEXT request by specifying
them all at the command line.

.. code-block:: bash

    $ snmpwalk.py  -v2c -c public demo.snmplabs.com TCP-MIB:: IF-MIB::
    TCP-MIB::tcpRtoAlgorithm.0 = Integer32: 'other'
    IF-MIB::ifNumber.0 = Integer32: 2
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    IF-MIB::ifIndex."1" = InterfaceIndex: 1
    ...

The output MIB objects count is guaranteed to be a multiple of the requested
MIB objects times the maximum number of response MIB objects for any of the
request MIB objects that peer SNMP agent is able to serve.

SNMP GETNEXT examples
---------------------

SNMPv1 GETNEXT example
++++++++++++++++++++++

The following command will send SNMP v1 GETNEXT message:

* with SNMPv1, community 'public'
* to an Agent at demo.snmplabs.com:161
* for MIB objects starting from SNMPv2-MIB::system and IF-MIB

.. code-block:: bash

    snmpwalk.py -v1 -c public demo.snmplabs.com SNMPv2-MIB::system IF-MIB::

SNMPv2c GETNEXT example
+++++++++++++++++++++++

The following command will send SNMP v2c GETNEXT message:

* with SNMPv1, community 'public'
* to an Agent at demo.snmplabs.com:161
* for MIB objects starting from SNMPv2-MIB::system and IF-MIB

.. code-block:: bash

    snmpwalk.py -v2c -c public demo.snmplabs.com SNMPv2-MIB::system IF-MIB::

SNMPv3 GETNEXT example
++++++++++++++++++++++

The following command will send SNMP v3 GETNEXT message:

* with SNMPv3, user 'usr-md5-des', MD5 authentication, DES encryption
* to an Agent at demo.snmplabs.com:161
* for MIB objects starting from SNMPv2-MIB::system and IF-MIB

.. code-block:: bash

    snmpwalk.py -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 \
        demo.snmplabs.com SNMPv2-MIB::system IF-MIB::

