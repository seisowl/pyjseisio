# pyjseisio SWIG interface file
# typemaps for jsFileReader

%extend jsIO::jsFileReader {

	%apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* frame)};
    %apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* trace)};
	%apply (int DIM1, signed char* ARGOUT_ARRAY1) 
		{(int hdrArrayLength_reader, signed char* hdrBuf)};
	%apply (int DIM1, signed char* IN_ARRAY1) 
		{(int posLength_reader, int* position_reader)};


	%typemap(typecheck) float* frame "";
	%typemap(typecheck) float* trace "";
	%typemap(typecheck) int* position_reader "";
	%typemap(typecheck) signed char* hdrBuf "";
	%typemap(typecheck) headerWordInfo* pInfo "";

    %typemap(in) headerWordInfo *pInfo{
        /* headerWordInfo argin */
        $1 = new headerWordInfo[(arg1)->getNumHeaderWords()];
    };

    %typemap(argout) headerWordInfo *pInfo{
        /* headerWordInfo argout */
        for(int i=0; i<(arg1)->getNumHeaderWords(); i++){
        PyObject* next = (PyObject*)SWIG_NewPointerObj(SWIG_as_voidptr(&$1[i]), 
                                            SWIGTYPE_p_jsIO__headerWordInfo, 
                                            0 );
            $result = SWIG_Python_AppendOutput($result, next);
        }
    };


# allow use of the int* _position methods
    %typemap(in) int* position_reader{
        /* parse position information from incoming tuple */
        int ndim = arg1->getNDim();
        int* pos = new int[ndim-2];
        std::cout << "ndim = " << ndim << "\n";
        if (PyTuple_Check($input)) {
            int tester = 0;
            SWIG_AsVal_int(PyTuple_GET_ITEM($input,0),&tester);
            std::cout << "test get item 0: " << tester << "\n";
            std::cout << "the size of the tuple is: " << PyTuple_GET_SIZE($input) << "\n";
            int parseResult = 0;
            switch(ndim){
                case 3:
                    parseResult = PyArg_ParseTuple($input,"i",pos);
                    std::cout << "my parseResult3 = " << parseResult << "\n";
                    break;
                case 4:
                    parseResult = PyArg_ParseTuple($input,"ii",pos, pos+1);
                    std::cout << "my parseResult4 = " << parseResult << "\n";
                    break;                   
                case 5:
                    parseResult = PyArg_ParseTuple($input,"iii",pos, pos+1, pos+2);
                    std::cout << "my parseResult5 = " << parseResult << "\n";
                    break;
            }
            if (!parseResult) {
              PyErr_SetString(PyExc_TypeError,"tuple must have nDim-2 elements");
              return NULL;
            }
            $1 = &pos[0];
            for(int i=0; i<(ndim-2); i++)
                std::cout << "$1[" << i << "] = " << $1[i] << "\n";
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

    long getFrameIndexPlease(int* position_reader){
        return ($self)->getFrameIndex(position_reader);
    };

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

	int readFrameHdrsOnly(long frameIndex, 
                     int hdrArrayLength_reader,
                     signed char* hdrBuf){

		return ($self)->readFrameHeader(frameIndex, (char*)hdrBuf);
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
