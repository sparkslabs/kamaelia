#!/usr/bin/python


from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

import Image


class CropAndScale(component):

    def __init__(self, newsize, cropbounds):
        super(CropAndScale,self).__init__()
        self.newsize = newsize
        self.cropbounds = cropbounds[0], cropbounds[3], cropbounds[2], cropbounds[1]

    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise "STOP"

    def main(self):
        self.shutdownMsg = None
        i=0
        try:
            while 1:
                while self.dataReady("inbox"):
                    frame = self.recv("inbox")
                    newframe = self.processFrame(frame)
                    for _ in self.waitSend(newframe, "outbox"):
                        yield _
                    print i
                    i+=1
    
                if self.canStop():
                    raise "STOP"
    
                self.pause()
                yield 1
        except "STOP":
            self.send(self.shutdownMsg,"signal")


    def processFrame(self, frame):
        if frame['pixformat'] == "RGB_interleaved":
            mode = "RGB"
            datakey = "rgb"
        elif frame['pixformat'] == "RGBA_interleaved":
            mode = "RGBA"
            datakey = "rgb"
        elif frame['pixformat'] == "Y_planar":
            mode = "L"
            datakey = "yuv"
        else:
            raise "Can't process images with pixformat '"+frame['pixformat']+"'"

        img = Image.frombuffer(mode, frame['size'], frame[datakey])
        newimg = img.transform(self.newsize,
                                Image.EXTENT,
                                self.cropbounds,
                                Image.BICUBIC)
        newrgb = newimg.tostring()
        
        newframe = {}
        for key in frame.keys():
            newframe[key] = frame[key]
        newframe[datakey] = newrgb
        newframe['size'] = self.newsize
    
        return newframe
