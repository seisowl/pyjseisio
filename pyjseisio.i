# pyjseisio SWIG interface file
# master interface file

%module pyjseisio

%{
#define SWIG_FILE_WITH_INIT
#include "../jseisIO/src/jsFileReader.h"
#include "../jseisIO/src/jsByteOrder.h"
#include "../jseisIO/src/catalogedHdrEntry.h"
using namespace jsIO;
%}

%init %{
import_array();
%}


%include <std_string.i>
%include <std_vector.i>
%include <typemaps.i>
%include "numpy.i"

# pyjseisio interface files
%include "jsFileReader_typemaps.i"
%include "jsFileReader_pythonDefs.i"

# Set up proxy classes for std::vectors
%template(DoubleVector) std::vector<double>;
%template(LongVector) std::vector<long>;
%template(StringVector) std::vector<std::string>;
%template(CatalogedHdrEntryVector) std::vector<jsIO::catalogedHdrEntry>;


%pythoncode %{
def vectorToList(vector):
    return [vector[x] for x in xrange(vector.size())]
%}


# list of functions to ignore for now ... not implemented in SWIG yet
%ignore jsFileReader::uncompressRawFrame;
%ignore jsFileReader::readRawFrames;
%ignore jsFileReader::readWithinLiveTraceHeaders;
%ignore jsFileReader::readWithinLiveTraces;
%ignore jsFileReader::readTraceHeader;
%ignore jsFileReader::readTraceHeaders;
%ignore jsFileReader::readTraces;
%ignore jsFileReader::readTrace;
%ignore jsFileReader::readFrameHeader;
%ignore jsFileReader::readTraceHeader;

%feature("autodoc", "1");
%include ../jseisIO/src/jsFileReader.h
%include "../jseisIO/src/catalogedHdrEntry.h"
%include "../jseisIO/src/jsByteOrder.h"



