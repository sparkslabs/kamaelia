import sys, zipfile, re, os, tarfile, cStringIO, shutil

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline

from console_io import prompt_yesno

def autoinstall(zip, dir):
    prompt_text = 'It does not appear that Kamaelia Publish has been installed.  Would you like to do so now? [y/n]'    
    if not prompt_yesno(prompt_text):
        print 'Kamaelia Publish must be installed to continue.  Halting.'
        sys.exit(1)
    
    tar_mem = cStringIO.StringIO( zip.read('data/kpuser.tar') )
    kpuser_file = tarfile.open(fileobj=tar_mem, mode='r')
    kpuser_file.extractall(path=dir)
    
    kpuser_file.close()
    tar_mem.close()
    
    shutil.move(dir + '/data/kpuser', dir + '/kpuser')
    shutil.move(dir + '/data/kp.ini', dir + '/kp.ini')

class AutoInstallBase(component):
    MethodText = 'handle_'
    ShutDownConditions = (producerFinished, shutdownMicroprocess)
    DataInZip = 'data/kpuser'
    def __init__(self, **argd):
        super(AutoInstallBase, self).__init__(**argd)
        self.not_done = True
        
    def main(self):
        while self.not_done:
            for box in self.inboxes:
                method_name = self.MethodText + box
                if hasattr(self, method_name):
                    print type(self)
                    self.method = getattr(self, method_name)
                    [self.method(x) for x in self.getInbox(box)]
                    
            if (not self.anyReady()) and self.not_done:
                self.pause()
                
            yield 1
        
    def getInbox(self, name='inbox'):
        while self.dataReady(name):
            yield self.recv(name)
            
    def handle_control(signal):
        if isinstance(signal, self.ShutDownConditions):
            self.not_done = False
            self.send(signal, 'signal')
    
class NameSelector(component):
    DataInZip = 'data/kpuser'
    def __init__(self, namelist, **argd):
        self.inamelist = iter(namelist)
        super(NameSelector, self).__init__(argd)
        if not self.DataInZip:
            raise "You must define a DataInZip argument to determine where installation data is located!"
        self.regex = re.compile(self.DataInZip)
        
    def main(self):
        not_done = True
        while True:
            try:
                item = self.inamelist.next()
            except StopIteration:
                break
            
            if self.regex.search(item):
                self.send(item)
                
            yield 1
            
        self.send(producerFinished(self), 'signal')
        
class FileExtractor(AutoInstallBase):
    zip = None
    def __init__(self, **argd):
        super(FileExtractor, self).__init__(**argd)
        if not self.zip:
            raise "Zip file must be specified!"
            
    def handle_inbox(self, item):
        data = self.zip.read(item)
        self.send((item, data))
            
class FileWriter(AutoInstallBase):
    DataInZip = 'data/kpuser'
    InstallPath = "~/kpuser"
    def __init__(self, **argd):
        super(FileWriter, self).__init__(**argd)
        self.InstallPath = os.path.expanduser(self.InstallPath)

    def handle_inbox(self, tup):
        name, data = tup
        
        name = name.replace(self.DataInZip, self.InstallPath)

        ext = name.rsplit('.', 1)[-1]
        if ext == 'ini' or ext == 'kp': #these extensions are non-binary
            mode = 'w'
        else:
            mode = 'wb'

        file = open(name, mode)
        file.write(data)
        file.close()
        
    def handle_control(signal):
        if isinstance(signal, (producerFinished, shutdownMicroprocess)):
            self.not_done = False
