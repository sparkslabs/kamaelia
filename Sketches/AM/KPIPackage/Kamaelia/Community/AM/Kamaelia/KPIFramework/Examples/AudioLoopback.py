from AudioLib import *
from Kamaelia.Util.PipelineComponent import pipeline

pipeline(AudioSource(10),
         AudioEncoder('mp3'),
         AudioDecoder('mp3'),         
         SoundOutput()
        ).run()
