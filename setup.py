#!/usr/bin/env python

from distutils.core import setup

setup(name="pysnmp-apps",
      version="0.2.4a",
      description="PySNMP applications",
      author="Ilya Etingof",
      author_email="ilya@glas.net ",
      url="http://sourceforge.net/projects/pysnmp/",
      packages = [ 'pysnmp_apps', 'pysnmp_apps.v4',
                   'pysnmp_apps.v4.cli' ],
      scripts = [ 'tools/pysnmpget', 'tools/pysnmpset',
                  'tools/pysnmpwalk', 'tools/pysnmpbulkwalk' ],
      license="BSD")
