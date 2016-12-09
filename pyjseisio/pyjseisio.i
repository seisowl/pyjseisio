# pyjseisio SWIG interface file
# master interface file

%module pyjseisio


%{
#define SWIG_FILE_WITH_INIT
#include "../src/jsFileReader.h"
#include "../src/jsByteOrder.h"
#include "../src/catalogedHdrEntry.h"
using namespace jsIO;
%}


%include <std_string.i>
%include <std_vector.i>
%include <typemaps.i>
%include "numpy.i"


%init %{
import_array();
%}


# pyjseisio interface files
%include "vector_templates.i"
%include "jsFileReader_typemaps.i"
%include "catalogedHdrEntry_typemaps.i"
%include "catalogedHdrEntry_pythonDefs.i"


%pythoncode %{
    def vectorToList(vector):
        return [vector[x] for x in xrange(vector.size())]
%}


%feature("autodoc", "1");
%include ../src/jsFileReader.h
%include "../src/catalogedHdrEntry.h"
%include "../src/jsByteOrder.h"



