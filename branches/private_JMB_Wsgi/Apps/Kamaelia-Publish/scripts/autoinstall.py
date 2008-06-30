import sys, zipfile, re
import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

def autoinstall(dkp_loc):
    prompt_text = 'It does not appear that Kamaelia Publish has been installed on your computer yet.  Would you like to do so now? [y/n]'
    if not prompt_yesno(prompt_text):
        print 'Kamaelia Publish must be installed to continue.  Halting.'
        sys.exit(1)
            
    zip = zipfile.ZipFile(sys.argv[0], 'r')
    
    corrupt = zip.testzip()
    if not corrupt:
        print 'The following files appear to be corrupted: \n', corrupt
        if not prompt_yesno('Would you like to continue anyway? [y/n]'):
            print "Halting!"
            sys.exit(1)
            
    namelist = zip.namelist()
    

def prompt_yesno(text):
    input = raw_input(text)
    if input[0] == 'y' or input[0] == 'Y':
        return True
    elif input[0] == 'n' or input[0] == 'N':
        return False
    else:
        print 'Unrecognizable input.  Please try again'
        return prompt_continue()
    
class NameSelector(component):
    def __init__(self, namelist, regex):
        self.inamelist = iter(namelist)
        self.regex = regex
        super(name_selector, self).__init__()
        
    def main(self):
        not_done = True
        while True:
            try:
                item = inamelist.next()
            except StopIteration:
                break
            
            if regex.search(item):
                self.send(item)
                
            yield 1
            
        self.send(producerFinished(self), 'signal')
        
class FileExtractor(component):
    def __init__(self, zip):
        self.zip = zip
        super(FileExtractor, self).__init__()
        
    def main(self):
        self.not_done = True  #variable is changed in self.handle_ctl_item
        
        while self.not_done:
            [self.handle_inbox_item(x) for x in self.getInbox('inbox')]          
            [self.handle_ctl_item(x) for x in self.getInbox('control')]
                    
            if not self.anyReady() and not_done:
                self.pause()
                
            yield 1
            
    def getInbox(self, name='inbox'):
        while self.dataReady(name):
            yield self.recv(name)
            
    def handle_inbox_item(self, item):
        data = self.zip.read(name)
        self.send(data)
        
    def handle_ctl_itm(self, item):
        if isinstance(item, producerFinished):
            self.not_done = False
        if isinstance(item, shutdownMicroprocess):
            self.not_done = False
            
class FileWriter(component):
    def __init__(self, path, regex):
        self.path = path
        self.regex = regex
        super(FileWriter, self).__init__()
        
    def main(self):
        self.not_done = False
        
        while self.not_done:
            