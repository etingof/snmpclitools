
.. _snmptrap.py:

.. |SNMPTOOL| replace:: *snmptrap.py*

SNMP TRAP/INFORM
================

SNMP notifications provide a way for an SNMP agent to send an asynchronous
notification about conditions that the SNMP manager(s) might care about.
The notifications that particular SNMP agent can generate are typically
defined by the MIB(s) that agent supports.

The |SNMPTOOL| tool implements SNMP TRAP and INFORM notification originator.
TRAPs are typically produced by the SNMP agent.

The |SNMPTOOL| behavior is tightly aligned with its
Net-SNMP prototypes e.g. `snmptrap <http://www.net-snmp.org/docs/man/snmptrap.html>`_
and `snmpinform <http://www.net-snmp.org/docs/man/snmpinform.html>`_.

Command line syntax is as follows:

|SNMPTOOL| [:ref:`options <options>`] <:ref:`peer-address <snmptrap-peer-address>`> <:ref:`trap-parameters <snmptrap-params>`

Options always start with dash (-), other parameters are positional.

.. _options:

Options can be categorized by the part they are tackling e.g.

* :ref:`SNMP protocol <options-protocol>`
* :ref:`MIB modules <options-mibs>`
* :ref:`input <options-input>`/:ref:`output <options-output>` formatting
* :ref:`network I/O <options-network>`
* :ref:`SNMP TRAP/INFORM <options-snmptrap>` command specifics

Past these named options, mandatory positional parameters follow:

* :ref:`SNMP peer address <snmptrap-peer-address>`
* :ref:`SNMP TRAP parameters <snmptrap-params>`

.. include:: options-protocol-rst.inc

.. note::

   When SNMP TRAP is sent over authenticated/encrypted SNMP v3, SNMP engine
   discovery can not be performed. That implies that receiving SNMPv3 entity
   must have USM configuration tied to the *SNMPv3 engine ID* used by
   the |SNMPTOOL|.

.. include:: options-mib-rst.inc
.. include:: options-input-rst.inc
.. include:: options-output-rst.inc
.. include:: options-network-rst.inc
.. include:: options-debug-rst.inc

.. _options-snmptrap:

TRAP/INFORM options
-------------------

The following one-letter options following the *-C* option modify
the way how |SNMPTOOL| tool behaves. These options are mostly specific
to |SNMPTOOL|'s operation logic.

Use INFORM notification
+++++++++++++++++++++++

The *-Ci* option forces |SNMPTOOL| to use SNMP INFORM notification flavor
instead of SNMP TRAP one. The difference is that INFORM implies receiver
acknowledgement, while TRAP is always a one-way communication.

.. note::

   Historically, INFORM was not meant to be used for the same purpose as
   SNMP TRAP - its original purpose was to let SNMP entities exchanging
   some management informaiton they gathered on an ad-hoc, peer-to-peer
   basis.

.. _snmptrap-peer-address:

SNMP peer address
-----------------

The first positional parameter specifies SNMP peer address on the network
and, optionally, network protocol to use.

The network protocol can be either *udp* for UDP-over-IPv4 or *udp6* for
UDP-over-IPv6.

The network address is either IPv4 or IPv6 address or a fully qualified
domain name optionally followed by a colon-separated port number. The
default for port is 162.

.. _snmptrap-params:

.. _snmptrap-v1-params:

SNMPv1 TRAP parameters
----------------------

When SNMPv1 is used for sending TRAP, the following parameters should be
given to populate TRAP PDU:

|SNMPTOOL| :ref:`enterprise-oid <snmptrap-v1-enterprise-oid>` :ref:`agent <snmptrap-v1-agent-ip>` :ref:`generic-trap <snmptrap-v1-generic-trap>` :ref:`specific-trap <snmptrap-v1-specific-trap>` :ref:`uptime <snmptrap-v1-agent-uptime>` [:ref:`mib-object <snmptrap-mib-objects>` [...]]

.. note::

   SNMP v1 TRAP PDU is very different that
   :ref:`SNMP v2c/v3 TRAP PDU <snmptrap-v2c-params>`. The former
   has a number of fields designed specifically to hold TRAP data
   while the latter is unified with the rest of PDU types.

.. _snmptrap-v1-enterprise-oid:

Enterprise OID
++++++++++++++

SNMP TRAPs fall into two categories,
ref:`generic <snmptrap-v1-generic-trap>` and
ref:`enterprise-specific <snmptrap-v1-specific-trap>`. When
enterprise-specific TRAPs are used, the enterprise object identifier
is put into the packet for receiver to triage and understand the
agent-specific meaning of the event.

For example, for IANA-assigned enterprise number is 1248, the enterprise OID
is *1.3.6.1.4.1.1248*.

.. _snmptrap-v1-agent-ip:

SNNP agent IP
+++++++++++++

The TRAP PDU also carries the IPv4 address of the SNMP agent that produces
this notification. Depending on the network configuration, it may or may not
be the same as the source IPv4 address of the TRAP packet.

.. _snmptrap-v1-generic-trap:

Generic TRAP ID
+++++++++++++++

There are seven generic TRAP numbers (0-6) for various typical conditions
that may occur to pretty much any SNMP-managed system.

* coldStart
* warmStart
* linkDown
* linkUp
* authenticationFailure
* egpNeighborLoss
* enterpriseSpecific

The last, *enterpriseSpecific* is used when
:ref:`specific TRAP <snmptrap-v1-specific-trap>` is in effect.

.. _snmptrap-v1-specific-trap:

