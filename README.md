
Command-line SNMP tools
-----------------------

[![PyPI](https://img.shields.io/pypi/v/snmpclitools.svg?maxAge=2592000)](https://pypi.org/project/snmpclitools)
[![Python Versions](https://img.shields.io/pypi/pyversions/snmpclitools.svg)](https://pypi.org/project/snmpclitools/)
[![Build status](https://travis-ci.org/etingof/snmpclitools.svg?branch=master)](https://travis-ci.org/etingof/snmpclitools)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/etingof/snmpclitools/master/LICENSE.txt)

This is a collection of command-line SNMP tools written in pure-Python.
The tools mimic their famous [Net-SNMP](http://sourceforge.net/projects/net-snmp/)
counterparts.

In the past this project was known as *pysnmp-apps*.

Features
--------

* Complete SNMPv1/v2c and SNMPv3 support
* Interface compatible (almost) with Net-SNMP's snmp\* tools.
* SNMPv3 USM supports MD5/SHA/SHA224/SHA256/SHA384/SHA512 auth and
  DES/3DES/AES128/AES192/AES256 privacy crypto algorithms
* Automatically downloads required MIBs from the Internet
* Runs over IPv4 and/or IPv6 transports
* Cross-platform: works on Linux, Windows and OS X.
* 100% Python, works with Python 2.4 up to Python 3.7

Download
--------

The snmpclitools package is distributed under terms and conditions of 2-clause
BSD [license](http://snmplabs.com/snmpclitools/license.html). Source code is freely
available as a Github [repo](https://github.com/etingof/snmpclitools).

Installation
------------

Download snmpclitools from [PyPI](https://pypi.org/project/snmpclitools) or just run:

```bash
$ pip install snmpclitools
```

How to use the tools
--------------------

The most of pysnmp command-line tools could be run in a similar way as 
their Net-SNMP counterparts. For example:

```bash
$ snmpbulkwalk.py -v3 -u usr-md5-des -l authPriv -A authkey1 -X privkey1 demo.snmplabs.com system
SNMPv2-MIB::sysDescr.0 = DisplayString: Linux grommit 3.5.11.1 #2 PREEMPT Tue Mar 1 14:03:24 MSD 2016 i686 unknown unknown GNU/Linux
SNMPv2-MIB::sysObjectID.0 = ObjectIdentifier: iso.org.dod.internet.private.enterprises.8072.3.2.101.3.6.1.4.1.8072.3.2.10
SNMPv2-MIB::sysUpTime.0 = TimeTicks: 43 days 1:55:47.85372214785
[ skipped ]
SNMPv2-MIB::sysORUpTime."8" = TimeStamp: 0 days 0:0:0.77
SNMPv2-MIB::sysORUpTime."9" = TimeStamp: 0 days 0:0:0.77

$ snmpget.py -v3 -u usr-sha-aes -l authPriv -A authkey1 -X privkey1 demo.snmplabs.com IP-MIB::ipAdEntBcastAddr.\"127.0.0.1\"
IP-MIB::ipAdEntBcastAddr."127.0.0.1" = Integer32: 1

$ snmpset.py -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0 = my-new-descr
notWritable(17)
```

For more information, please, run any of these tools with `--help` option.

You can play with different security protocols against the publicly available SNMP
agent like [this one @snmplabs.com](http://snmplabs.com/snmpsim/public-snmp-agent-simulator.html).

Getting help
------------

If something does not work as expected, please open up a
[GitHub issue](https://github.com/etingof/snmpclitools/issues/new) or post
your question [to Stack Overflow](http://stackoverflow.com/questions/ask).

Feedback and collaboration
--------------------------

I'm interested in bug reports, fixes, suggestions and improvements. Your
pull requests are very welcome!

Copyright (c) 2005-2019, [Ilya Etingof](mailto:etingof@gmail.com). All rights reserved.

