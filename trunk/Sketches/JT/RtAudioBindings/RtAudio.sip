%Module RtAudio 0


class RtAudio
{
%TypeHeaderCode
#include "RtAudio.h"
#include "Numeric/arrayobject.h"
%End
public:

    enum Api {
        UNSPECIFIED,
        LINUX_ALSA,
        LINUX_OSS,
        UNIX_JACK,
        MACOSX_CORE,
        WINDOWS_ASIO,
        WINDOWS_DS,
        RTAUDIO_DUMMY
    };


    RtAudio(RtAudio::Api api=UNSPECIFIED);

    ~RtAudio();

// TODO: Make this a proper function returning a list :)
//    static void getCompiledApi();

        
        
    RtAudio::Api getCurrentApi();

    unsigned int getDeviceCount();

    unsigned int getDefaultOutputDevice();

    unsigned int getDefaultInputDevice();


%TypeCode

    static int formatToType(unsigned long format) {
        switch (format) {
            case RTAUDIO_SINT8:
                return PyArray_SHORT;     
            case RTAUDIO_SINT16:
                return PyArray_SHORT;
            case RTAUDIO_SINT24:
                // Numpy has no Int24 type, so use Int32 instead
                return PyArray_SHORT;
            case RTAUDIO_SINT32:
                return PyArray_SHORT;
            case RTAUDIO_FLOAT32:
                return PyArray_DOUBLE;
            case RTAUDIO_FLOAT64:
                return PyArray_DOUBLE;
        }
        return -1;
    }

    
    typedef struct callbackData {
        PyObject *function;
        PyObject *param;
        unsigned long format;
        unsigned int outputChannels;
        unsigned int inputChannels;
    };

    int streamCallback(void *outputBuffer, void *inputBuffer,
                       unsigned int nFrames, double streamTime,
                       RtAudioStreamStatus status,
                       void *userData) {
        // Numpy arrays for the input and output
        PyArrayObject *outputArray, *inputArray;
        // The array dimensions
        int outputDims[1], inputDims[1];
        
        struct callbackData *data = (callbackData *)userData;

        outputDims[0] = nFrames * data->outputChannels;
        inputDims[0] = nFrames * data->inputChannels;

        if (outputBuffer != NULL) {
            outputArray = (PyArrayObject *)
                              PyArray_FromDimsAndData(1, outputDims,
                                                 formatToType(data->format),
                                                      (char *) outputBuffer);
        }

        inputArray = (PyArrayObject *)
                          PyArray_FromDimsAndData(1, inputDims,
                                                  formatToType(data->format),
                                                  (char *) inputBuffer);
        // TODO:Make me send RtAudioStreamStatus properly
        PyObject *args = Py_BuildValue("(OOidO)", outputArray, inputArray,
                                        nFrames, streamTime, data->param);
        PyEval_CallObject(data->function, args);
        return 1;
    }
    
%End
    
    // TODO: Make some way to actually get at the buffer :D
    void openStream(unsigned int outputDevice,
                    unsigned int outputChannels,
                    unsigned int firstOutputChannel,
                    unsigned int inputDevice,
                    unsigned int inputChannels,
                    unsigned int firstInputChannel,
                    unsigned long format,
                    unsigned int sampleRate, unsigned int bufferSize,
                    SIP_PYCALLABLE callback, SIP_PYOBJECT userData);

//                   SIP_PYDICT streamOptions);

%MethodCode
    // Convert parameters to structs
    RtAudio::StreamParameters outputParameters;
    RtAudio::StreamParameters inputParameters;

    outputParameters.deviceId = a0;
    outputParameters.nChannels = a1;
    outputParameters.firstChannel = a2;

    inputParameters.deviceId = a3;
    inputParameters.nChannels = a4;
    inputParameters.firstChannel = a5;

    struct callbackData data;
    data.function = a9;
    data.param = a10;
    data.format = a6;
    data.outputChannels = outputParameters.nChannels;
    data.inputChannels = inputParameters.nChannels;

    // TODO: Handle stream options dict
    RtAudio::StreamOptions streamOptions;

    sipCpp->openStream(&outputParameters, &inputParameters, a6, a7,
                       &a8, &streamCallback, (void *) &data, &streamOptions);

%End

    void closeStream();

    void startStream();

    void abortStream();

    bool isStreamOpen();

    bool isStreamRunning();

    double getStreamTime();

    long getStreamLatency();

    void showWarnings(bool value = true);

};


