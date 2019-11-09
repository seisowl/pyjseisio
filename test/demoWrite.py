import numpy as np
import pyjseisio.pyjseisio_swig as jsswig

numDim = 4
NSamples = 501
NOffsets =  197
NXlines =   7
NInlines =  10
off0 = 0.0
doff = 100.0
xl0 = 10
dxl = 20
inl0 = 20
dinl = 40

# testing the SWIGGED methods of jsFileWriter on the test data to create a new dataset

jsWrtTest = jsswig.jsFileWriter()
jsWrtTest.setFileName("./dataTest.js")
jsWrtTest.initGridDim(numDim)
jsWrtTest.initGridAxis(0, "TIME", "SECONDS","TIME", NSamples, 0, 1, 0, 4)
jsWrtTest.initGridAxis(1, "OFFSET_BIN", "METERS", "SPACE", NOffsets, 0, 1, off0, doff)
jsWrtTest.initGridAxis(2, "CROSSLINE", "METERS", "SPACE", NXlines, 0, 1, xl0, dxl)
jsWrtTest.initGridAxis(3, "INLINE", "METERS", "SPACE", NInlines, 0, 1, inl0, dinl)
jsWrtTest.addProperty("NEW_HDR", "Header description", "INTEGER", 1)
jsWrtTest.addSurveyGeom(inl0,inl0 + (NInlines-1)*dinl,xl0, xl0 + (NXlines-1)*dxl,5.5,6.6,7.7,8.8,9.9,10.10)
jsWrtTest.addCustomProperty("Stacked", "boolean", "false")

jsWrtTest.writeMetaData()

itrcTypeHdr = jsWrtTest.getHdrEntry("TRC_TYPE")
iTimeHdr = jsWrtTest.getHdrEntry("TIME")
fOffsetHdr = jsWrtTest.getHdrEntry("OFFSET")
iOffsetBinHdr = jsWrtTest.getHdrEntry("OFB_NO")
dCdpXHdr = jsWrtTest.getHdrEntry("CDP_XD")
dCdpYHdr = jsWrtTest.getHdrEntry("CDP_YD")
iInLineHdr = jsWrtTest.getHdrEntry("ILINE_NO")
iXLineHdr = jsWrtTest.getHdrEntry("XLINE_NO")

traceheaderSize = jsWrtTest.getTraceHeaderSize()
frame = np.zeros((NOffsets*NSamples), dtype=np.float32)
hdbuf = np.zeros((NOffsets*traceheaderSize), dtype=np.byte)
hdbuf2d = np.reshape(hdbuf, (-1, traceheaderSize))

#print len(hdbuf), len(hdbuf2d)

iInline=0
while (iInline<NInlines): 
	iXline=0
	while (iXline<NXlines):
		iTraces=0
		while (iTraces<NOffsets):
			itrcTypeHdr.setIntVal(hdbuf2d[iTraces], 1)
			iTimeHdr.setIntVal(hdbuf2d[iTraces], 0)
			fOffsetHdr.setFloatVal(hdbuf2d[iTraces],  off0 + iTraces*doff)
			iOffsetBinHdr.setIntVal(hdbuf2d[iTraces], iTraces)
			dCdpXHdr.setDoubleVal(hdbuf2d[iTraces], xl0 + iXline*dxl)
			dCdpYHdr.setDoubleVal(hdbuf2d[iTraces], inl0 + iInline*dinl)
			iInLineHdr.setIntVal(hdbuf2d[iTraces], iInline)
			iXLineHdr.setIntVal(hdbuf2d[iTraces], iXline)
			iSample=0
			while (iSample<NSamples):
				frame[iTraces*NSamples+iSample]= iSample + (iInline*NXlines + iXline)*NOffsets + iTraces
				iSample +=1
			iTraces+=1
		numLiveTraces = jsWrtTest.leftJustify(frame, hdbuf, NOffsets)
		frameInd=iInline*NXlines + iXline
		print(frameInd, numLiveTraces)
		ires = jsWrtTest.writeFrame(frameInd,frame, hdbuf, numLiveTraces)
		if ires!=numLiveTraces:
			print("Error while writing frame ", frameInd)
			iXline=NXlines
			iInline=NInlines
			break
		iXline+=1
	iInline+=1
