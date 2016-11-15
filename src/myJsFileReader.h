#include <vector>
#include "jsByteOrder.h"

namespace jsIO
{

  struct headerWordInfo;

  class jsFileReader
  {
    public:
      ~jsFileReader();
      
      jsFileReader(const unsigned long _bufferSize = 2097152); //default: 2MB cache. Set 0, to read directly (not cached)

      int Init(const std::string _jsfilename, const int _NThreads=1);
      
      bool isRegular() const;
      bool isSeisPEG() const; 
      
      long getNtr() const;
      
      long getNFrames() const;

      int getHeaderWords(std::vector<std::string> &names, std::vector<std::string> &descriptions) const;
      
      int getNumHeaderWords() const; 
      
      int getNumBytesInHeader() const;
      
      long getNumBytesInRawFrame() const;
      
      void getHeaderWordsInfo(headerWordInfo *pInfo) const;  

      unsigned long getIOBufferSize() const {return m_IOBufferSize;}
      int getNDim() const;
      int getAxisLen(int index) const;
      int getAxisLogicalValues(int index, std::vector<long> &axis) const;
      int getAxisPhysicalValues(int index, std::vector<double> &axis) const;
      int getAxisLabels(std::vector<std::string> &axis) const;
      int getAxisUnits(std::vector<std::string> &units) const;
      
      
      JS_BYTEORDER getByteOrder() const {return m_byteOrder;}
      std::string getByteOrderAsString() const;
      std::string getTraceFormatName() const;
      std::string getDescriptiveName() const{return m_descriptiveName;}
      std::string getDataType() const;

      catalogedHdrEntry getHdrEntry(std::string _name) const;
      
      std::vector<catalogedHdrEntry> getHdrEntries() const;
      int readTraceHeader(const int* _position, char *headbuf);
      
      int readTraceHeader(const long _traceIndex, char *headbuf);
      
      int readFrameHeader(const int* _position, char *headbuf);
      
      int readFrameHeader(const long _frameIndex, char *headbuf);//headbuf must be pre-allocated with the size = numOfTracesInFrame * getNumBytesInHeader()

      int readTrace(const int* _position, float *trace);
      
      int readTrace(const long _traceIndex, float *trace); 

      
      long readTraces(const long _firstTraceIndex,  const long _numOfTraces, float *buffer, char *headbuf=NULL);



      int liveToGlobalTraceIndex(const long _liveTraceIndex, long &_globalTraceIndex);

      long readWithinLiveTraces(const long _firstTraceIndex,  const long _numOfTraces, float *buffer, char *headbuf=NULL);


      long readWithinLiveTraceHeaders(const long _firstTraceIndex,  const long _numOfTraces, char *headbuf);


      int readFrame(const int* _position, float *frame, char *headbuf=NULL);
      

      int readRawFrames(const int* _position, int NFrames, char *rawframe, int *numLiveTraces);  
      
      int readRawFrames(const long _frameindex, int NFrames, char *rawframe, int *numLiveTraces);
      

      int getNumOfLiveTraces(int _frameIndex) const;
      
      std::string getVersion() const;
      
      std::string getCustomProperty(std::string _property);
      
      int getNumOfExtents() const;

      int getNumOfVirtualFolders() const;


  };
}



