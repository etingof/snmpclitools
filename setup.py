#!/usr/bin/env python
import sys

def howto_install_setuptools():
    print("""Error: You need setuptools Python package!

It's very easy to install it, just type (as root on Linux):
   wget http://peak.telecommunity.com/dist/ez_setup.py
   python ez_setup.py
""")

try:
    from setuptools import setup
    params = {
        'install_requires': [ 'pysnmp>=4.2.2' ],
        'zip_safe': True
        }
except ImportError:
    for arg in sys.argv:
        if arg.find('egg') != -1:
            howto_install_setuptools()
            sys.exit(1)
    from distutils.core import setup
    params = {}
    if sys.version_info[:2] > (2, 4):
        params['requires'] = [ 'pysnmp(>=4.2.2)' ]

params.update( {
    'name': 'pysnmp-apps',
    'version': '0.3.2',
    'description': 'PySNMP applications',
    'author': 'Ilya Etingof',
    'author_email': 'ilya@glas.net',
    'url': 'http://sourceforge.net/projects/pysnmp/',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: BSD License'
        ],
    'license': 'BSD',
    'packages': [ 'pysnmp_apps', 'pysnmp_apps.cli' ],
    'scripts': [ 'tools/pysnmpget', 'tools/pysnmpset',
                 'tools/pysnmpwalk', 'tools/pysnmpbulkwalk',
                 'tools/pysnmptrap', 'tools/pysnmptranslate' ]
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
                ]
            }
        }

setup(**params)