print ("Write OK")

# testing the SWIGGED methods of jsFileWriter on the test data to copy and update
fr = jsswig.jsFileReader()
fr.Init("./dataTest.js")
fr.closefp();

jsWrtTestCopy = jsswig.jsFileWriter()
jsWrtTestCopy.setFileName("./dataTestCopy.js")
jsWrtTestCopy.Init(fr);
ires = jsWrtTestCopy.writeMetaData(2);
itrcTypeHdr = jsWrtTestCopy.getHdrEntry("TRC_TYPE")
iTimeHdr = jsWrtTestCopy.getHdrEntry("TIME")
fOffsetHdr = jsWrtTestCopy.getHdrEntry("OFFSET")
iOffsetBinHdr = jsWrtTestCopy.getHdrEntry("OFB_NO")
dCdpXHdr = jsWrtTestCopy.getHdrEntry("CDP_XD")
dCdpYHdr = jsWrtTestCopy.getHdrEntry("CDP_YD")
iInLineHdr = jsWrtTestCopy.getHdrEntry("ILINE_NO")
iXLineHdr = jsWrtTestCopy.getHdrEntry("XLINE_NO")

ndim = jsWrtTestCopy.getNDim()
NInlines = jsWrtTestCopy.getAxisLen(3)
NXlines = jsWrtTestCopy.getAxisLen(2)
NOffsets = jsWrtTestCopy.getAxisLen(1)
NSamples = jsWrtTestCopy.getAxisLen(0)

traceheaderSize = jsWrtTestCopy.getTraceHeaderSize()
frame = np.zeros((NOffsets*NSamples), dtype=np.float32)
hdbuf = np.zeros((NOffsets*traceheaderSize), dtype=np.byte)
hdbuf2d = np.reshape(hdbuf, (-1, traceheaderSize))

#print len(hdbuf), len(hdbuf2d)

iInline=0
while (iInline<NInlines): 
	iXline=0
	while (iXline<NXlines):
		iTraces=0
		while (iTraces<NOffsets):
			itrcTypeHdr.setIntVal(hdbuf2d[iTraces], 1)
			iTimeHdr.setIntVal(hdbuf2d[iTraces], 0)
			fOffsetHdr.setFloatVal(hdbuf2d[iTraces],  off0 + iTraces*doff)
			iOffsetBinHdr.setIntVal(hdbuf2d[iTraces], iTraces)
			dCdpXHdr.setDoubleVal(hdbuf2d[iTraces], xl0 + iXline*dxl)
			dCdpYHdr.setDoubleVal(hdbuf2d[iTraces], inl0 + iInline*dinl)
			iInLineHdr.setIntVal(hdbuf2d[iTraces], iInline)
			iXLineHdr.setIntVal(hdbuf2d[iTraces], iXline)
			iSample=0
			while (iSample<NSamples):
				frame[iTraces*NSamples+iSample]= 10 + iSample + (iInline*NXlines + iXline)*NOffsets + iTraces
				iSample +=1
			iTraces+=1
		numLiveTraces = jsWrtTestCopy.leftJustify(frame, hdbuf, NOffsets)
		frameInd=iInline*NXlines + iXline
		print(frameInd, numLiveTraces)
		ires = jsWrtTestCopy.writeFrame(frameInd,frame, hdbuf, numLiveTraces)
		if ires!=numLiveTraces:
			print("Error while writing frame ", frameInd)
			iXline=NXlines
			iInline=NInlines
			break
		iXline+=1
	iInline+=1
print ("copy and update all OK")

# testing the SWIGGED methods of jsFileWriter on the test data to copy and update traces only
fr1 = jsswig.jsFileReader()
fr1.Init("./dataTest.js")
fr1.closefp();