Specific TRAP ID
++++++++++++++++

Enterprise-specific TRAP is the way to extend the built-in generic events
in a vendor-specific manner. An enterprise-specific TRAP is identified by
two things: the :ref:`Enterprise OID <snmptrap-v1-enterprise-oid>`
of the company that defined the TRAP and a company-specific TRAP number
(just an integer).

.. _snmptrap-v1-agent-uptime:

SNMP agent uptime
+++++++++++++++++

SNMP TRAP requires an uptime value. Uptime is how long the system has been
running since boot.  With |SNMPTOOL|, this value is set to
either SNMP engine uptime which is likely zero.

When sending SNMP TRAP with |SNMPTOOL| you can choose whatever uptime
value best models the situation you are trying to produce.

The value is measured in hundreds of a second.

.. _snmptrap-v2c-params:

SNMPv2/SNMPv3 parameters
------------------------

When SNMPv2c or SNMPv3 is used for sending TRAP, the following parameters
should be given to populate TRAP2 PDU:

|SNMPTOOL| :ref:`uptime <snmptrap-v2c-agent-uptime>` :ref:`trap-oid <snmptrap-v2c-trap-oid>` [:ref:`mib-object <snmptrap-mib-objects>` [...]]

.. note::

   SNMP v2c/v3 TRAP PDU is very different that
   :ref:`SNMP v1 TRAP PDU <snmptrap-v1-params>`. The latter has a number of
   fields designed specifically to hold TRAP data, while the latter is
   unified with the rest of PDU types.

   The way how that unification is implemented is that all the TRAP-specific
   items are put into the variable-bindings. You still need to supply
   the mandatory items at the |SNMPTOOL|'s command line, the missing
   parameters get reasonable defaults.

.. _snmptrap-v2c-agent-uptime:

SNMP agent uptime
+++++++++++++++++

SNMPv2c/v3 TRAP PDU carries the uptime value in the first variable-binding
(e.g. *SNMPv2-MIB::sysUpTime.0*). With |SNMPTOOL|, this value is set to
either SNMP engine uptime which is likely zero.

When sending SNMP TRAP with |SNMPTOOL| you can choose whatever uptime
value best models the situation you are trying to produce.

The value is measured in hundreds of a second.

.. _snmptrap-v2c-trap-oid:

TRAP OID
++++++++

TRAP object identifier is always present in TRAP v2c PDU at the second
place of the variable-bindings (e.g. *SNMPv2-MIB::snmpTrapOID.0*). The
value part is either one of the *Generic TRAPs*:

* *SNMPv2-MIB::coldStart*
* *SNMPv2-MIB::warmStart*
* *IF-MIB::linkDown*
* *IF-MIB::linkUp*
* SNMPv2-MIB::authenticationFailure*

In case of a :ref:`Specific TRAP <snmptrap-v1-specific-trap>`, the
:ref:`Enterprise OID <snmptrap-v1-enterprise-oid>` should be passed
as a value.

The |SNMPTOOL| requires the *Enterprise TRAP* value to be specified
at the command line.

SNNP agent IP
+++++++++++++

The TRAP v2c/v3 PDU can optionally carry the IPv4 address of the SNMP agent
that produces this notification. Depending on the network configuration,
it may or may not be the same as the source IPv4 address of the TRAP
packet.

To pass SNMP agent IP to |SNMPTOOL|, you need to give it a variable-binding
with the OID of *SNMP-COMMUNITY-MIB::snmpTrapAddress.0* and value
of your choice.

.. _snmptrap-mib-objects:

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

SNMP TRAP examples
------------------

SNMPv1 TRAP example
+++++++++++++++++++

The following command will send SNMP v1 TRAP message:

* with community name 'public'
* with Generic Trap #1 (warmStart) and Specific Trap 0
* with default Uptime
* with default Agent Address
* with Enterprise OID 1.3.6.1.4.1.20408.4.1.1.2
* include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'

.. code-block:: bash

   snmptrap.py -v1 -c public demo.snmplabs.com 1.3.6.1.4.1.20408.4.1.1.2 \
       0.0.0.0 1 0 0 1.3.6.1.2.1.1.1.0 s "my system"

SNMPv2c TRAP example
++++++++++++++++++++

The following command will send SNMP v2c TRAP message:

* with community name 'public'
* with Agent uptime value 123
* with TRAP ID 'coldStart'
* include managed object information specified as var-bind objects pair

.. code-block:: bash

   snmptrap.py -v2c -c public demo.snmplabs.com 123 1.3.6.1.6.3.1.1.5.1 \
    SNMPv2-MIB::sysName.0 = "my system"

SNMPv3 TRAP example
+++++++++++++++++++

The following command will send SNMP v3 TRAP message:

* with authoritative snmpEngineId = 0x8000000001020304
  (USM at the receiving manager part must be configured accordingly)
* with user 'usr-sha-aes128', auth: SHA, priv: AES128
* with TRAP ID 'authenticationFailure'
* include managed object information specified as var-bind objects pair

.. code-block:: bash

   snmptrap.py -v3 -e 8000000001020304 -l authPriv -u usr-sha-aes \
   -A authkey1 -X privkey1 -a SHA -x AES demo.snmplabs.com 12345 \
       1.3.6.1.4.1.20408.4.1.1.2 SNMPv2-MIB::sysName.0 = "my system"

.. note::

   SNMPv3 TRAPs requires pre-sharing the Notification Originator's
   value of SnmpEngineId with Notification Receiver. To facilitate that
   we will use static (e.g. not autogenerated) version of snmpEngineId.
