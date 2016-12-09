import pyjseisio as js
import os.path

def open(filename):
    fpfile = filename+"/FileProperties.xml"
    assert(os.path.isdir(filename)),("JavaSeis file not found: " + filename)
    assert(os.path.isfile(fpfile)), ("JavaSeis file not found: " + fpfile)
    return jsdataset.openForRead(filename)


class jsdataset(object):

    @classmethod
    def openForRead(cls, filename):
        """
        Factory classmethod to open a JavaSeis dataset for reading.
        Input: filename - path to JavaSeis dataset directory
        Output: jsdataset object with file opened
        """
        data = jsdataset()
        data._reader = js.jsFileReader()
        data._reader.Init(filename)
        data.hdrs = {}
        for hdr in data._reader.getHdrEntries():
            data.hdrs[hdr.getName()] = hdr
        data.axes = ()
        labels = js.StringVector()
        units = js.StringVector()
        data._reader.getAxisLabels(labels)
        data._reader.getAxisUnits(units)
        for idim in range(0,data._reader.getNDim()):
            logValues = js.LongVector()
            data._reader.getAxisLogicalValues(idim,logValues)
            physValues = js.DoubleVector()
            data._reader.getAxisPhysicalValues(idim,physValues)
            newAxis = jsaxis(js.vectorToList(labels)[idim],
                             js.vectorToList(units)[idim],
                             data._reader.getAxisLen(idim),
                             js.vectorToList(logValues),
                             js.vectorToList(physValues))
            data.axes = data.axes + (newAxis,)
        return data       


    def readFrame(self, frameIndex, readHdrs=True, liveOnly=False):
        """
        Read one frame from the dataset at the given global frameIndex.
        By default, returns a tulple containing (frameData, frameHeader),
        where frameData is a numpy ndarray with shape (AxisLen(1),AxisLen(0))
        frameHeader ia a numpy ndarray with shape (AxisLen(1),NumBytesInHeader)
        if readHdrs is set to False, only returns the frameData numpy array.
        If liveOnly is set to True, then the data and header returned are
        for the live traces within the frame only.
        """
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
        """
        Read the headers of one frame from the dataset at the given global frameIndex.
        Returns a numpy ndarray with shape (AxisLen(1),NumBytesInHeader)
        Keyword argument 'liveOnly' determines whether to retrieve only the live 
        trace headers, or all headers.  
        """
        ntraces =  self.getNumOfLiveTraces(frameIndex) if liveOnly \
                   else self.axes[1].len
        fullHdrLength = self.getNumBytesInHeader() * self.axes[1].len
        hdrLength = self.getNumBytesInHeader() * ntraces
        hdrs = self._reader.readFrameHdrsOnly(frameIndex,fullHdrLength)[1]
        return hdrs[0:hdrLength].reshape(ntraces, self.getNumBytesInHeader())


    def readTraces(self, traceIndex, numTraces):
        """
        Read multiple traces from the dataset starting 
        at the given global trace index.
        Returns a numpy ndarray with shape (numTraces,AxisLen(0))
        """
        length = numTraces*self.axes[0].len
        trace = self._reader.readTracesDataOnly(traceIndex, numTraces, length)[1]
        return trace.reshape(numTraces, self.axes[0].len)


    def readTraceHeaders(self, traceIndex, numTraces):
        """
        Read multiple trace headers from the dataset starting 
        at the given global trace index.
        Returns a numpy ndarray with shape (numTraces,NumBytesInHeader)
        """
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


class jsaxis:
    def __init__(self, label, units, length, logVals, physVals):
        self.label = label
        self.units = units
        self.len = length
        self.logicalValues = logVals
        self.physicalValues = physVals
    
