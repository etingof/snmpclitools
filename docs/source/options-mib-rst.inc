
MIB options
-----------

Pre-load MIBs
+++++++++++++

You may want to pre-load some of the MIB modules to let the |SNMPTOOL| tool
rendering SNMP responses in a more meaningful way.

The *-m* option specifies a colon separated list of MIB modules (not files)
to load. The |SNMPTOOL| tool will first try to find pre-compiled pysnmp MIB
files (by default in *~/.pysnmp/mibs* in UNIX), then try to find required
ASN.1 MIB file on local filesystem or on Web (by default it will look it up
at *http://mibs.snmplabs.com/asn1/*). If ASN.1 MIB file is found, it will be
compiled into pysnmp form and cached for future use.

The special keyword ALL is used to load all pre-compiled pysnmp MIB modules
in the MIB directory search list.

MIB files search path
+++++++++++++++++++++

The *-M* option specifies a colon separated list of local directories and/or
URLs pointing to remote HTTP/FTP servers where to search for MIBs.

.. note::

   Default MIB search path is *http://mibs.snmplabs.com/asn1/*
