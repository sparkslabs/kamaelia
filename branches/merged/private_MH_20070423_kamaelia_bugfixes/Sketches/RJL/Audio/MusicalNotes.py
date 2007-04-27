from Axon.Component import component
from types import ListType

class MusicalNoteToFrequency(component):
    def __init__(self):
        super(MusicalNoteToFrequency, self).__init__()
        
        fullscale = ["A", ["A#","Bb"], "B", "C", ["C#","Db"], "D", ["D#","Eb"], "E", "F", ["F#", "Gb"], "G", ["G#", "Ab"]]
        self.notetofreq = {}
        noteid = 0
        currentfreq = 27.5
        geometricratio = pow(2, 1.0 / 12.0)
        
        for note in fullscale:
            if isinstance(note, ListType):
                for notename in note:
                    self.notetofreq = { notename: currentfreq }
            else:
                self.notetofreq = { note: currentfreq }
            
            currentfreq *= geometricratio
            
        self.octavemultiplier = (1, 2, 4, 8, 16, 32, 64, 128, 256)
    
    def noteToFrequency(self, note):
        if isinstance(note, str):
            notename = note[:-1]
            octave = int(note[-1:])
            return self.octavemultiplier[octave] * self.notetofreq[notename]
            
        else: #int
            return 27.5 * pow(2.0, (note - 1) / 12.0)
            
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                note = self.recv("inbox")
                #print note
                self.send(self.noteToFrequency(note), "outbox")
            self.pause()
