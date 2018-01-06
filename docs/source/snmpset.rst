
.. _snmpset.py:

.. |SNMPTOOL| replace:: *snmpset.py*

SNMP SET command
================

The |SNMPTOOL| tool implements SNMP SET command generator. Its usage is
tightly aligned with its
`Net-SNMP prototype <http://www.net-snmp.org/docs/man/snmpset.html>`_.

Command line syntax is as follows:

|SNMPTOOL| [:ref:`options <options>`] <:ref:`peer-address <snmpset-peer-address>`> <:ref:`mib-object <snmpset-mib-objects>` [:ref:`mib-object <snmpset-mib-objects>` [...]]>

Options always start with dash (-), other parameters are positional.

.. _options:

Options can be categorized by the part they are tackling e.g.

* :ref:`SNMP protocol <options-protocol>`
* :ref:`MIB modules <options-mibs>`
* :ref:`input <options-input>`/:ref:`output <options-output>` formatting
* :ref:`network I/O <options-network>`

Past these named options, mandatory positional parameters follow:

* :ref:`SNMP peer address <snmpset-peer-address>`
* :ref:`MIB object(s) to work on <snmpset-mib-objects>`

.. include:: options-protocol-rst.inc
.. include:: options-mib-rst.inc
.. include:: options-input-rst.inc
.. include:: options-output-rst.inc
.. include:: options-network-rst.inc
.. include:: options-debug-rst.inc

.. _snmpset-peer-address:

SNMP peer address
-----------------

The first positional parameter specifies SNMP peer address on the network
and, optionally, network protocol to use.

The network protocol can be either *udp* for UDP-over-IPv4 or *udp6* for
UDP-over-IPv6.

The network address is either IPv4 or IPv6 address or a fully qualified
domain name optionally followed by a colon-separated port number. The
default for port is 161.

.. _snmpset-mib-objects:

MIB objects specification
-------------------------

The rest of positional parameters specify SNMP managed objects to modify and
their new values. The syntax for setting a new value to a MIB object is
either of:

* *mib-object = value*
* *mib-object <snmp-type> value*

The *=* modifier can only be used if *mib-object* refers to a MIB which
would be looked up and the type of the *value* to set would be figured out.

Alternatively, *snmp-type* modifier can be passed to directly specify SNMP
type of the *value* being set without using the MIB.

The following *snmp-type*'s are recognized:

+--------+--------------------+
| *ID*   | *SNMP type*        |
+--------+--------------------+
| i      | INTEGER            |
+--------+--------------------+
| u      | Unsigned32         |
+--------+--------------------+
| s      | OctetString        |
+--------+--------------------+
| n      | NULL               |
+--------+--------------------+
| o      | ObjectIdentifier   |
+--------+--------------------+
| t      | TimeTicks          |
+--------+--------------------+
| a      | IP address         |
+--------+--------------------+

The *mib-object* can be specified in either of these ways:

* *[MIB-name::]object-name[.index[.index]...]*
* *object-identifier*

When MIB name or object-name is referenced, the |SNMPTOOL| tool will try to
locate and load the corresponding MIB module. The OID specification does not
require MIB access, however if you are not using a MIB, be prepared to
specify SNMP value type by hand.

.. code-block:: bash

    $ snmpset.py -v2c -c private demo.snmplabs.com IF-MIB::ifAdminStatus."1" = 'up'
    IF-MIB::ifAdminStatus."1" = Integer32: 'up'
    $
    $ snmpset.py -v2c -c private demo.snmplabs.com 1.3.6.1.2.1.2.2.1.7.1 i 1
    1.3.6.1.2.1.6.2.0 = Integer32: 1

You can address many MIB objects by a single SNMP SET request by specifying
them all at the command line.

.. code-block:: bash

    $ snmpset.py -v2c -c private demo.snmplabs.com IF-MIB::ifAdminStatus."1" = 'up' \
        IF-MIB::ifAdminStatus."2" = 'down'
    IF-MIB::ifAdminStatus."1" = Integer32: 'up'
    IF-MIB::ifAdminStatus."2" = Integer32: 'down'

SNMP SET examples
-----------------

SNMPv1 SET example
++++++++++++++++++

The following command will send SNMP v1 SET message:

* with SNMPv1, community 'public'
* to an Agent at demo.snmplabs.com:161
* setting some MIB objects to the new values

.. code-block:: bash

   snmpset.py -v1 -c public demo.snmplabs.com \
       1.3.6.1.2.1.1.9.1.2.1 = 1.3.6.1.4.1.20408.1.1 \
       1.3.6.1.2.1.1.9.1.3.1 s "new system name"

SNMPv2c SET example
+++++++++++++++++++

The following command will send SNMP v2c SET message:

* with SNMPv2c, community 'public'
* to an Agent at demo.snmplabs.com:161
* setting some MIB objects to the new values

.. code-block:: bash

   snmpset.py -v2c -c public demo.snmplabs.com \
       1.3.6.1.2.1.1.9.1.2.1 = 1.3.6.1.4.1.20408.1.1 \
       1.3.6.1.2.1.1.9.1.3.1 s "new system name"

SNMPv3 SET example
++++++++++++++++++

The following command will send SNMP v3 SET message:

* with SNMPv3, user 'usr-md5-des', MD5 authentication, DES encryption
* to an Agent at demo.snmplabs.com:161
* setting some MIB objects to the new values

.. code-block:: bash

   snmpset.py -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 \
       demo.snmplabs.com \
       1.3.6.1.2.1.1.9.1.2.1 = 1.3.6.1.4.1.20408.1.1 \
       1.3.6.1.2.1.1.9.1.3.1 s "new system name"
