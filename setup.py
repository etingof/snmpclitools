#!/usr/bin/env python
"""SNMP command-line tools

   A collection of command-line tools for SNMP management purposes built
   on top of PySNMP package.
"""
import sys

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Information Technology
Intended Audience :: System Administrators
Intended Audience :: Telecommunications Industry
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Communications
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Monitoring
Topic :: System :: Networking :: Monitoring
Topic :: Software Development :: Libraries :: Python Modules
"""

def howto_install_setuptools():
    print("""
   Error: You need setuptools Python package!

   It's very easy to install it, just type (as root on Linux):

   wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
   python ez_setup.py

   Then you could make eggs from this package.
""")

if sys.version_info[:2] < (2, 4):
    print("ERROR: this package requires Python 2.4 or later!")
    sys.exit(1)

try:
    from setuptools import setup
    params = {
        'install_requires': [ 'pysnmp>=4.3.0' ],
        'zip_safe': True
        }
except ImportError:
    for arg in sys.argv:
        if 'egg' in arg:
            howto_install_setuptools()
            sys.exit(1)
    from distutils.core import setup
    params = {}
    if sys.version_info[:2] > (2, 4):
        params['requires'] = [ 'pysnmp(>=4.3.0)' ]

doclines = [ x.strip() for x in __doc__.split('\n') if x ]

params.update( {
    'name': 'pysnmp-apps',
    'version': open('pysnmp_apps/__init__.py').read().split('\'')[1],
    'description': doclines[0],
    'long_description': ' '.join(doclines[1:]),
    'maintainer': 'Ilya Etingof <ilya@glas.net>',
    'author': 'Ilya Etingof',
    'author_email': 'ilya@glas.net',
    'url': 'http://sourceforge.net/projects/pysnmp/',
    'classifiers': [ x for x in classifiers.split('\n') if x ],
    'platforms': ['any'],
    'license': 'BSD',
    'packages': [ 'pysnmp_apps', 'pysnmp_apps.cli' ],
    'scripts': [ 'scripts/snmpget.py', 'scripts/snmpset.py',
                 'scripts/snmpwalk.py', 'scripts/snmpbulkwalk.py',
                 'scripts/snmptrap.py', 'scripts/snmptranslate.py' ]
  } )

if "py2exe" in sys.argv:
    import py2exe
    # fix executables
    params['console'] = params['scripts']
    del params['scripts']
    # add files not found my modulefinder
    params['options'] = {
        'py2exe': {
            'includes': [
                'pysnmp.smi.mibs.*',
                'pysnmp.smi.mibs.instances.*'
            ],
            'bundle_files': 1,
            'compressed': True
        }
    }

    params['zipfile'] = None

    print("!!! Make sure your pysnmp/pyasn1 packages are NOT .egg'ed!!!")

setup(**params)
