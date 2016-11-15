# pyjseisio SWIG interface file
# python definitions for catalogedHdrEntry

%extend jsIO::catalogedHdrEntry {
%pythoncode %{

    def getVal(self, hdrBuf):
        """ 
        Get the value of a header from a header buffer. 
        The format of the returned value is inferred from the 
        getFormatAsStr() method.
        """
        frmt = self.getFormatAsStr();
        return {
            'float': self.getFloatVal,
            'double': self.getDoubleVal,
            'int': self.getIntVal,
            'short': self.getShortVal,
            'long': self.getLongVal
        }.get(frmt)(hdrBuf)

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

%}
}

