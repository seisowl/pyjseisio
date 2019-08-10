import numpy as np
import pyjseisio as js
import matplotlib.pyplot as p
import pyjseisio.pyjseisio_swig as jsswig


# testing the SWIGGED methods of jsFileReader on the test dataset synth.js
fr = jsswig.jsFileReader()

# %matplotlib inline


usefulStuff = filter((lambda s: s[0:2]!='__'),dir(js))
print usefulStuff

dataset = js.open("../test/synth.js")
usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset))
print usefulStuff

iframe = 2
fh = dataset.readFrameHeader(iframe, liveOnly=True)
frame = dataset.readFrame(iframe, readHdrs=False, liveOnly=True)

for ir in xrange(fh.shape[0]):
    print dataset.hdrs['PAD_TRC'].getVal(fh[ir]), dataset.hdrs['TR_FOLD'].getVal(fh[ir])
#, dataset.hdrs['SHOT_2D'].getVal(fh[ir])

usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset.hdrs['XLINE_NO']))
print usefulStuff

#####################################################################
usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset.axes[1]))
print usefulStuff

usefulStuff = filter((lambda s: s[0:2]!='__'),dir(jsswig))
print usefulStuff

usefulStuff = filter((lambda s: s[0:2]!='__'),dir(fr))
print usefulStuff

fr.getAxisLabels



