from Axon.Component import component
from pymedia.audio import acodec
from pymedia.audio import sound
import struct

from Axon.Ipc import shutdownMicroprocess, producerFinished

class AudioDecoder(component):
    """pymedia audio decoder component

       Send coded audio data to the inbox, and decoded audio data frames
       (pymedia audio_frame objects) will be sent out the outbox.

       This component will shutdown in response to a producerFinished or
       shutdownMicroprocess message (received on 'control'). Immediately before
       shutting down, the message(s) are passed on (out of 'signal').
    """

    def __init__(self, extn):
        """Initialisation. Create a decoder for the specified codec.
           Codec is specified by file extension. Available codecs are
           listed in pymedia.audio.acodec.extensions.
        """
        super(AudioDecoder, self).__init__()

        self.codecid = acodec.getCodecID(extn)
        self.decoder = acodec.Decoder( {"id":self.codecid} )

        
    def main(self):
        done = False
        while not done:
            
            yield 1
            self.pause()

            while self.dataReady("inbox"):
                print "decoded sound"                
                data = self.recv("inbox")
                output = self.decoder.decode( data )
                if output:
                    self.send( output, "outbox" )

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, "signal")
                    done = True





class AudioEncoder(component):
    """pymedia audio encoder component

       Send raw audio data to the inbox, and encoded audio data frames
       (pymedia audio_frame objects) will be sent out the outbox.

       This component will shutdown in response to a producerFinished or
       shutdownMicroprocess message (received on 'control'). Immediately before
       shutting down, the message(s) are passed on (out of 'signal').
    """

    def __init__(self, extn):
        """Initialisation. Create a encoder for the specified codec.
           Codec is specified by file extension. Available codecs are
           listed in pymedia.audio.acodec.extensions.
        """
        super(AudioEncoder, self).__init__()
        cparams= { 'id': acodec.getCodecID( extn ), 'bitrate': 128000,
                   'sample_rate': 44100, 'channels': 1 }
        self.encoder = acodec.Encoder( cparams )

        
    def main(self):
        done = False
        while not done:
            
            yield 1
            self.pause()

            while self.dataReady("inbox"):
                print "encoding data"
                data = self.recv("inbox")
                output = self.encoder.encode( data )
                for fr in output:
                    self.send( fr, "outbox" )

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, "signal")
                    done = True




class AudioSource(component):
    """pymedia audio encoder component

       Send raw audio data to the inbox, and encoded audio data frames
       (pymedia audio_frame objects) will be sent out the outbox.

       This component will shutdown in response to a producerFinished or
       shutdownMicroprocess message (received on 'control'). Immediately before
       shutting down, the message(s) are passed on (out of 'signal').
    """

    def __init__(self, secs):
        """Initialisation. Create a encoder for the specified codec.
           Codec is specified by file extension. Available codecs are
           listed in pymedia.audio.acodec.extensions.
        """
        super(AudioSource, self).__init__()
        self.snd= sound.Input( 44100, 1, sound.AFMT_S16_LE )
        self.secs = secs

       
    def main(self):
        done = False
        self.snd.start()
        while not done:
            
            yield 1
            #self.pause()

            while self.snd.getPosition()<= self.secs:
                s = self.snd.getData()
                print "got sound data"
                if s and len( s ):
                    self.send(s, "outbox")
                yield 1
                        
            if self.snd.getPosition() >= self.secs:
                print "shutting down"
                self.snd.stop()
                msg = shutdownMicroprocess()
                self.send(msg, "signal")
                yield 1
                done = True
                



class SoundOutput(component):
    """pymedia sound output component

    Plays audio from received pymedia audio_frame objects.

    The sample_rate and channels parameters are taken from the audio_frame
    objects. The pymedia sound output object is therefore not created until
    the first audio_frame is received. If the parameters changed, then the
    sound output object is replaced.

    This component will shutdown in response to a producerFinished or
    shutdownMicroprocess message (received on 'control'). Immediately before
    shutting down, the message(s) are passed on (out of 'signal').
    """

    def __init__(self, audioformat = sound.AFMT_S16_LE):
        """Initialisation.

        afmt = raw audio data format. defaults to pymedia.audio.sound.AFMT_S16_LE
        """
        super(SoundOutput,self).__init__()

        self.audioformat = audioformat
        self.outputter = None
        self.channels = None
        self.sample_rate = None


    def main(self):
        done = False
        while not done:

            yield 1
            self.pause()

            while self.dataReady("inbox"):
                frame = self.recv("inbox")

                if not self.outputter or self.sample_rate != frame.sample_rate or self.channels != frame.channels:
                    self.sample_rate = frame.sample_rate
                    self.channels = frame.channels
                    self.outputter = sound.Output(self.sample_rate, self.channels, self.audioformat)

                self.outputter.play( frame.data )
                

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, "signal")
                    done = True

        

