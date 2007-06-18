#ifndef MICROPROCESSTEST_H
#define MICROPROCESSTEST_H

#include <cppunit/extensions/HelperMacros.h>
#include "Microprocess.h"

class MicroprocessTest : public CppUnit::TestFixture
{
  CPPUNIT_TEST_SUITE( MicroprocessTest );
  CPPUNIT_TEST( testConstructor );
  CPPUNIT_TEST_EXCEPTION( testExampleThrow, SampleFailureError );
  CPPUNIT_TEST_SUITE_END();
            
public:
  void setUp();
  void tearDown();
  void testConstructor();
  void testExampleThrow();
};

#endif  // MICROPROCESSTEST_H
