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
        return {
            'float': self.getFloatVal(hdrBuf),
            'double': self.getDoubleVal(hdrBuf),
            'int': self.getIntVal(hdrBuf),
            'short': self.getShortVal(hdrBuf),
            'long': self.getLongVal(hdrBuf)
        }.get(self.getFormatAsStr())

    def setVal(self, hdrBuf, value):
    """ 
    Set the value of a header in a header buffer. 
    The format of the set value is inferred from the 
    getFormatAsStr() method.
    """
        return {
            'float': self.setFloatVal(hdrBuf, value),
            'double': self.setDoubleVal(hdrBuf, value),
            'int': self.setIntVal(hdrBuf, value),
            'short': self.setShortVal(hdrBuf, value),
            'long': self.setLongVal(hdrBuf, value)
        }.get(self.getFormatAsStr())


%}
}

