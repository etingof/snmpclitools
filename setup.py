#!/usr/bin/env python

from distutils.core import setup

setup(name="pysnmp-apps",
      version="0.0.2",
      description="A collection of SNMP applications written in Python",
      author="Ilya Etingof",
      author_email="ilya@glas.net ",
      url="http://sourceforge.net/projects/pysnmp/",
      packages = [ 'pysnmpap',
                   'pysnmpap.cli',
                   'pysnmpap.cli.ucd',
                   'pysnmpap.cli.ucd.proto',                   
                   'pysnmpap.cli.ucd.carrier',
                   'pysnmpap.cli.ucd.carrier.udp' ],
      scripts = [ 'apps/pysnmpget', 'apps/pysnmpset',
                  'apps/pysnmpwalk', 'apps/pysnmpbulkwalk',
                  'apps/pysnmptrap', 'apps/pysnmptrapd' ],
      license="BSD")
