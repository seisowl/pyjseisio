// pyjseisio SWIG interface file
// master interface file

%module pyjseisio_swig


%{
#define SWIG_FILE_WITH_INIT
#include "../src/jsFileReader.h"
#include "../src/jsFileWriter.h"
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

%pythoncode %{
import numpy as np
%}

// pyjseisio interface files
%include "vector_templates.i"
%include "jsFileReader_typemaps.i"
%include "jsFileWriter_typemaps.i"
%include "catalogedHdrEntry_typemaps.i"
%include "catalogedHdrEntry_pythonDefs.i"


%pythoncode %{
    def vectorToList(vector):
        return [vector[x] for x in range(vector.size())]
%}


%feature("autodoc", "1");
%include ../src/jsFileReader.h
%include ../src/jsFileWriter.h
%include "../src/jsByteOrder.h"
%include "../src/catalogedHdrEntry.h"

