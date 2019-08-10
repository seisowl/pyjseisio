// pyjseisio SWIG interface file
// typemaps for jsFileWriter

%extend jsIO::jsFileWriter {

        %apply (float* IN_ARRAY1, int DIM1) 
		{(float* frame, int arrayLength_reader)};
        %apply (float* IN_ARRAY1, int DIM1) 
		{(float* trace, int arrayLength_reader)};
        %apply (signed char* IN_ARRAY1, int DIM1) 
		{(signed char* hdrBuf, int hdrArrayLength_reader)};
        %apply (float* IN_ARRAY1, int DIM1) 
		{(float* frames, int arrayLength_reader)};

// ignore typechecking for these specific argumentes
        %typemap(typecheck) float* frame "";
        %typemap(typecheck) float* frames "";
        %typemap(typecheck) float* trace "";
        %typemap(typecheck) int* position_reader "";
        %typemap(typecheck) signed char* hdrBuf "";
        %typemap(typecheck) headerWordInfo* pInfo "";


// allow use of the int* _position methods with tuples
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

// supplementary methods
//%ignore leftJustify(float* frame, char* headbuf, int numTraces);

   int leftJustify(float* frame,
                   int arrayLength_reader, 
                   signed char* hdrBuf,
                   int hdrArrayLength_reader,
                   int  numTraces) {
       return ($self)->leftJustify(frame, (char*)hdrBuf, numTraces);
   };

   int writeFrame(long frameindex,
                   float* frame,
                   int arrayLength_reader, 
                   signed char* hdrBuf,
                   int hdrArrayLength_reader,
                   int  numTraces) {
       return ($self)->writeFrame(frameindex, frame, (char*)hdrBuf, numTraces);
   };
                    
   int writeFrame(int* position,
                   float* frame,
                   int arrayLength_reader, 
                   signed char* hdrBuf,
                   int hdrArrayLength_reader,
                   int  numTraces) {
       return ($self)->writeFrame(position, frame, (char*)hdrBuf, numTraces);
   };

   int writeFrame(long frameindex,
                   float* frame,
                   int arrayLength_reader,
                   signed char* hdrBuf,
                   int hdrArrayLength_reader) {
       return ($self)->writeFrame(frameindex, frame, (char*)hdrBuf);
   };

   int writeFrame(int* position,
                   float* frame,
                   int arrayLength_reader,
                   signed char* hdrBuf,
                   int hdrArrayLength_reader) {
       return ($self)->writeFrame(position, frame, (char*)hdrBuf);
   };

   int writeFrame(int* position,
                   float* frame,
                   int arrayLength_reader) {
       return ($self)->writeFrame(position, frame);
   };

   int writeFrame(long frameindex,
                   float* frame,
                   int arrayLength_reader) {
       return ($self)->writeFrame(frameindex, frame);
   };
                    
}
