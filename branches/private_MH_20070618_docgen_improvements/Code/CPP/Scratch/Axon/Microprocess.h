#ifndef MICROPROCESS_H
#define MICROPROCESS_H
#include <string>
#include <stdexcept>

class SampleFailureError : public std::runtime_error
{
public:
  SampleFailureError() : runtime_error( "Bla Bla Bla error message" )
  {
  }
};
      
class Microprocess
{
public:

private:

}

#endif