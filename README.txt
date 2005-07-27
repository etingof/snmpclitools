
PySNMP command-line tools
-------------------------

Here is a set of SNMP applications written on top of the PySNMP package
(http://sourceforge.net/projects/pysnmp/). Some of these tools mimic
their famous Net-SNMP (http://sourceforge.net/projects/net-snmp/)
counterparts, while others are designed toward easy integration with
other Python applications.

PySNMP command-line tools are written entirely in Python and only rely 
upon PySNMP package to run (PySNMP requires other Python packages). For
MIB resolution services to work for popular MIBs, pysnmp-mibs package
should be installed as well.

These tools have been tested on Linux & Windows XP, though, they might work
on any Python-populated system.

The whole package is distributed under terms and conditions of BSD-style 
license. See the LICENSE file for details.

INSTALLATION
------------

The pysnmp-apps package is fully distutil'ed, so just type

$ python setup.py install

to install the whole thing.

PySNMP version 4.1.x or later is required to run these tools.

OPERATION
---------

The most of PySNMP command-line tools could be run in a similar way as 
their Net-SNMP counterparts. For example:

$ pysnmpbulkwalk -v3 -u myuser -l authPriv -A myauthkey -X myprivkey localhost system
SNMPv2-MIB::sysDescr.0 = DisplayString: Linux cray.glas.net 2.4.20-13.8 #1 Mon May 12 12:20:54 EDT 2003 i686
SNMPv2-MIB::sysObjectID.0 = ObjectIdentifier: iso.org.dod.internet.private.enterprises.8072.3.2.101.3.6.1.4.1.8072.3.2.10
SNMPv2-MIB::sysUpTime.0 = SysUpTime: 43 days 1:55:47.85372214785
^C

$ pysnmpget -v3 -u myuser -l authPriv -A myauthkey -X myprivkey localhost IP-MIB::ipAdEntBcastAddr.\"127.0.0.1\"
IP-MIB::ipAdEntBcastAddr."127.0.0.1" = Integer32: 1

$ pysnmpset -v2c -c public localhost SNMPv2-MIB::sysDescr.0 = my-new-descr
notWritable(17)

For more information, please, run any of these tools with --help option.

GETTING HELP
------------

Try PySNMP mailing list at http://sourceforge.net/mail/?group_id=14735

=-=-=
mailto: ilya@glas.net
