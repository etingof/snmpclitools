#!/usr/bin/env python

from distutils.core import setup

setup(name="pysnmp-apps",
      version="0.1.0-alpha-0",
      description="A collection of SNMP applications written in Python",
      author="Ilya Etingof",
      author_email="ilya@glas.net ",
      url="http://sourceforge.net/projects/pysnmp/",
      packages = [ 'pysnmp_apps', 'pysnmp_apps.cli' ],
      scripts = [ 'apps/pysnmpwalk' ],
      license="BSD")
