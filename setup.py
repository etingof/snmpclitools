#!/usr/bin/env python

from distutils.core import setup

setup(name="pysnmp-apps",
      version="0.1.0a",
      description="A collection of SNMP applications written in Python",
      author="Ilya Etingof",
      author_email="ilya@glas.net ",
      url="http://sourceforge.net/projects/pysnmp/",
      packages = [ 'pysnmp_apps', 'pysnmp_apps.v4',
                   'pysnmp_apps.v4.cli' ],
      scripts = [ 'tools/pysnmpwalk' ],
      license="BSD")
