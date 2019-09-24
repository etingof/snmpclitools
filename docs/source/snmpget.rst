
.. _snmpget.py:

.. |SNMPTOOL| replace:: *snmpget.py*

SNMP GET command
================

The |SNMPTOOL| tool implements SNMP GET command generator. Its usage is
tightly aligned with its
`Net-SNMP prototype <http://www.net-snmp.org/docs/man/snmpget.html>`_.

Command line syntax is as follows:

|SNMPTOOL| [:ref:`options <snmpget-options>`] <:ref:`peer-address <snmpget-peer-address>`> <:ref:`mib-object <snmpget-mib-objects>` [:ref:`mib-object <snmpget-mib-objects>` [...]]>

Options always start with dash (-), other parameters are positional.

.. _snmpget-options:

Options can be categorized by the part they are tackling e.g.

* :ref:`SNMP protocol <snmpget-options-protocol>`
* :ref:`MIB modules <snmpget-options-mibs>`
* :ref:`input <snmpget-options-input>`/:ref:`output <snmpget-options-output>` formatting
* :ref:`network I/O <snmpget-options-network>`

Past these named options, mandatory positional parameters follow:

* :ref:`SNMP peer address <snmpget-peer-address>`
* :ref:`MIB object(s) to work on <snmpget-mib-objects>`

.. _snmpget-options-protocol:

.. include:: options-protocol-rst.inc

.. _snmpget-options-mibs:

.. include:: options-mib-rst.inc

.. _snmpget-options-input:

.. include:: options-input-rst.inc

.. _snmpget-options-output:

.. include:: options-output-rst.inc

.. _snmpget-options-network:

.. include:: options-network-rst.inc

.. _snmpget-options-debug:

.. include:: options-debug-rst.inc

.. _snmpget-peer-address:

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

.. _snmpget-mib-objects:

MIB objects specification
-------------------------

The rest of positional parameters specify SNMP managed objects to work
on. Each object can be either:

* *[MIB-name::]object-name[.index[.index]...]*
* *MIB-name*
* *object-identifier*

When MIB name or object-name is referenced, the |SNMPTOOL| tool will try to
locate and load the corresponding MIB module. The OID specification does not
require MIB access.

.. code-block:: bash

    $ snmpget.py -v2c -c public demo.snmplabs.com TCP-MIB::tcpRtoMin.0
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    $
    $ snmpget.py -v2c -c public demo.snmplabs.com 1.3.6.1.2.1.6.2.0
    1.3.6.1.2.1.6.2.0 = Integer32: 200 milliseconds
    $
    $ snmpget.py  -v2c -c public demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"
    TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389" = Integer32: 'established'

If only MIB name is given, the first MIB object in that MIB will be taken
as object name

.. code-block:: bash

    $ snmpwalk.py -v2c -c public demo.snmplabs.com TCP-MIB::
    TCP-MIB::tcpRtoAlgorithm.0 = Integer32: 'other'
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds

You can query many MIB objects by a single SNMP GET request by specifying
them all at the command line.

.. code-block:: bash

    $ snmpget.py -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysName.0 SNMPv2-MIB::sysLocation.0
    SNMPv2-MIB::sysName.0 = DisplayString: new system name
    SNMPv2-MIB::sysLocation.0 = DisplayString: San Francisco, California, United States

SNMP GET examples
-----------------

SNMPv1 GET example
++++++++++++++++++

The following command will send SNMP v1 GET message:

* with SNMPv1, community 'public'
* to an Agent at demo.snmplabs.com:161
* with SNMPv2-MIB::sysDescr.0 and SNMPv2-MIB::sysName.0 MIB objects

.. code-block:: bash

   snmpget.py -v1 -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0 \
      SNMPv2-MIB::sysName.0

SNMPv2c GET example
+++++++++++++++++++

The following command will send SNMP v2c GET message:

* with SNMPv1, community 'public'
* to an Agent at demo.snmplabs.com:161
* with SNMPv2-MIB::sysDescr.0 and SNMPv2-MIB::sysName.0 MIB objects

.. code-block:: bash

   snmpget.py -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0 \
      SNMPv2-MIB::sysName.0

SNMPv3 GET example
++++++++++++++++++

The following command will send SNMP v3 GET message:

* with SNMPv3, user 'usr-md5-des', MD5 authentication, DES encryption
* to an Agent at demo.snmplabs.com:161
* for IF-MIB::ifInOctets.1 MIB object

.. code-block:: bash

   snmpget.py -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 \
       demo.snmplabs.com IF-MIB::ifInOctets.1
