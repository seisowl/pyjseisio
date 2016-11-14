# list of functions to ignore for now ... not implemented in SWIG yet

# unimplemented jsFileReader methods
%ignore jsIO::jsFileReader::uncompressRawFrame;
%ignore jsIO::jsFileReader::readRawFrames;
%ignore jsIO::jsFileReader::readWithinLiveTraceHeaders;
%ignore jsIO::jsFileReader::readWithinLiveTraces;
%ignore jsIO::jsFileReader::readTraceHeader;
%ignore jsIO::jsFileReader::readTraceHeaders;
%ignore jsIO::jsFileReader::readTraces;
%ignore jsIO::jsFileReader::readTrace;
%ignore jsIO::jsFileReader::readFrameHeader;
%ignore jsIO::jsFileReader::readTraceHeader;
