# pyjseisio SWIG interface file
# python definitions for catalogedHdrEntry

%extend jsIO::catalogedHdrEntry {
%pythoncode %{

    def getVal(self, hdrBuf):
        """ 
        Get the value of a header from a single trace header buffer. 
        The format of the returned value is inferred from the 
        getFormatAsStr() method.
        """
        frmt = self.getFormatAsStr();
        return {
            'float': self.getFloatVal,
            'double': self.getDoubleVal,
            'int': self.getIntVal,
            'int8': self.getIntVal,
            'int16': self.getIntVal,
            'int32': self.getIntVal,
            'int64': self.getIntVal,
            'short': self.getShortVal,
            'long': self.getLongVal
        }.get(frmt)(hdrBuf)

    def getVals(self, hdrBuf):
        """ 
        Get the values of a header from a multi-trace header buffer. 
        The format of the returned value is inferred from the 
        getFormatAsStr() method.
        Returns a standard Python list of the header values from the
        provided header buffer. 
        """
        ntraces = hdrBuf.shape[0]
        return [self.getVal(hdrBuf[i,:]) for i in xrange(ntraces)]

    def setVal(self, hdrBuf, value):
        """ 
        Set the value of a header in a header buffer. 
        The format of the set value is inferred from the 
        getFormatAsStr() method.
        """
        frmt = self.getFormatAsStr();
        return {
            'float': self.setFloatVal,
            'double': self.setDoubleVal,
            'int': self.setIntVal,
            'short': self.setShortVal,
            'long': self.setLongVal
        }.get(frmt)(hdrBuf,value)

    def setVals(self, hdrBuf, values):
        """ 
        Set the values of a header from a multi-trace header buffer. 
        """
        assert hdrBuf.shape[0]==len(values), \
            "require hdrBuf.shape[0]==len(values)"
        ntraces = hdrBuf.shape[0]
        return [self.setVal(hdrBuf[i,:], values[i]) for i in xrange(ntraces)]

%}
}

