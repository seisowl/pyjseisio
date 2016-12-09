# pyjseisio SWIG interface file
# typemaps for jsFileReader

%extend jsIO::jsFileReader {

# numpy.i interfaces to return numpy arrays
	%apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* frame)};
    %apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* trace)};
	%apply (int DIM1, signed char* ARGOUT_ARRAY1) 
		{(int hdrArrayLength_reader, signed char* hdrBuf)};


# ignore typechecking for these specific argumentes
	%typemap(typecheck) float* frame "";
	%typemap(typecheck) float* trace "";
	%typemap(typecheck) int* position_reader "";
	%typemap(typecheck) signed char* hdrBuf "";
	%typemap(typecheck) headerWordInfo* pInfo "";


# typemaps to return a list of header words infos
    %typemap(in) headerWordInfo *pInfo{
        /* headerWordInfo argin */
        $1 = new headerWordInfo[(arg1)->getNumHeaderWords()];
    };

    %typemap(argout) headerWordInfo *pInfo{
        /* headerWordInfo argout */
        for(int i=0; i<(arg1)->getNumHeaderWords(); i++){
            PyObject* next = (PyObject*)SWIG_NewPointerObj(
                                            SWIG_as_voidptr(&$1[i]), 
                                            SWIGTYPE_p_jsIO__headerWordInfo, 
                                            0 );
            $result = SWIG_Python_AppendOutput($result, next);
        }
    };


# allow use of the int* _position methods with tuples
    %typemap(in) int* position_reader{
        /* parse position information from incoming tuple */
        int ndim = arg1->getNDim();
        int* pos = new int[ndim-2];
        if (PyTuple_Check($input)) {
            int parseResult = 0;
            switch(ndim){
                case 3:
                    parseResult = PyArg_ParseTuple($input,"i",pos);
                    break;
                case 4:
                    parseResult = PyArg_ParseTuple($input,"ii",pos, pos+1);
                    break;                   
                case 5:
                    parseResult = PyArg_ParseTuple($input,"iii",pos, pos+1, pos+2);
                    break;
            }
            if (!parseResult) {
              PyErr_SetString(PyExc_TypeError,"tuple must have nDim-2 elements");
              return NULL;
            }
            $1 = &pos[0];
          } else {
            PyErr_SetString(PyExc_TypeError,"expected a tuple.");
            return NULL;
          }
    };

    %typemap(freearg) int* position_reader{
        /* free memory allocated for pos */
        delete[] $1;
    };


# supplementary methods

	int readFrameDataOnly(long frameIndex, 
                          int arrayLength_reader, 
                          float* frame){
		return ($self)->readFrame(frameIndex, frame, NULL);
	}

	int readFrameDataOnly(int* position_reader, 
                          int arrayLength_reader,
                          float* frame){
		return ($self)->readFrame(position_reader, frame, NULL);
	}

	int readFrameDataAndHdrs(long frameIndex, 
                         int arrayLength_reader, 
                         float* frame,
                         int hdrArrayLength_reader,
                         signed char* hdrBuf){

		return ($self)->readFrame(frameIndex, frame, (char*)hdrBuf);
	}

	int readFrameDataAndHdrs(int* position_reader, 
                         int arrayLength_reader, 
                         float* frame,
                         int hdrArrayLength_reader,
                         signed char* hdrBuf){

		return ($self)->readFrame(position_reader, frame, (char*)hdrBuf);
	}

	int readFrameHdrsOnly(long frameIndex, 
                     int hdrArrayLength_reader,
                     signed char* hdrBuf){

		return ($self)->readFrameHeader(frameIndex, (char*)hdrBuf);
	}

	int readFrameHdrsOnly(int* position_reader, 
                     int hdrArrayLength_reader,
                     signed char* hdrBuf){

		return ($self)->readFrameHeader(position_reader, (char*)hdrBuf);
	}

    // THIS IS NOT WORKING RIGHT!!!
    // Headers are reading wrong
	int readTraceDataAndHdr(long traceIndex, 
                               int arrayLength_reader, 
                               float* trace,
                               int hdrArrayLength_reader,
                               signed char* hdrBuf){
        ($self)->readTraceHeader(traceIndex, (char*)hdrBuf);
		return ($self)->readTrace(traceIndex, trace);
	}

    int readTraceHeadersOnly(long traceIndex, 
                               long numTraces, 
                               int hdrArrayLength_reader,
                               signed char* hdrBuf){
        return ($self)->readTraceHeaders(traceIndex, numTraces, (char*)hdrBuf);
    }

	int readTracesDataOnly(long traceIndex, 
                            long numTraces, 
                            int arrayLength_reader, 
                            float* trace){
        return ($self)->readTraces(traceIndex, numTraces, trace);
	}

}
