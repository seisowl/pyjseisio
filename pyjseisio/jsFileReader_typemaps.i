# pyjseisio SWIG interface file
# typemaps for jsFileReader

%extend jsIO::jsFileReader {

	%apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* frame)};
	%apply (int DIM1, signed char* ARGOUT_ARRAY1) 
		{(int hdrArrayLength_reader, signed char* hdrBuf)};

	%typemap(typecheck) float* frame "";
	%typemap(typecheck) signed char* hdrBuf "";

	int readFrameOnly(long frameIndex, int arrayLength_reader, float* frame){
		return ($self)->readFrame(frameIndex, frame, NULL);
	}

	int readFrameAndHdrs(long frameIndex, 
                         int arrayLength_reader, 
                         float* frame,
                         int hdrArrayLength_reader,
                         signed char* hdrBuf){

		return ($self)->readFrame(frameIndex, frame, (char*)hdrBuf);
	}

	int readHdrsOnly(long frameIndex, 
                     int hdrArrayLength_reader,
                     signed char* hdrBuf){

		return ($self)->readFrameHeader(frameIndex, (char*)hdrBuf);
	}

}
