
SNMP applications for Python
----------------------------

Here is a bunch of SNMP tools written on top of the PySNMP package
(http://sourceforge.net/projects/pysnmp/). Some of these tools mimic
their famous Net-SNMP (http://sourceforge.net/projects/net-snmp/)
counterparts, while others are designed toward easy integration with
other Python applications.

PySNMPApps is written entirely in Python and only relies upon the PySNMP
package to run.

The PySNMPApps package is distributed under terms and conditions of BSD-style
license. See the LICENSE file for details.

FEATURES
--------

* Net-SNMP style snmpwalk/snmpget command-line tools
* SNMP agent framework suitable for easy integration with user apps
* 100% Python, works with Python 1.x and later

MISFEATURES
-----------

* No MIB parser
* No SNMP v.3 support

INSTALLATION
------------

The PySNMPApps package is fully distutil'ed, so just type

$ python setup.py install

to install the whole thing.

GETTING HELP
------------

Try PySNMP mailing list at http://sourceforge.net/mail/?group_id=14735

=-=-=
mailto: ilya@glas.net
