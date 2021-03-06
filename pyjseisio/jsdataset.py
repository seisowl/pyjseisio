import numpy as np
import pyjseisio.pyjseisio_swig as jsswig
import os.path

def open(filename):
    fpfile = filename+'/FileProperties.xml'
    assert(os.path.isdir(filename)),('JavaSeis file not found: ' + filename)
    assert(os.path.isfile(fpfile)), ('JavaSeis file not found: ' + fpfile)
    return jsdataset.openForRead(filename)



class jsdataset(object):

    @classmethod
    def openForRead(cls, filename):
        '''
        Factory classmethod to open a JavaSeis dataset for reading.
        Input: filename - path to JavaSeis dataset directory
        Output: jsdataset object with file opened
        '''
        data = cls()
        data._reader = jsswig.jsFileReader()
        data._reader.Init(filename)
        data._infilename = filename
        data._writer = None
        data._outfilename = None
        data._outwriter = None
        data.hdrs = {}
        for hdr in data._reader.getHdrEntries():
            data.hdrs[hdr.getName()] = hdr
        data.axes = ()
        labels = jsswig.StringVector()
        units = jsswig.StringVector()
        domains = jsswig.StringVector()
        data._reader.getAxisLabels(labels)
        data._reader.getAxisUnits(units)
        data._reader.getAxisDomains(domains)
        for idim in range(0,data._reader.getNDim()):
            logValues = jsswig.LongVector()
            data._reader.getAxisLogicalValues(idim,logValues)
            physValues = jsswig.DoubleVector()
            data._reader.getAxisPhysicalValues(idim,physValues)
            newAxis = jsaxis(jsswig.vectorToList(labels)[idim],
                             jsswig.vectorToList(units)[idim],
                             jsswig.vectorToList(domains)[idim],
                             data._reader.getAxisLen(idim),
                             jsswig.vectorToList(logValues),
                             jsswig.vectorToList(physValues))
            data.axes = data.axes + (newAxis,)
        return data

    def writeFrame(self, frameIndex, traces, headers=None, ntraces=-1):
        '''
        Overwrite the current frame/hdrs at given global frameIndex
        :param frameIndex: global frame index
        :param traces: the frame buffer
        :param headers: the header buffer
        :param ntraces: number trace in this frame
        :return: number of trace written
        '''
        if self._writer is None:
            self._writer = jsswig.jsFileWriter()
            self._writer.setFileName(self._infilename)
            self._writer.Init(self._reader)

        if headers is None:
            return self._writer.writeFrame(frameIndex, np.reshape(traces, (np.product(traces.shape),)))
        else:
            return self._writer.writeFrame(frameIndex, np.reshape(traces, (np.product(traces.shape),)),
                                           np.reshape(headers, (np.product(headers.shape),)), ntraces)

    def writeFrameToFile(self, outfilename, frameIndex, traces, headers=None, ntraces=-1):
        '''
        save the frame/header to outfilename file. if it is new file, it will copy all info from current input file,
        then replace the specify frame with the given buffer.
        :param outfilename: the filename to be written
        :param frameIndex: global frame index
        :param traces: the frame buffer
        :param headers: the header buffer
        :param ntraces: number trace in this frame
        :return: number of trace written
        '''
        if outfilename == self._infilename :
            self.overWriteFrame(frameIndex, np.reshape(traces, (np.product(traces.shape),)),
                                np.reshape(headers, (np.product(headers.shape),)), ntraces)
        else :
            if outfilename == self._outfilename :
                self._outwriter.writeFrame(frameIndex, np.reshape(traces, (np.product(traces.shape),)),
                                           np.reshape(headers, (np.product(headers.shape),)), ntraces)
            else:
                assert (not os.path.isdir(outfilename)), ('!!!File exist: ' + outfilename)
                self._outwriter = jsswig.jsFileWriter()
                self._outwriter.setFileName(outfilename)
                self._outwriter.Init(self._reader)
                self._outwriter.writeMetaData(2)
                self._outfilename = outfilename
                self._outwriter.writeFrame(frameIndex, np.reshape(traces, (np.product(traces.shape),)),
                                           np.reshape(headers, (np.product(headers.shape),)), ntraces)


    def readFrame(self, frameIndex, readHdrs=True, liveOnly=False):
        '''
        Read one frame from the dataset at the given global frameIndex.
        By default, returns a tulple containing (frameData, frameHeader),
        where frameData is a numpy ndarray with shape (AxisLen(1),AxisLen(0))
        frameHeader ia a numpy ndarray with shape (AxisLen(1),NumBytesInHeader)
        if readHdrs is set to False, only returns the frameData numpy array.
        If liveOnly is set to True, then the data and header returned are
        for the live traces within the frame only.
        '''
        ntraces =  self.getNumOfLiveTraces(frameIndex) if liveOnly \
                   else self.axes[1].len
        fullDataLength = self.axes[0].len * self.axes[1].len
        dataLength = self.axes[0].len * ntraces
        fullHdrLength = self.getNumBytesInHeader() * self.axes[1].len
        hdrLength = self.getNumBytesInHeader() * ntraces

        if readHdrs:
            data = self._reader.readFrameDataAndHdrs(frameIndex,
                                                 fullDataLength,
                                                 fullHdrLength)
            returnData = (data[1][0:dataLength].reshape(ntraces, 
                                              self.axes[0].len),
                          data[2][0:hdrLength].reshape(ntraces, 
                                              self.getNumBytesInHeader()))
        else:
            frame = self._reader.readFrameDataOnly(frameIndex,fullDataLength)[1]
            returnData =  frame[0:dataLength].reshape(ntraces, self.axes[0].len)            

        return returnData


    def readFrameHeader(self, frameIndex, liveOnly=False):
        '''
        Read the headers of one frame from the dataset at the given global frameIndex.
        Returns a numpy ndarray with shape (AxisLen(1),NumBytesInHeader)
        Keyword argument 'liveOnly' determines whether to retrieve only the live 
        trace headers, or all headers.  
        '''
        ntraces =  self.getNumOfLiveTraces(frameIndex) if liveOnly \
                   else self.axes[1].len
        fullHdrLength = self.getNumBytesInHeader() * self.axes[1].len
        hdrLength = self.getNumBytesInHeader() * ntraces
        hdrs = self._reader.readFrameHdrsOnly(frameIndex,fullHdrLength)[1]
        return hdrs[0:hdrLength].reshape(ntraces, self.getNumBytesInHeader())


    def readTraces(self, traceIndex, numTraces):
        '''
        Read multiple traces from the dataset starting 
        at the given global trace index.
        Returns a numpy ndarray with shape (numTraces,AxisLen(0))
        '''
        length = numTraces*self.axes[0].len
        trace = self._reader.readTracesDataOnly(traceIndex, numTraces, length)[1]
        return trace.reshape(numTraces, self.axes[0].len)


    def readTraceHeaders(self, traceIndex, numTraces):
        '''
        Read multiple trace headers from the dataset starting 
        at the given global trace index.
        Returns a numpy ndarray with shape (numTraces,NumBytesInHeader)
        '''
        length = numTraces*self.getNumBytesInHeader()
        trace = self._reader.readTraceHeadersOnly(traceIndex, numTraces, length)[1]
        return trace.reshape(numTraces, self.getNumBytesInHeader())


    # no-arg methods delegated to self._reader
    def isRegular(self): return self._reader.isRegular()
    def isSeisPEG(self): return self._reader.isSeisPEG()
    def getNtr(self): return self._reader.getNtr()
    def getNFrames(self): return self._reader.getNFrames()
    def getNumHeaderWords(self): return self._reader.getNumHeaderWords()
    def getNumBytesInHeader(self): return self._reader.getNumBytesInHeader()
    def getNumBytesInRawFrame(self): return self._reader.getNumBytesInRawFrame()
    def getIOBufferSize(self): return self._reader.getIOBufferSize()
    def getNDim(self): return self._reader.getNDim()
    def getFrameSizeOnDisk(self): return self._reader.getFrameSizeOnDisk()
    def getByteOrder(self): return self._reader.getByteOrder()
    def getByteOrderAsString(self): return self._reader.getByteOrderAsString()
    def getTraceFormatName(self): return self._reader.getTraceFormatName()
    def getDescriptiveName(self): return self._reader.getDescriptiveName()
    def getDataType(self): return self._reader.getDataType()
    def getVersion(self): return self._reader.getVersion()
    def getNumOfExtents(self): return self._reader.getNumOfExtents()
    def getNumOfVirtualFolders(self): return self._reader.getNumOfVirtualFolders()
    def getHeaderWordsInfo(self): return self._reader.getHeaderWordsInfo(0)

    # arg-full methods delegated to self._reader
    def getNumOfLiveTraces(self, frameIndex): 
        return self._reader.getNumOfLiveTraces(frameIndex)

label2hdr = {'CROSSLINE':'XLINE_NO', 'INLINE':'ILINE_NO', 'SAIL_LINE':'S_LINE', 'TIME':'V_TIME', 'DEPTH':'V_DEPTH', 'CMP':'CDP', 'RECEIVER_LINE':'R_LINE', 'CHANNEL':'CHAN', 'RECEIVER':'REC_SLOC', 'OFFSET_BIN':'OFB_NO' }
class jsaxis:
    def __init__(self, label, units, domain, length, logVals, physVals):
        self.label = label
        hdr = label2hdr.get(label)
        self.hdr = hdr if hdr else label
        self.units = units
        self.domain = domain
        self.len = length
        self.logicalValues = logVals
        self.physicalValues = physVals
    
