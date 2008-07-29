%Module RtAudio 0

%ModuleHeaderCode
#include "Python.h"
#include "RtAudio.h"
#include "NumpyInterface.h"
#include <vector>
%End

%PostInitialisationCode
importNumpy();
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
        
        // The array dimensions
        PyObject *outputArray, *inputArray;
        outputArray = Py_None;
        inputArray = Py_None;
        unsigned int outputBufferSize, inputBufferSize;

        callbackData *data = (callbackData *)userData;

        outputBufferSize = nFrames * data->outputChannels;
        inputBufferSize = nFrames * data->inputChannels;
        
        PyGILState_STATE state;
        state = PyGILState_Ensure();
        char *outBuffer = (char *)outputBuffer;

        if (inputBuffer != NULL) {
            inputArray = bufferToArray((char *)inputBuffer, inputBufferSize,
                                        data->format);
        }

        else {
            inputArray = NULL;
        }

        // TODO:Make me send RtAudioStreamStatus properly
        //printf("Frames: %i Time: %f\n", nFrames, streamTime);
        PyObject *result;

//        std::cout << PyEval_GetFuncName(data->function) << std::endl;
        result = PyEval_CallFunction(data->function, "OidOO", inputArray,
                            nFrames, streamTime, Py_None,
                            data->param);
        PyObject *error = PyErr_Occurred();
        if (error) {
            PyErr_Print();
        }

        outBuffer = arrayToBuffer(result);
//        std::cout << outBuffer[0] << std::endl;
        
        PyGILState_Release(state);
        
        return 0;
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

    callbackData *data = (callbackData *) calloc(1, sizeof(callbackData));

    data->function = a9;
    data->param = a10;
    data->format = a6;
    data->outputChannels = outputParameters.nChannels;
    data->inputChannels = inputParameters.nChannels;


    // TODO: Handle stream options dict
    RtAudio::StreamOptions streamOptions;
    
    Py_BEGIN_ALLOW_THREADS
    sipCpp->openStream(&outputParameters, &inputParameters, a6, a7,
                       &a8, streamCallback, (void *)data, &streamOptions);
    Py_END_ALLOW_THREADS
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

};


