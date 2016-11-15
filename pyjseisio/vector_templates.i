# Set up proxy classes for std::vectors
%template(DoubleVector) std::vector<double>;
%template(LongVector) std::vector<long>;
%template(StringVector) std::vector<std::string>;
%template(CatalogedHdrEntryVector) std::vector<jsIO::catalogedHdrEntry>;

