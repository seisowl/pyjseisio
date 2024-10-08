#!/usr/bin/env python

"""
setup.py file for pyjseisIO
"""

from setuptools import setup, Extension
#import imp
import numpy
from distutils.command.build import build as _build

#Define custom build order, so that the python interface module
#created by SWIG is staged in build_py.
class build(_build):
    # different order: build_ext *before* build_py
    sub_commands = [('build_ext',     _build.has_ext_modules),
                    ('build_py',      _build.has_pure_modules),
                    ('build_clib',    _build.has_c_libraries),
                    ('build_scripts', _build.has_scripts),
                   ]


pyjseisio_module = Extension('_pyjseisio_swig',
                           sources=['pyjseisio/pyjseisio.i'],
                           library_dirs=['../jseisIO'],
                           libraries=['jseisIO'],
                           swig_opts=['-c++']
                           )

setup (name = 'pyjseisio',
       version = '0.11',
       author      = "SWIG Docs",
       description = """Wrapped jseisIO library for Python""",
       ext_package = 'pyjseisio',
       ext_modules = [pyjseisio_module],
       include_dirs=[numpy.get_include()],
       packages = ["pyjseisio"],
       cmdclass = {'build': build }
       )
