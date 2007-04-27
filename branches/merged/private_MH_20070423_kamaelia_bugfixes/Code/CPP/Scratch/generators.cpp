/*
 *
 * Sample generator test in C++
 *
 */

#include "generators.hpp"
#include <iostream>

using namespace std;

struct Counter : public Generator {
    int i;
    int next() {
    GENERATOR_CODE_START
        for (i=0; i<10; i++) {
            YIELD(i);
        };
        YIELD(2);
    GENERATOR_CODE_END
    };
};

int main(int, char **) {
    Counter a[10];
    for(int i=0; i<12; i++) {
        for(int j=0; j<10; j++) {
            try {
                cout << "Yield in C++ generator:"<< j<< " value:" << (a[j]).next() << endl;
            } catch(StopIteration null){
                cout << " Exception Caught" << "...\n";
            }
        };
    }
    return 0;
}
