#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension
import imp

pyjseisio_module = Extension('_pyjseisio',
                           sources=['pyjseisio.i'],
                           library_dirs=['/data/esdrd/eyms/python/pyjseisio/jseisIO'],
                           libraries=['jseisIO'],
                           swig_opts=['-c++']
                           )

setup (name = 'pyjseisio',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig example from docs""",
       ext_modules = [pyjseisio_module],
       py_modules = ["pyjseisio"],
       )
