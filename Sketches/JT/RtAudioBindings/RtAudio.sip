%Module RtAudio 0

%ModuleHeaderCode
#include "Python.h"
#include "RtAudio.h"
#include <vector>
#include "RingBuffer.h"
%End

class RtAudio
{

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
%TypeCode
    RingBuffer buffer(1024*4);
%End

    RtAudio(RtAudio::Api api=UNSPECIFIED);

    ~RtAudio();

    SIP_PYLIST getCompiledApi();
%MethodCode
    std::vector<RtAudio::Api> apiVec;
    PyObject *apiList;

    Py_BEGIN_ALLOW_THREADS
    sipCpp->getCompiledApi(apiVec);
    Py_END_ALLOW_THREADS
    if ((apiList = PyList_New(apiVec.size())) == NULL) {
        return NULL;
    }

    for (unsigned int i=0; i < apiVec.size(); i++) {
        PyList_SET_ITEM(apiList, i, PyInt_FromLong(apiVec.at(i)));
    }
    return (PyObject *) apiList;
%End

        
        
    RtAudio::Api getCurrentApi();

    unsigned int getDeviceCount();

    SIP_PYDICT getDeviceInfo(unsigned int device=0);
%MethodCode
    RtAudio::DeviceInfo deviceInfo = sipCpp->getDeviceInfo(a0);

    // Convert booleans to PyTrue or PyFalse
    PyObject *probed;
    PyObject *isDefaultOutput;
    PyObject *isDefaultInput;

    if (deviceInfo.probed) {
        probed = Py_True;
    }
    else {
        probed = Py_False;
    }

    if (deviceInfo.isDefaultOutput) {
        isDefaultOutput = Py_True;  
    }
    else {
        isDefaultOutput = Py_False;
    }

    if (deviceInfo.isDefaultInput) {
        isDefaultInput = Py_True;    
        }
    else {
        isDefaultInput = Py_False;
    }

    // Convert vector of supported sample rates to a list
    PyObject *sampleRateList = PyList_New(deviceInfo.sampleRates.size());

    for (unsigned int i=0; i < deviceInfo.sampleRates.size(); i++) {
        PyList_SET_ITEM(sampleRateList, i,
                        PyInt_FromLong(deviceInfo.sampleRates.at(i)));
    }

    PyObject *infoTuple = Py_BuildValue("{s:O,s:s,s:i,s:i,s:i}",
                                        "probed", probed,
                                        "name", deviceInfo.name.c_str(),
                                        "outputChannels",
                                        deviceInfo.outputChannels,
                                        "inputChannels",
                                        deviceInfo.inputChannels,
                                        "duplexChannels",
                                        deviceInfo.duplexChannels,
                                        "isDefaultOutput",
                                        isDefaultOutput,
                                        "isDefaultInput",
                                        isDefaultInput);
    return infoTuple;

%End

    unsigned int getDefaultOutputDevice();

    unsigned int getDefaultInputDevice();


%TypeCode

    int streamCallback(void *outputBuffer, void *inputBuffer,
                       unsigned int nFrames, double streamTime,
                       RtAudioStreamStatus status,
                       void *userData) {
        // More copying than needed, but meh
        double *data;
        data = new double[nFrames];
        buffer.readWithPad(data, nFrames);

        memcpy(outputBuffer, data, nFrames * sizeof(double));
        delete[] data;
        data = NULL;
        return 0;
    }
    
%End
    
    void openStream(unsigned int device,
                    unsigned int sampleRate,
                    unsigned int bufferSize);

%MethodCode
    // Convert parameters to structs
    RtAudio::StreamParameters outputParameters;

    outputParameters.deviceId = a0;
    outputParameters.nChannels = 1;
    outputParameters.firstChannel = 0;

    RtAudio::StreamOptions streamOptions;
    
    sipCpp->openStream(&outputParameters, NULL, 0x20, a1, &a2,
                       streamCallback, NULL, &streamOptions);
%End

    void closeStream();

    void startStream();

    void stopStream();

    void abortStream();

    bool isStreamOpen();

    bool isStreamRunning();

    double getStreamTime();

    long getStreamLatency();

    void showWarnings(bool value = true);

    void write(SIP_PYOBJECT array);
%MethodCode
        double *data;
        unsigned int frames;
        // The data array is initialized (via malloc) when converting from the
        // numpy array...
        frames = numpyToC(&data, a0);
        buffer.write(data, frames);
        // ...so we need to free it here
        free(data);
        data = NULL;
%End

    unsigned int needWrite();
%MethodCode
        return PyInt_FromLong(buffer.vacant());
%End

};


