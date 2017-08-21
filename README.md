#pyjseisio

This project attempts to enable JavaSeis IO capability in Python by providing SWIG wrappers for the C++ [JSeisIO JavaSeis library](http://jseisio.com/). 

##Status
Just enough of a SWIG interface has been written to allow basic reading of JavaSeis files. This includes opening a file and collecting metadata (extents, axis definitions, header words, etc), and reading single frames, both trace amplitudes and headers. Trace data and headers are returned as NumPy `ndarray` data.

##Dependencies
* NumPy
* JSeisIO
* cmake (for JSeisIO)
* SWIG

##For some Linux distributions, this might be convenient (especially when you do not deal with any cross-platform compiling):
```shell
sudo ln -s /usr/local/lib /usr/local/lib64
sudo echo /usr/local/lib > /etc/ld.so.conf.d/libc.conf
sudo ldconfig
```

##Building JSeisIO

The modified JSeisIO library can be downloaded at https://github.com/seisowl/jseisio. It can be built and installed (on Linux) by:
```shell
cd jseisio
cmake src -DBUILD_SHARED_LIBS=TRUE
make
sudo make install
```

##Installation
If you have JSeisIO and NumPy (and SWIG) installed, then it should be as easy as running:
```shell
sudo python setup.py install
```
If JSeisIO is installed in a non-path location, then you should set the `library_dirs` command in `setup.cfg`, and if you don't want to set `LD_LIBRARY_PATH`, then you should also set `rpath`.

##API Examples
Jupyter notebooks are available in the `demo/` directory which demonstrate use of `pyjseisio`:
* [Basic reading](./demo/basic.ipynb)

Here is the super quick, condensed version of how to get started reading JavaSeis data:
```python
import numpy as np
import pyjseisio as js

dataset = js.open("../test/synth.js")   # open the given JavaSeis file for reading
frame = dataset.readFrame(0)            # read trace data from frame 0
```

For convenience, calls to the wrapped C++ methods are made through the `jsdataset` class, which will hopefully hide all the interaction with SWIG/C++ types and let the user deal with purely python data.

Header words are packed into a `hdrs` dictionary for easier use:

```python
dataset.hdrs.keys()                      # returns a list of all header names
dataset.hdrs['OFFSET']                   # returns a catalogedHdrEntry object for the header OFFSET
dataset.hdrs['OFFSET'].getDescription()  # returns the description string for the header OFFSET

hdrBuf = dataset.readFrameHeader(0)      # read the header buffer from frame 0
dataset.hdrs['OFFSET'].getVal(hdrBuf[0]) # returns the value of the OFFSET header for trace 0
```

##TODO
* Finish implementing methods from jsFileReader
* More convenience methods? Maybe get array of values for one header from headerFrameBuffer?
* Fix JS_BYTORDER
* Start on jsFileWriter
* geometry?
* Can I use installed JSeisIO headers (in an include dir) instead of providing those files myself?
* Should I use setuptools instead of distutils?
