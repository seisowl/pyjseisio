from pyjseisio import jsFileReader
from pyjseisio import vectorToList
import os.path

def open(filename):
    fpfile = filename+"/FileProperties.xml"
    assert(os.path.isdir(filename)),("JavaSeis file not found: " + filename)
    assert(os.path.isfile(fpfile)), ("JavaSeis file not found: " + fpfile)
    newJseis = jsdataset()
    newJseis.reader = jsFileReader()
    newJseis.reader.Init(filename)
    newJseis._makeHeaderDict()
    return newJseis



class jsdataset(object):

    def _makeHeaderDict(self):
        self.hdrs = {}
        for hdr in self.reader.getHdrEntries():
            self.hdrs[hdr.getName()] = hdr

# jsFileReader delegate and convenience methods

    def readFrame(self, frameIndex):
        """
        Read one frame from the dataset at the given frameIndex.
        Returns a numpy ndarray with shape (AxisLen(1),AxisLen(0))
        """
        length = self.getAxisLen(0) * self.getAxisLen(1)
        frame = self.reader._readFrameOnly(frameIndex,length)[1]
        return frame.reshape(self.getAxisLen(1),self.getAxisLen(0))

    def readFrameAndHdrs(self, frameIndex):
        """
        Read one frame from the dataset at the given frameIndex with headers.
        Returns two numpy ndarrays in a tuple with shapes
        [0]: (AxisLen(1),AxisLen(0))
        [1]: (AxisLen(1),NumBytesInHeader)
        """
        length = self.getAxisLen(0) * self.getAxisLen(1)
        hdrLength = self.getNumBytesInHeader() * self.getAxisLen(1)
        data = self.reader._readFrameAndHdrs(frameIndex,length,hdrLength);
        return (data[1].reshape(self.getAxisLen(1),
                                self.getAxisLen(0)),
                data[2].reshape(self.getAxisLen(1),
                                self.getNumBytesInHeader()))

    def getHeaderWords(self):
        """
        Get the header words and descriptions.
        Returns a three element tuple with:
                0: List of header names
                1: List of header descriptions
                2: Number of headers
        """
        names = StringVector()
        desc = StringVector()
        nWords = self.reader._getHeaderWords(names,desc)
        return (vectorToList(names), vectorToList(desc), nWords)

    def getAxisLogicalValues(self, axisIndex):
        """
        Get the logical values for the given axis.
        Returns a two element tuple with:
                0: List of logical values (long)
                1: Number of values
        """
        values = LongVector()
        nValues = self.reader._getAxisLogicalValues(axisIndex, values)
        return (vectorToList(values), nValues)

    def getAxisPhyscialValues(self, axisIndex):
        """
        Get the physical values for the given axis.
        Returns a two element tuple with:
                0: List of physical values (double)
                1: Number of values
        """
        values = DoubleVector()
        nValues = self.reader._getAxisPhysicalValues(axisIndex, values)
        return (vectorToList(values), nValues)

    def getAxisLabels(self):
        """
        Get the labels of each axis.
        Returns a two element tuple with:
                0: List of axis labels (string)
                1: Number of axes
        """
        labels = StringVector()
        nLabels = self.reader._getAxisLabels(labels)
        return (vectorToList(labels), nLabels)

    def getAxisUnits(self):
        """
        Get the units of each axis.
        Returns a two element tuple with:
                0: List of axis units (string)
                1: Number of axes
        """
        units = StringVector()
        nUnits = self.reader._getAxisUnits(units)
        return (vectorToList(units), nUnits)

    def getAxisLen(self, axis):
        return self.reader.getAxisLen(axis)
    
    def getNumBytesInHeader(self):
        return self.reader.getNumBytesInHeader()
