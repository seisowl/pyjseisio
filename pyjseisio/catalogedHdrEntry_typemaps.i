// pyjseisio SWIG interface file
// typemaps for catalogedHdrEntry

%extend jsIO::catalogedHdrEntry {

	%apply (int DIM1, signed char* IN_ARRAY1) 
		{(int arrayLength, signed char* headerBuf)};
	%typemap(typecheck) signed char* headerBuf "";
	
	%apply (signed char* IN_ARRAY3, int DIM1, int DIM2, int DIM3) 
		{(signed char* headerBuf, int nFrames, int nTraces, int nBytesHeader)};
	%apply (float* INPLACE_ARRAY2, int DIM1, int DIM2) {(float* vals, int n1dummy, int n2dummy)};
	%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2) {(double* vals, int n1dummy, int n2dummy)};
	%apply (int* INPLACE_ARRAY2, int DIM1, int DIM2) {(int* vals, int n1dummy, int n2dummy)};
	%apply (short* INPLACE_ARRAY2, int DIM1, int DIM2) {(short* vals, int n1dummy, int n2dummy)};
	%apply (long* INPLACE_ARRAY2, int DIM1, int DIM2) {(long* vals, int n1dummy, int n2dummy)};

	void getFloatValsHelper(signed char* headerBuf, int nFrames, int nTraces, int nBytesHeader, float* vals, int n1dummy, int n2dummy){
		($self)->getFloatVals(headerBuf, vals, nBytesHeader, nTraces, nFrames);
	}

	void getDoubleValsHelper(signed char* headerBuf, int nFrames, int nTraces, int nBytesHeader, double* vals, int n1dummy, int n2dummy){
		($self)->getDoubleVals(headerBuf, vals, nBytesHeader, nTraces, nFrames);
	}

	void getIntValsHelper(signed char* headerBuf, int nFrames, int nTraces, int nBytesHeader, int* vals, int n1dummy, int n2dummy){
		($self)->getIntVals(headerBuf, vals, nBytesHeader, nTraces, nFrames);
	}

	void getShortValsHelper(signed char* headerBuf, int nFrames, int nTraces, int nBytesHeader, short* vals, int n1dummy, int n2dummy){
		($self)->getShortVals(headerBuf, vals, nBytesHeader, nTraces, nFrames);
	}

	void getLongValsHelper(signed char* headerBuf, int nFrames, int nTraces, int nBytesHeader, long* vals, int n1dummy, int n2dummy){
		($self)->getLongVals(headerBuf, vals, nBytesHeader, nTraces, nFrames);
	}

	float getFloatVal(int arrayLength, signed char* headerBuf){
		return ($self)->getFloatVal((char*)headerBuf);
	}

	double getDoubleVal(int arrayLength, signed char* headerBuf){
		return ($self)->getDoubleVal((char*)headerBuf);
	}

	int getIntVal(int arrayLength, signed char* headerBuf){
		return ($self)->getIntVal((char*)headerBuf);
	}

	short getShortVal(int arrayLength, signed char* headerBuf){
		return ($self)->getShortVal((char*)headerBuf);
	}

	long getLongVal(int arrayLength, signed char* headerBuf){
		return ($self)->getLongVal((char*)headerBuf);
	}


	int setFloatVal(int arrayLength, signed char* headerBuf, float val){
		return ($self)->setFloatVal((char*)headerBuf, val);
	}

	int setDoubleVal(int arrayLength, signed char* headerBuf, double val){
		return ($self)->setDoubleVal((char*)headerBuf, val);
	}

	int setIntVal(int arrayLength, signed char* headerBuf, int val){
		return ($self)->setIntVal((char*)headerBuf, val);
	}

	int setShortVal(int arrayLength, signed char* headerBuf, short val){
		return ($self)->setShortVal((char*)headerBuf, val);
	}

	int setLongVal(int arrayLength, signed char* headerBuf, long val){
		return ($self)->setLongVal((char*)headerBuf, val);
	}
}

