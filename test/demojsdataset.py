import numpy as np
import pyjseisio as js

dataset = js.open("./synth.js")

iframe = 2
fh = dataset.readFrameHeader(iframe, liveOnly=True)
frame = dataset.readFrame(iframe, readHdrs=False, liveOnly=True)
frame[:] = 200
dataset.writeFrame(iframe, frame, fh, fh.shape[0])
dataset.writeFrameToFile("./dataAs.js", iframe, frame, fh, fh.shape[0])

iframe = 3
frame[:] = 300
dataset.writeFrame(iframe, frame, fh, fh.shape[0])
dataset.writeFrameToFile("./dataAs.js", iframe, frame, fh, fh.shape[0])

# read to validate
datasetAs = js.open("./dataAs.js")
iframe = 3
fhnew = datasetAs.readFrameHeader(iframe, liveOnly=True)
framenew = datasetAs.readFrame(iframe, readHdrs=False, liveOnly=True)

if np.array_equal(framenew,frame) :
    print ("Write check ok")
else :
    print ("Write check error")


#for ir in xrange(fh.shape[0]):
#    print dataset.hdrs['PAD_TRC'].getVal(fh[ir]), dataset.hdrs['TR_FOLD'].getVal(fh[ir])
#, dataset.hdrs['SHOT_2D'].getVal(fh[ir])

#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset.hdrs['XLINE_NO']))
#print usefulStuff

#####################################################################
#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset.axes[1]))
#print usefulStuff

#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(jsswig))
#print usefulStuff

#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(fr))
#print usefulStuff

#fr.getAxisLabels



