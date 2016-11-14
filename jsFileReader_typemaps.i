# pyjseisio SWIG interface file
# typemaps for jsFileReader

%extend jsIO::jsFileReader {

	# rename overloaded functions
	%rename("_readFrame") readFrame;
	%rename("_readFrameAndHdrs") readFrame(const long, float *, char *);
	%rename("_readFrameOnly") readFrame(const long, float *);

	# rename other functions in favor of custom python wrappers
	%rename("_getHeaderWords") getHeaderWords;
	%rename("_getAxisLogicalValues") getAxisLogicalValues;
	%rename("_getAxisPhysicalValues") getAxisPhysicalValues;
	%rename("_getAxisLabels") getAxisLabels;
	%rename("_getAxisUnits") getAxisUnits;
	

	%typemap(in, fragment="NumPy_Fragments") (char* headbuf)
	(PyObject* header = NULL)
	{
		// Allocate Numpy array for header
		npy_intp hdrDims[2];
		hdrDims[0] = (npy_intp) arg1->getAxisLen(1)*arg1->getNumBytesInHeader();
		header = PyArray_SimpleNew(1, hdrDims, NPY_BYTE);
		if (!header) SWIG_fail;
		$1 = (char*) array_data(header);
	}

	%typemap(argout) (char* headbuf)
	{
	  $result = SWIG_Python_AppendOutput($result,(PyObject*)header$argnum);
	}

	%typemap(in, fragment="NumPy_Fragments") (float *frame)
	(PyObject* array = NULL)
	{
		// Allocate Numpy array for data
		npy_intp dims[2];
		dims[0] = (npy_intp) arg1->getAxisLen(0)*arg1->getAxisLen(1);
		array = PyArray_SimpleNew(1, dims, NPY_FLOAT);
		if (!array) SWIG_fail;
		$1 = (float*) array_data(array);
	}

	%typemap(argout) (float *frame)
	{
	  $result = SWIG_Python_AppendOutput($result,(PyObject*)array$argnum);
	}


	%typemap(typecheck) float* frame "";
	%typemap(typecheck) char* headbuf "";
}
