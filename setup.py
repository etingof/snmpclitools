#!/usr/bin/env python

from distutils.core import setup

setup(name="pysnmpap",
      version="0.0.1",
      description="A collection of SNMP applications written in Python",
      author="Ilya Etingof",
      author_email="ilya@glas.net ",
      url="http://sourceforge.net/projects/pysnmp/",
      packages = [ 'pysnmpap',
                   'pysnmpap.cli' ],
      data_files = [ ('/usr/local/bin', ['apps/pysnmpwalk']),
                     ('/usr/local/bin', ['apps/pysnmpbulkwalk']),
                     ('/usr/local/bin', ['apps/pysnmptrapd']), ],
      license="BSD"
      )
