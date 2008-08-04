#include <iostream>
#include "Python.h"
#include "RingBuffer.h"
#include <numpy/arrayobject.h>

RingBuffer::RingBuffer(int size):_size(size) {
    import_array();
    _buffer = new double[size];
    _occupied = 0;
    _readPos = 0;
    _writePos = 0;
}

RingBuffer::~RingBuffer() {
    delete [] _buffer;
}
    

unsigned int RingBuffer::vacant() {
    return _size - _occupied;
}

unsigned int RingBuffer::occupied() {
    return _occupied;
}

void RingBuffer::write(double *data, unsigned int frames) {
    if (frames <= vacant()) {
        for (unsigned int i=0; i<frames; i++) {
            // Slow - speed me up using memcpy
            _buffer[_writePos] = data[i];
            _writePos = _writePos + 1;
            if (_writePos == _size) {
                _writePos = 0;
            }
        }
        _occupied = _occupied + frames;
    }
}

void RingBuffer::read(double *data, unsigned int frames) {
    if (frames <= occupied()) {
        for (unsigned int i=0; i<frames; i++) {
            data[i] = _buffer[_readPos];
            std::cout << data[i] << std::endl;
            _readPos = _readPos + 1;
            if (_readPos == _size) {
                _readPos = 0;
            }
        }
        _occupied = _occupied - frames;
    }
}

void RingBuffer::readWithPad(double *data, unsigned int frames) {
    if (frames <= occupied()) {
        read(data, frames);
    }
    else {
        std::cout << "Underrun" << std::endl;
        // Not enough in the buffer so pad with zeros
        unsigned int padSize = frames - occupied();
        read(data, occupied());
        for (unsigned int i=0; i<padSize; i++) {
            data[frames - i - 1] = 0;
        }
    }
}


void importNumpy() {
    import_array();
}

unsigned int numpyToC(double **data, PyObject *array) {
    PyArrayObject *arrayObj = (PyArrayObject *)PyArray_GETCONTIGUOUS((PyArrayObject *)array);
    unsigned int frames = PyArray_SIZE(arrayObj);
    *data = (double *)malloc(frames * sizeof(double));
    memcpy(*data, PyArray_BYTES(arrayObj), frames * sizeof(double));
    return frames;
}
