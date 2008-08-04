#ifndef RingBuffer_H
#define RingBuffer_H
#include "Python.h"

class RingBuffer {
    private:
        double *_buffer;
        unsigned int _occupied, _size, _readPos, _writePos;
    public:
        RingBuffer(int size);
        ~RingBuffer();
        unsigned int vacant();
        unsigned int occupied();
        void write(double *data, unsigned int frames);
        void read(double *data, unsigned int frames);
        void readWithPad(double *data, unsigned int frames);
};
void importNumpy();
unsigned int numpyToC(double **data, PyObject *array);
#endif
