#include <Python.h>
#include "RtAudio.h"

void importNumpy();
int formatToType(RtAudioFormat format);
    
    
PyObject *bufferToArray(char *buffer, unsigned int bufferSize,
                       RtAudioFormat format);

char *arrayToBuffer(PyObject *array);
