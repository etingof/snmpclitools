
.. _snmptranslate.py:

.. |SNMPTOOL| replace:: *snmptranslate.py*

MIB lookup tool
===============

The |SNMPTOOL| tool can look up MIB object information at MIB by OID or
vice versa. This tool does not require a SNMP agent to operate -- it just
loads up MIB module(s) and performs the requested lookup.

Its usage is tightly aligned with its
`Net-SNMP prototype <http://www.net-snmp.org/docs/man/snmptranslate.html>`_.

Command line syntax is as follows:

|SNMPTOOL| [:ref:`options <options>`] <:ref:`mib-object <snmptranslate-mib-objects>` [:ref:`mib-object <snmptranslate-mib-objects>` [...]]>

Options always start with dash (-), other parameters are positional.

.. _options:

Options can be categorized by the part they are tackling e.g.

* :ref:`MIB modules <options-mibs>`
* :ref:`input <options-input>`/:ref:`output <options-output>` formatting

Past these named options, mandatory positional parameters follow:

* :ref:`MIB object(s) to look up <snmptranslate-mib-objects>`

.. include:: options-mib-rst.inc
.. include:: options-input-rst.inc
.. include:: options-output-rst.inc
.. include:: options-debug-rst.inc

.. _snmptranslate-mib-objects:

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

    $ snmptranslate.py TCP-MIB::tcpRtoMin.0
    TCP-MIB::tcpRtoMin.0
    $
    $ snmptranslate.py 1.3.6.1.2.1.6.2.0
    SNMPv2-SMI::mib-2.6.2.0
    $
    $ snmptranslate.py -m TCP-MIB 1.3.6.1.2.1.6.2.0
    TCP-MIB::tcpRtoMin.0
    $
    $ snmptranslate.py TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"
    TCP-MIB::tcpConnState."195.218.254.105"."45632"."10.105.41.179"."3389"

If only MIB name is given, the first MIB object in that MIB will be taken
as object name:

.. code-block:: bash

    $ snmptranslate.py TCP-MIB::
    TCP-MIB::tcp

You can look up many MIB objects by specifying them all at the command line:

.. code-block:: bash

    $ snmptranslate.py -On SNMPv2-MIB::sysName.0 SNMPv2-MIB::sysLocation.0
    1.3.6.1.2.1.1.5.0
    1.3.6.1.2.1.1.6.0
