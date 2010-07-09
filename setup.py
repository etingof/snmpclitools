#!/usr/bin/env python
import sys
import string

def howto_install_setuptools():
    print """Error: You need setuptools Python package!

It's very easy to install it, just type (as root on Linux):
   wget http://peak.telecommunity.com/dist/ez_setup.py
   python ez_setup.py
"""

try:
    from setuptools import setup
except ImportError:
    for arg in sys.argv:
        if string.find(arg, 'egg') != -1:
            howto_install_setuptools()
            sys.exit(1)
    from distutils.core import setup

options = {
    'name': 'pysnmp-apps',
    'version': '0.2.10a',
    'description': 'PySNMP applications',
    'author': 'Ilya Etingof',
    'author_email': 'ilya@glas.net',
    'url': 'http://sourceforge.net/projects/pysnmp/',
    'license': 'BSD',
    'requires': 'pysnmp',
    'packages': [ 'pysnmp_apps', 'pysnmp_apps.cli' ],
    'scripts': [ 'tools/pysnmpget', 'tools/pysnmpset',
                 'tools/pysnmpwalk', 'tools/pysnmpbulkwalk',
                 'tools/pysnmptranslate' ]
  }

if "py2exe" in sys.argv:
    import py2exe
    # fix executables
    options['console'] = options['scripts']
    del options['scripts']
    # add files not found my modulefinder
    options['options'] = {
        'py2exe': {
            'includes': [
                'pysnmp.smi.mibs.*',
                'pysnmp.smi.mibs.instances.*'
                ]
            }
        }

apply(setup, (), options)
