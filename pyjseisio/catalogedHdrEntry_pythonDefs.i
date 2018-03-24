// pyjseisio SWIG interface file
// python definitions for catalogedHdrEntry

%extend jsIO::catalogedHdrEntry {
%pythoncode %{

    def getVal(self, hdrBuf):
        """ 
        Get the value of a header from a single trace header buffer. 
        The format of the returned value is inferred from the 
        getFormatAsStr() method.
        """
        frmt = self.getFormatAsStr()
        return {
            'float': self.getFloatVal,
            'double': self.getDoubleVal,
            'int': self.getIntVal,
            'int8': self.getShortVal, # this should still be buggy, need to add more methods in jseisIO
            'int16': self.getShortVal,
            'int32': self.getIntVal,
            'int64': self.getLongVal,
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
        ndim = hdrBuf.ndim
        assert ndim==2 or ndim==3, \
            "require hdrBuf ndim 2 or 3"
        hbuf = hdrBuf.reshape(1, hdrBuf.shape[0], hdrBuf.shape[1]) if (ndim ==2) else hdrBuf
        nframes = hbuf.shape[0]
        ntraces = hbuf.shape[1]
        nbytes = hbuf.shape[2]
        frmt = self.getFormatAsStr()
        vals = np.empty(shape=(nframes, ntraces), dtype= {
            'float': np.float32,
            'double': np.float64,
            'int': np.int32,
            'int8': np.int8,
            'int16': np.int16,
            'int32': np.int32,
            'int64': np.int64,
            'short': np.int16,
            'long': np.int64
        }.get(frmt))
        {
            'float': self.getFloatValsHelper,
            'double': self.getDoubleValsHelper,
            'int': self.getIntValsHelper,
            'int8': self.getShortValsHelper, # this should still be buggy, need to add more methods in jseisIO
            'int16': self.getShortValsHelper,
            'int32': self.getIntValsHelper,
            'int64': self.getLongValsHelper,
            'short': self.getShortValsHelper,
            'long': self.getLongValsHelper
        }.get(frmt)(hbuf, vals)
        return vals.reshape(ntraces) if (ndim ==2) else vals

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
        return [self.setVal(hdrBuf[i,:], values[i]) for i in range(ntraces)]

%}
}

