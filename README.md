#pyjseisio

Wrapping the C++ jseisIO library with SWIG for python.

All meta data is coming out as lists or tuples (getHdrEntries() returns a tuple)
Binary data should come out as numpy arrays

##References to read
https://docs.scipy.org/doc/numpy-1.10.0/reference/swig.interface-file.html

##Notes
Added numpy.i from numpy git master 11Nov16
Need to add setenv LD_LIBRARY_PATH "/data/esdrd/eyms/python/pyjseisio/jseisIO"

##TODO
appropriate swig type for JS_BYTORDER pointers
int readFrame(const int* _position, float *frame, char *headbuf=NULL);
void getHeaderWordsInfo(headerWordInfo *pInfo) const;
int readTraceHeader(const int* _position, char *headbuf);
int readTraceHeader(const long _traceIndex, char *headbuf);
int readFrameHeader(const int* _position, char *headbuf);
int readFrameHeader(const long _frameIndex, char *headbuf)
int readTrace(const int* _position, float *trace);
int readTrace(const long _traceIndex, float *trace);
long readTraces(const long _firstTraceIndex,  const long _numOfTraces, float *buffer, char *headbuf=NULL);
long readTraceHeaders(const long _firstTraceIndex,  const long _numOfTraces, char *headbuf);
int liveToGlobalTraceIndex(const long _liveTraceIndex, long &_globalTraceIndex);
long readWithinLiveTraces(const long _firstTraceIndex,  const long _numOfTraces, float *buffer, char *headbuf=NULL);
long readWithinLiveTraceHeaders(const long _firstTraceIndex,  const long _numOfTraces, char *headbuf);
int readFrame(const long _frameIndex, float *frame, char *headbuf=NULL);
int readRawFrames(const int* _position, int NFrames, char *rawframe, int *numLiveTraces);
int readRawFrames(const long _frameindex, int NFrames, char *rawframe, int *numLiveTraces);
int uncompressRawFrame(char *rawframe, int numLiveTraces, int iThread,  float *frame, char* headbuf=NULL);


##test code snippet
import pyjseisio as js; reader = js.jsFileReader(); reader.Init("/data/data343/AcpPromaxHome/mauritania3d/eyms/00transposed_frame.js")
x = reader.readFrame(0)
x = reader.getHdrEntries()
