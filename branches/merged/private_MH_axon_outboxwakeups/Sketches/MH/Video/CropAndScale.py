#!/usr/bin/python


from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import Image


class CropAndScale(component):

    def __init__(self, newsize, cropbounds):
        super(CropAndScale,self).__init__()
        self.newsize = newsize
        self.cropbounds = cropbounds

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                frame = self.recv("inbox")
                newframe = self.processFrame(frame)
                self.send(newframe, "outbox")

            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg, "signal")
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    return

            self.pause()
            yield 1



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
