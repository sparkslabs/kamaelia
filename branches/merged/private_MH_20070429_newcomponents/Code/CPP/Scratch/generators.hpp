#ifndef GENERATORS_HPP
#define GENERATORS_HPP

class StopIteration { };

class Generator {
  protected:
    int __generator_state;
  public:
    Generator()  {     };
    ~Generator() {     };
};

// #define GENERATOR struct
#define GENERATOR_CODE_START  if (this->__generator_state == -1)      \
                     { throw StopIteration(); }         \
                     switch(this->__generator_state)         \
                     { default:
#define YIELD(v)         this->__generator_state = __LINE__; \
                         return (v);                         \
                         case __LINE__:
#define GENERATOR_CODE_END     };                                      \
                     this->__generator_state = -1; throw StopIteration();
#endif
