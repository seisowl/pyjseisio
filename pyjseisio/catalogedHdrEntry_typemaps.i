# pyjseisio SWIG interface file
# typemaps for catalogedHdrEntry

%extend jsIO::catalogedHdrEntry {

	%apply (int DIM1, signed char* INPLACE_ARRAY1) 
		{(int arrayLength, signed char* headerBuf)};
	%typemap(typecheck) signed char* headerBuf "";

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

