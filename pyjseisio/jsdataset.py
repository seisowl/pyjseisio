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



    def readFrame(self, frameIndex):
        """
        Read one frame from the dataset at the given frameIndex.
        Returns a numpy ndarray with shape (AxisLen(1),AxisLen(0))
        """
        length = self.axes[0].len * self.axes[1].len
        frame = self._reader.readFrameDataOnly(frameIndex,length)[1]
        return frame.reshape(self.axes[1].len, self.axes[0].len)

    def readFrameAndHdrs(self, frameIndex):
        """
        Read one frame from the dataset at the given frameIndex with headers.
        Returns two numpy ndarrays in a tuple with shapes
        [0]: (AxisLen(1),AxisLen(0))
        [1]: (AxisLen(1),NumBytesInHeader)
        """
        length = self.axes[0].len * self.axes[1].len
        hdrLength = self.getNumBytesInHeader() * self.axes[1].len
        data = self._reader.readFrameDataAndHdrs(frameIndex,length,hdrLength);
        return (data[1].reshape(self.axes[1].len,
                                self.axes[0].len),
                data[2].reshape(self.axes[1].len,
                                self.getNumBytesInHeader()))

    def readFrameHeader(self, frameIndex):
        """
        Read the headers of one frame from the dataset at the given frameIndex.
        Returns a numpy ndarray with shape (AxisLen(1),NumBytesInHeader)
        """
        hdrLength = self.getNumBytesInHeader() * self.axes[1].len
        hdrs = self._reader.readFrameHdrsOnly(frameIndex,hdrLength)[1];
        return hdrs.reshape(self.axes[1].len, self.getNumBytesInHeader())

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


class jsaxis:
    def __init__(self, label, units, length, logVals, physVals):
        self.label = label
        self.units = units
        self.len = length
        self.logicalValues = logVals
        self.physicalValues = physVals
    
