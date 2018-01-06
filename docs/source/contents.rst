
Command-line SNMP tools
=======================

.. toctree::
   :maxdepth: 2

This is the collection of command-line SNMP tools written in
pure-Python and tightly aligned with the de-facto standard
SNMP tools that come with Net-SNMP e.g. *snmpget*, *snmpwalk* and
many others.

In most cases, you should be able to alternate between Net-SNMP
tools and the tools provided by this project without changing
much at the command line.

The goals of this project is to bring SNMP tooling to a wider range
of computing platforms and ease introducing new SNMP features
by leveraging the high-level programming language.

These SNMP tools are free and open-source. Source code is hosted in
a `GitHub repo <https://github.com/etingof/pysnmp-apps>`_ and
distributed under 2-clause BSD-style license.

Quick start
-----------

If you understand SNMP and have some experience with the Net-SNMP tool set,
you do not need to learn much. Just install *pysnmp-apps* and run the
*.py*-suffixed version of the SNMP tool you want.

.. code-block:: bash

   $ snmpget -v2c -c public demo.snmplabs.com sysDescr.0
   SNMPv2-MIB::sysDescr.0 = STRING: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686
   $
   $ snmpget.py -v2c -c public demo.snmplabs.com sysDescr.0
   SNMPv2-MIB::sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

Here and later throughout the examples we will be using the
`public instance <http://snmplabs.com/snmpsim/public-snmp-agent-simulator.html>`_
of `SNMP agent simulator <http://snmplabs.com/snmpsim/>`_ at *demo.snmplabs.com*.
You are welcome to use it as well. ;-)

All SNMP versions are indeed supported including version 3.

.. code-block:: bash

   $ snmpget -v3 -u usr-md5-des -l authPriv \
       -A authkey1 -X privkey1  demo.snmplabs.com sysDescr.0
   SNMPv2-MIB::sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686
   $
   $ snmpget.py -v3 -u usr-md5-des -l authPriv \
       -A authkey1 -X privkey1  demo.snmplabs.com sysDescr.0
   SNMPv2-MIB::sysDescr.0 = DisplayString: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686

.. note::

   The SNMP tools support many strong encryption algorithms that have been
   introduced to SNMP at the later stages of the standards development.

SNMP employs MIB files to describe the structure of the system being managed
from the management perspective. Typically, each SNMP-enabled system implements
some of the well-known MIBs (such as `SNMPv2-MIB <http://mibs.snmplabs.com/asn1/SNMPv2-MIB>`_)
along with some vendor-specific MIBs.

With SNMP tools you can pass MIB module name together with the SNMP object
you want to manage. By default, the tool will try to pull required SNMP MIB by
name from `this large MIB repository <http://mibs.snmplabs.com/asn1/>`_, compile
the MIB and use the information it contains for building SNMP query.

For example, the *snmpget.py* tool in the snippet below will pull
`IF-MIB <http://mibs.snmplabs.com/asn1/IF-MIB>`_ file, parse it to
find the object ID of the *ifNumber* object, build and send proper
SNMP query:

.. code-block:: bash

   $ snmpget.py -v3 -u usr-md5-des -l authPriv \
       -A authkey1 -X privkey1  demo.snmplabs.com IF-MIB::ifNumber.0
   IF-MIB::ifNumber.0 = Integer32: 2

More information on the supported options can be looked up at the
documentation.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   snmpget.py </snmpget>
   snmpset.py </snmpset>
   snmpwalk.py </snmpwalk>
   snmpbulkwalk.py </snmpbulkwalk>
   snmptrap.py </snmptrap>
   snmptranslate.py </snmptranslate>

Download
--------

Best way is usually to

.. code-block:: bash

   # pip install pysnmp-apps
   
If that does not work for you for some reason, you might need to read the 
following page.

.. toctree::
   :maxdepth: 2

   /download

Changes
-------

.. toctree::
   :maxdepth: 2

   /changelog

License
-------

.. toctree::
   :maxdepth: 2

   /license

Contact
-------

In case of questions or issues using these SNMP tools, please open up an
`issue <https://github.com/etingof/pysnmp-apps/issues>`_ at GitHub.
Or just fix it and send us a pull request. ;-)
