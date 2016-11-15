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
        data = jsdataset()
        data.reader = js.jsFileReader()
        data.reader.Init(filename)
        data.hdrs = {}
        data.hdrDesc = {}
        for hdr in data.reader.getHdrEntries():
            data.hdrs[hdr.getName()] = hdr
        data.axes = ()
        labels = js.StringVector()
        units = js.StringVector()
        data.reader.getAxisLabels(labels)
        data.reader.getAxisUnits(units)
        for idim in range(0,data.reader.getNDim()):
            logValues = js.LongVector()
            data.reader.getAxisLogicalValues(idim,logValues)
            physValues = js.DoubleVector()
            data.reader.getAxisPhysicalValues(idim,physValues)
            newAxis = jsaxis(js.vectorToList(labels)[idim],
                             js.vectorToList(units)[idim],
                             data.reader.getAxisLen(idim),
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
        frame = self.reader.readFrameOnly(frameIndex,length)[1]
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
        data = self.reader.readFrameAndHdrs(frameIndex,length,hdrLength);
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
        hdrs = self.reader.readHdrsOnly(frameIndex,hdrLength)[1];
        return hdrs.reshape(self.axes[1].len, self.getNumBytesInHeader())

    # no-arg methods delegated to self.reader
    def isRegular(self): return self.reader.isRegular()
    def isSeisPEG(self): return self.reader.isSeisPEG()
    def getNtr(self): return self.reader.getNtr()
    def getNFrames(self): return self.reader.getNFrames()
    def getNumHeaderWords(self): return self.reader.getNumHeaderWords()
    def getNumBytesInHeader(self): return self.reader.getNumBytesInHeader()
    def getNumBytesInRawFrame(self): return self.reader.getNumBytesInRawFrame()
    def getIOBufferSize(self): return self.reader.getIOBufferSize()
    def getNDim(self): return self.reader.getNDim()
    def getFrameSizeOnDisk(self): return self.reader.getFrameSizeOnDisk()
    def getByteOrder(self): return self.reader.getByteOrder()
    def getByteOrderAsString(self): return self.reader.getByteOrderAsString()
    def getTraceFormatName(self): return self.reader.getTraceFormatName()
    def getDescriptiveName(self): return self.reader.getDescriptiveName()
    def getDataType(self): return self.reader.getDataType()
    def getVersion(self): return self.reader.getVersion()
    def getNumOfExtents(self): return self.reader.getNumOfExtents()
    def getNumOfVirtualFolders(self): return self.reader.getNumOfVirtualFolders()

class jsaxis:
    def __init__(self, label, units, length, logVals, physVals):
        self.label = label
        self.units = units
        self.len = length
        self.logicalValues = logVals
        self.physicalValues = physVals
    
