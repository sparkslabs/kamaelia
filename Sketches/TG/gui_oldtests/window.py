from Tkinter import *
from tkSimpleDialog import *
from ModuleShard import *

top = Tk()

def meh():
    print 'nothing works'

def generate():
    for s in mainPanel.slaves():
        print s
        s.generate()

class config(Dialog):
    def __init__(self, parent, title = None):
        Dialog.__init__(self, parent, title)

    def body(self, frame):
        Label(frame, text="import modules:").grid(row=0)
        Label(frame, text="import froms:").grid(row=1)
        Label(frame, text="docstring:").grid(row=2)
        Label(frame, text="shards:").grid(row=3)

        self.importmodules = Entry(frame)
        self.importfrom = Label(frame, text = "not yet")
        self.docstring = Entry(frame)
        self.shards = Label(frame, text = "not yet")
        
        self.importmodules.grid(row=0, column=1)
        self.importfrom.grid(row=1, column=1)
        self.docstring.grid(row=2, column=1)
        self.shards.grid(row = 3, column = 1)
        
        return self.importmodules # initial focus

    def apply(self):
        return self.importmodules.get().split(','), self.docstring.get()

class name(Dialog):
    def body(self, frame):
        Label(frame, text="module name:").grid(row=0)

        self.name = Entry(frame)
        self.name.grid(row=0, column=1)
        
        return self.name # initial focus
        
    def apply(self):
        addButton(self.name.get())

class myButton(Button):
    def __init__(self, master = None, **config):
        self.name = config['text']
        Button.__init__(self, master, config, command = self.configDialog)
    
    def configDialog(self):
        imods, docstr = config(top)#, 'configure module '+ self.name)
        self.configure(importmodules = imods, docstring = docstr)
    
    def configure(self, importmodules = [], importfrom = {},
                        docstring = '', shards = []):

        if importmodules:
            self.importmodules = importmodules
        if importfrom:
            self.importfrom = importfrom
        if docstring:
            self.docstring = docstring
        if shards:
            self.shards = shards
        
        return self
        
    def generate():
        moduleShard(name = self.name, importmodules = self.importmodules,
                              docstring = self.docstring).writeFile()
        

def addButton(text):    
    newButton = myButton(mainPanel, text = text)
    newButton.pack(side = 'left')
    
    return newButton

def makeModule():
    name(top, 'new module')

buttonPanel = Frame()
buttonPanel.pack(side='top')

genBtn = Button(buttonPanel, text = "generate", command = generate)
genBtn.pack(side = 'left')

separator = Frame(buttonPanel, height = 25, width = 2, bd=1, relief=SUNKEN)
separator.pack(side = 'left', padx=5, pady=5)

moduleBtn = Button(buttonPanel, text = "module", command = makeModule)
moduleBtn.pack(side = 'left')

mainPanel = Frame(height = 100)
mainPanel.pack()

top.mainloop()