# pyjseisio SWIG interface file
# typemaps for jsFileReader

%extend jsIO::jsFileReader {

	%apply (int DIM1, float* ARGOUT_ARRAY1) 
		{(int arrayLength_reader, float* frame)};
	%apply (int DIM1, signed char* ARGOUT_ARRAY1) 
		{(int hdrArrayLength_reader, signed char* hdrBuf)};
	%typemap(typecheck) float* frame "";
	%typemap(typecheck) signed char* hdrBuf "";

	int _readFrameOnly(long frameIndex, int arrayLength_reader, float* frame){
		return ($self)->readFrame(frameIndex, frame, NULL);
	}

	int _readFrameAndHdrs(long frameIndex, 
                          int arrayLength_reader, 
                          float* frame,
                          int hdrArrayLength_reader,
                          signed char* hdrBuf){

		return ($self)->readFrame(frameIndex, frame, (char*)hdrBuf);
	}



	# rename other functions in favor of custom python wrappers
	%rename("_getHeaderWords") getHeaderWords;
	%rename("_getAxisLogicalValues") getAxisLogicalValues;
	%rename("_getAxisPhysicalValues") getAxisPhysicalValues;
	%rename("_getAxisLabels") getAxisLabels;
	%rename("_getAxisUnits") getAxisUnits;

}
