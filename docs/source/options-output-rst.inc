
.. _options-output:

Output options
--------------

The following one-letter options following the *-O* option modify
|SNMPTOOL| tool's output.

Equal sign and type information
+++++++++++++++++++++++++++++++

The *-Oq* option removes the equal sign (=) and SNMP value type information
from the variable-binding being reported on stdout.

.. code-block:: bash

    $ snmpget.py -v2c -c public -Oq demo.snmplabs.com sysDescr.0
    SNMPv2-MIB::sysDescr.0 Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686
    $
    $ snmpget.py -v2c -c public demo.snmplabs.com sysDescr.0
    SNMPv2-MIB::sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

Type information
++++++++++++++++

The *-OQ* option removes the SNMP value type information from the
variable-binding being reported on stdout.

.. code-block:: bash

    $ snmpget.py -v2c -c public -OQ demo.snmplabs.com sysDescr.0
    SNMPv2-MIB::sysDescr.0 = Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686
    $
    $ snmpget.py -v2c -c public demo.snmplabs.com sysDescr.0
    SNMPv2-MIB::sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

Managed object path
+++++++++++++++++++

The *-Of* option prints out the full path of the managed object in the MIB
tree rather than MIB name and MIB object name (the default).

.. code-block:: bash

    $ snmpget.py -v2c -c public -Of demo.snmplabs.com sysDescr.0
    iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

Managed object name
+++++++++++++++++++

The *-Os* option prints out just managed object name (excluding MIB name)
rather than MIB name and MIB object name (the default).

.. code-block:: bash

    $ snmpget.py -v2c -c public -Os demo.snmplabs.com sysDescr.0
    sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

Raw OID
+++++++

The *-On* option prints out the raw object identifier (OID) rather than
human friendly MIB object name:

.. code-block:: bash

    $ snmpget.py -v2c -c public -On demo.snmplabs.com sysDescr.0
    1.3.6.1.2.1.1.1.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

Numeric enumerations
++++++++++++++++++++

The *-Oe* option disables symbolic labels rendering for the enumeration
values:

.. code-block:: bash

    $ snmpget.py -v2c -c public -On demo.snmplabs.com IF-MIB::ifAdminStatus.1
    1.3.6.1.2.1.2.2.1.7.1 = Integer32: 'up'
    $
    $ snmpget.py -v2c -c public -Oe demo.snmplabs.com IF-MIB::ifAdminStatus.1
    IF-MIB::ifAdminStatus."1" = Integer32: 1

Break down table index
++++++++++++++++++++++

The *-Ob* option disables interpreting SNMP table indices and renders just
raw OID instead:

.. code-block:: bash

    $ snmpget.py  -v2c -c public -Ob demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"
    TCP-MIB::tcpConnState.195.218.254.105.45632.10.105.41.179.3389 = Integer32: 'established'
    $
    $ snmpget.py  -v2c -c public demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"
    TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389" = Integer32: 'established'

Escape table index quotes
+++++++++++++++++++++++++

The *-OE* includes extra escaped quotes surrounding SNMP table index parts.
This can be useful when UNIX shell is in the processing pipeline.

.. code-block:: bash

    $ snmpget.py  -v2c -c public -OE  demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"
    TCP-MIB::tcpConnState.\"195.218.254.105\".\"45632\".\"10.105.41.179\".\"3389\" = Integer32: 'established'

Brackets around table indices
+++++++++++++++++++++++++++++

The *-OX* option surrounds SNMP table index parts with square brackets
instead of quotes (default):

.. code-block:: bash

    $ snmpget.py  -v2c -c public -OX  demo.snmplabs.com TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"
    TCP-MIB::tcpConnState.[195.218.254.105].[45632].[10.105.41.179].[3389] = Integer32: 'established'

Hexified values
+++++++++++++++

The *-OT* option ensures that rendered values are always in hex:

.. code-block:: bash

    $ snmpget.py -v2c -c public -OT demo.snmplabs.com sysName.0
    SNMPv2-MIB::sysName.0 = DisplayString: 6e 65 77 20 73 79 73 74 65 6d 20 6e 61 6d 65
    $
    $ snmpget.py -v2c -c public demo.snmplabs.com sysName.0
    SNMPv2-MIB::sysName.0 = DisplayString: new system name

Rendering just values
+++++++++++++++++++++

The *-Ov* option removes managed object name from the rendered output:

.. code-block:: bash

    $ snmpget.py -v2c -c public -Ov demo.snmplabs.com sysName.0
    DisplayString: new system name

Units rendering
+++++++++++++++

The *-OU* option disables units rendering:

.. code-block:: bash

    $ snmpget.py -v2c -c public demo.snmplabs.com TCP-MIB::tcpRtoMin.0
    TCP-MIB::tcpRtoMin.0 = Integer32: 200 milliseconds
    $
    $ snmpget.py -v2c -c public -OU  demo.snmplabs.com TCP-MIB::tcpRtoMin.0
    TCP-MIB::tcpRtoMin.0 = Integer32: 200

Raw timeticks
+++++++++++++

The *-Ot* option disables *TimeTicks* values interpretation so that
raw values get rendered:

.. code-block:: bash

    $ snmpget.py -v2c -c public -Ot demo.snmplabs.com SNMPv2-MIB::sysORLastChange.0
    SNMPv2-MIB::sysORLastChange.0 = TimeStamp: 143145968
    $
    $ snmpget.py -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysORLastChange.0
    SNMPv2-MIB::sysORLastChange.0 = TimeStamp: 16 days 13:37:44.82
