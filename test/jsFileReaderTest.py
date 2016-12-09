import unittest
import numpy as np
import pyjseisio.pyjseisio_swig as jsswig


# testing the SWIGGED methods of jsFileReader on the test dataset synth.js
fr = jsswig.jsFileReader()

# know values
ndim = 5
nsamples = 501
tracesperframe = 40
ntraces = 720
nframes = 18
framespervolume = 3
nvolumes = 3
nhypers = 2
header0name = "TRC_TYPE"
header0desc = "\"Trace type (data, aux, etc.)\""
header15name = "TRACENO"
header15desc = "\"Trace number in seismic line*\""
numhdrwords = 35
numbytesinheader = 148
bytespersample = 2
numbytesinrawframe = 41120
buffersize = 2097152
samplelogicalvalues = range(nsamples)
tracelogicalvalues = range(1,tracesperframe+1)
framelogicalvalues = range(2000,2003)
volumelogicalvalues = range(1000,1003)
hyperlogicalvalues = range(0,2)
samplephysicalvalues = range(0,1002,2)
tracephysicalvalues = range(0,2000,50)
framephysicalvalues = range(0,150,50)
volumephysicalvalues = range(0,150,50)
hyperphysicalvalues = range(0,2,1)
axislabels = ["TIME", "SEQNO", "CROSSLINE", "INLINE", "FILTERID"]
axisunits = ['milliseconds', 'feet', 'feet', 'feet', 'unknown']


# tests
class TestJsFileReader(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestJsFileReader, self).__init__(*args, **kwargs)
    
    def test_instantiate(self):
        assert (fr is not None)

    def test_isRegular(self):
        assert fr.isRegular()

    def test_isSeisPEG(self):
        assert (not fr.isSeisPEG())

    def test_getNtr(self):
        assert (fr.getNtr() == ntraces)

    def test_getNFrames(self):
        assert (fr.getNFrames() == nframes)

    def test_getHeaderWords(self):
        s = jsswig.StringVector()
        d = jsswig.StringVector()
        fr.getHeaderWords(s,d)
        assert s[0] == (header0name)
        assert s[15] == (header15name)
        assert d[0] == (header0desc)
        assert d[15] == (header15desc)

    def test_getNumHeaderWords(self):
        assert (fr.getNumHeaderWords() == numhdrwords)

    def test_getNumBytesInHeader(self):
        assert (fr.getNumBytesInHeader() == numbytesinheader)

    def test_getNumBytesInRawFrame(self):
        assert (fr.getNumBytesInRawFrame() == numbytesinrawframe)

    def test_getHeaderWordsInfo(self):
        info = fr.getHeaderWordsInfo(0)
        assert (len(info) == numhdrwords)
        
    def test_getIOBufferSize(self):
        assert (fr.getIOBufferSize() == buffersize)
            
    def test_getNDim(self):
        assert (fr.getNDim() == ndim)

    def test_getAxisLen(self):
        assert (fr.getAxisLen(0) == nsamples)
        assert (fr.getAxisLen(1) == tracesperframe)
        assert (fr.getAxisLen(2) == framespervolume)
        assert (fr.getAxisLen(3) == nvolumes)
        assert (fr.getAxisLen(4) == nhypers)

    def test_getAxisLogicalValues_samples(self):
        samps = jsswig.LongVector()
        fr.getAxisLogicalValues(0, samps)
        sampsL = [samps[i] for i in range(len(samps))]
        assert (sampsL == samplelogicalvalues)

    def test_getAxisLogicalValues_traces(self):
        traces = jsswig.LongVector()
        fr.getAxisLogicalValues(1, traces)
        tracesL = [traces[i] for i in range(len(traces))]
        assert (tracesL == tracelogicalvalues)

    def test_getAxisLogicalValues_frames(self):
        frames = jsswig.LongVector()
        fr.getAxisLogicalValues(2, frames)
        framesL = [frames[i] for i in range(len(frames))]
        assert (framesL == framelogicalvalues)

    def test_getAxisLogicalValues_volumes(self):
        volumes = jsswig.LongVector()
        fr.getAxisLogicalValues(3, volumes)
        volumesL = [volumes[i] for i in range(len(volumes))]
        assert (volumesL == volumelogicalvalues)

    def test_getAxisLogicalValues_hypers(self):
        hypers = jsswig.LongVector()
        fr.getAxisLogicalValues(4, hypers)
        hypersL = [hypers[i] for i in range(len(hypers))]
        assert (hypersL == hyperlogicalvalues)

    def test_getAxisPhysicalValues_samples(self):
        samps = jsswig.DoubleVector()
        fr.getAxisPhysicalValues(0, samps)
        sampsL = [samps[i] for i in range(len(samps))]
        assert (sampsL == samplephysicalvalues)

    def test_getAxisPhysicalValues_traces(self):
        traces = jsswig.DoubleVector()
        fr.getAxisPhysicalValues(1, traces)
        tracesL = [traces[i] for i in range(len(traces))]
        assert (tracesL == tracephysicalvalues)

    def test_getAxisPhysicalValues_frames(self):
        frames = jsswig.DoubleVector()
        fr.getAxisPhysicalValues(2, frames)
        framesL = [frames[i] for i in range(len(frames))]
        assert (framesL == framephysicalvalues)

    def test_getAxisPhysicalValues_volumes(self):
        volumes = jsswig.DoubleVector()
        fr.getAxisPhysicalValues(3, volumes)
        volumesL = [volumes[i] for i in range(len(volumes))]
        assert (volumesL == volumephysicalvalues)

    def test_getAxisPhysicalValues_hypers(self):
        hypers = jsswig.DoubleVector()
        fr.getAxisPhysicalValues(4, hypers)
        hypersL = [hypers[i] for i in range(len(hypers))]
        assert (hypersL == hyperphysicalvalues)

    def test_getAxisLabels(self):
        labels = jsswig.StringVector()
        fr.getAxisLabels(labels)
        labelsL = [labels[i] for i in range(len(labels))]
        assert labelsL == axislabels
       
    def test_getAxisUnits(self):
        units = jsswig.StringVector()
        fr.getAxisUnits(units)
        unitsL = [units[i] for i in range(len(units))]
        assert unitsL == axisunits
    

if __name__ == '__main__':
    fr.Init("./synth.js")
    unittest.main()