jsWrtTestCopy = jsswig.jsFileWriter()
jsWrtTestCopy.setFileName("./dataTestCopy2.js")
jsWrtTestCopy.Init(fr1)
ires = jsWrtTestCopy.writeMetaData(2)

ndim = jsWrtTestCopy.getNDim()
NInlines = jsWrtTestCopy.getAxisLen(3)
NXlines = jsWrtTestCopy.getAxisLen(2)
NOffsets = jsWrtTestCopy.getAxisLen(1)
NSamples = jsWrtTestCopy.getAxisLen(0)
traceheaderSize = jsWrtTestCopy.getTraceHeaderSize()
frame = np.zeros((NOffsets*NSamples), dtype=np.float32)

iInline=0
while (iInline<NInlines): 
	iXline=0
	while (iXline<NXlines):
		iTraces=0
		while (iTraces<NOffsets):
			iSample=0
			while (iSample<NSamples):
				frame[iTraces*NSamples+iSample]= 10 + iSample + (iInline*NXlines + iXline)*NOffsets + iTraces
				iSample +=1
			iTraces+=1
		frameInd=iInline*NXlines + iXline
		print(frameInd)
		ires = jsWrtTestCopy.writeFrame(frameInd,frame)
		if ires!=NOffsets:
			print("Error while writing frame ", frameInd)
			iXline=NXlines
			iInline=NInlines
			break
		iXline+=1
	iInline+=1
print ("copy and update traces OK")


# testing the SWIGGED methods of jsFileWriter on the test data to update traces only

fr1 = jsswig.jsFileReader()
fr1.Init("./dataTestCopy2.js")

jsWrtTestCopy = jsswig.jsFileWriter()
jsWrtTestCopy.setFileName("./dataTestCopy2.js")
jsWrtTestCopy.Init(fr1)
jsWrtTestCopy.Initialize();

ndim = jsWrtTestCopy.getNDim()
NInlines = jsWrtTestCopy.getAxisLen(3)
NXlines = jsWrtTestCopy.getAxisLen(2)
NOffsets = jsWrtTestCopy.getAxisLen(1)
NSamples = jsWrtTestCopy.getAxisLen(0)
traceheaderSize = jsWrtTestCopy.getTraceHeaderSize()
frame = np.zeros((NOffsets*NSamples), dtype=np.float32)
iInline=1
while (iInline<NInlines):
	iXline=1
	while (iXline<NXlines):
		iTraces=0
		while (iTraces<NOffsets):
			iSample=0
			while (iSample<NSamples):
				frame[iTraces*NSamples+iSample]= -100
				iSample +=1
			iTraces+=1
		frameInd=iInline*NXlines + iXline
		print(frameInd)
		ires = jsWrtTestCopy.writeFrame(frameInd,frame)
		if ires!=NOffsets:
			print("Error while writing frame ", frameInd)
			iXline=NXlines
			iInline=NInlines
			break
		iXline+=1
	iInline+=1
print ("over write traces OK")


#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(js))
#print(usefulStuff)

#iframe = 2
#fh = dataset.readFrameHeader(iframe, liveOnly=True)
#frame = dataset.readFrame(iframe, readHdrs=False, liveOnly=True)

#for ir in xrange(fh.shape[0]):
#    print dataset.hdrs['PAD_TRC'].getVal(fh[ir]), dataset.hdrs['TR_FOLD'].getVal(fh[ir]), dataset.hdrs['SHOT_2D'].getVal(fh[ir])

#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset.hdrs['XLINE_NO']))
#print usefulStuff

#####################################################################
#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(dataset.axes[1]))
#print usefulStuff

usefulStuff = filter((lambda s: s[0:2]!='__'),dir(jsswig))
print(usefulStuff)

#usefulStuff = filter((lambda s: s[0:2]!='__'),dir(fr))
#print usefulStuff

fr.getAxisLabels



