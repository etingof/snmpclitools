
.. _snmpbulkwalk.py:

.. |SNMPTOOL| replace:: *snmpbulkwalk.py*

SNMP GETBULK command
====================

The |SNMPTOOL| tool implements SNMP GETBULK command generator. Its usage
is tightly aligned with its
`Net-SNMP prototype <http://www.net-snmp.org/docs/man/snmpbulkwalk.html>`_.

.. note::

    The *GETBULK* command is similar to the *GETNEXT* command but optimized for
    high throughput - SNMP agent can stuff many MIB objects into a single
    response to the GETBULK command.

Command line syntax is as follows:

|SNMPTOOL| [:ref:`options <options>`] <:ref:`peer-address <snmpbulkwalk-peer-address>`> <:ref:`mib-object <snmpbulkwalk-mib-objects>` [:ref:`mib-object <snmpbulkwalk-mib-objects>` [...]]>

Options always start with dash (-), other parameters are positional.

.. _options:

Options can be categorized by the part they are tackling e.g.

* :ref:`SNMP protocol <options-protocol>`
* :ref:`MIB modules <options-mibs>`
* :ref:`input <options-input>`/:ref:`output <options-output>` formatting
* :ref:`network I/O <options-network>`
* :ref:`SNMP GETBULK <options-getbulk>` command specifics

Past these named options, mandatory positional parameters follow:

* :ref:`SNMP peer address <snmpbulkwalk-peer-address>`
* :ref:`MIB object(s) to work on <snmpbulkwalk-mib-objects>`

.. include:: options-protocol-rst.inc
.. include:: options-mib-rst.inc
.. include:: options-input-rst.inc
.. include:: options-output-rst.inc
.. include:: options-network-rst.inc

.. _options-getbulk:

GETBULK options
---------------

The following one-letter options following the *-C* option modify
the way how |SNMPTOOL| tool behaves. These options are mostly specific
to |SNMPTOOL|'s operation logic.

Non-repeating MIB objects
+++++++++++++++++++++++++

The *-Cn<NUM>* option indicates how many of the leading MIB objects given
at the command line should be processed in the same way as *GETNEXT*
does it e.g. returning just one MIB object following the given one.

The default for *non-repeaters* is 0.

MIB objects max-repetitions
+++++++++++++++++++++++++++

The *-Cr<NUM>* option indicates the maximum count of MIB objects to be
returned in response for each of the repeating objects given on the
command line. The repeating objects are those that follow the
leading *non-repeating* objects.

The default for *max-repetitions* is 25.

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

.. _snmpbulkwalk-peer-address:

SNMP peer address
-----------------

The first positional parameter specifies SNMP peer address on the network
and, optionally, network protocol to use.

The network protocol can be either *udp* for UDP-over-IPv4 or *udp6* for
UDP-over-IPv6.

The network address is either IPv4 or IPv6 address or a fully qualified
domain name optionally followed by a colon-separated port number. The
default for port is 161.

.. _snmpbulkwalk-mib-objects:

MIB objects specification
-------------------------

The rest of positional parameters specify SNMP managed objects to walk by.
Each object can be either:

* *[MIB-name::]object-name[.index[.index]...]*
* *MIB-name*
* *object-identifier*

.. note::

   The MIB object(s) specified are interpreted as a starting point for
   "walking" the SNMP agent. The SNMP agent will return zero or more *next*
   objects past the one you've asked for.

When MIB name or object-name is referenced, the |SNMPTOOL| tool will try to
locate and load the corresponding MIB module. The OID specification does not
require MIB access.

.. code-block:: bash

    $ snmpbulkwalk.py -v2c -c public demo.snmplabs.com TCP-MIB::tcpRtoMin
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    $
    $ snmpbulkwalk.py -v2c -c public demo.snmplabs.com 1.3.6.1.2.1.6.2
    1.3.6.1.2.1.6.2.0 = Integer32: 200 milliseconds
    $
    $ snmpbulkwalk.py  -v2c -c public demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"
    TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389" = Integer32: 'established'

If only MIB name is given, the first MIB object in that MIB will be taken
as object name

.. code-block:: bash

    $ snmpbulkwalk.py -v2c -c public demo.snmplabs.com TCP-MIB::
    TCP-MIB::tcpRtoAlgorithm.0 = Integer32: 'other'
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    ...

You can query many MIB objects by a single SNMP GETBULK request by specifying
them all at the command line.

.. code-block:: bash

    $ snmpbulkwalk.py  -v2c -c public demo.snmplabs.com TCP-MIB:: IF-MIB::
    TCP-MIB::tcpRtoAlgorithm.0 = Integer32: 'other'
    IF-MIB::ifNumber.0 = Integer32: 2
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    IF-MIB::ifIndex."1" = InterfaceIndex: 1
    ...

The output MIB objects count is guaranteed to be a multiple of the requested
MIB objects times the maximum number of response MIB objects for any of the
request MIB objects that peer SNMP agent is able to serve.
