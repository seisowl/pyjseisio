# pyjseisio SWIG interface file
# typemaps for jsFileReader

%extend jsIO::jsFileReader {

	%apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* frame)};
	%apply (int DIM1, signed char* ARGOUT_ARRAY1) 
		{(int hdrArrayLength_reader, signed char* hdrBuf)};

	%typemap(typecheck) float* frame "";
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


# supplementary methods

	int readFrameDataOnly(long frameIndex, int arrayLength_reader, float* frame){
		return ($self)->readFrame(frameIndex, frame, NULL);
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

}
