#!/usr/bin/python

from Tkinter import *

class ScrollyList:
    def __init__(self, master, cb):
        scrollbar = Scrollbar(master, orient=VERTICAL)
        self.b1 = Listbox(master, 
                          yscrollcommand=scrollbar.set)
        self.b1.bind("<ButtonRelease-1>", self.lbcallback)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.b1.pack(side=LEFT, fill=BOTH, expand=1)
        self.insert = self.b1.insert
        self.cb = cb
    
    def yview(self, *args):
        apply(self.b1.yview, args)

    def lbcallback(self, *args):
        print "Hmm...", self.b1.curselection(), repr(self.b1.selection_get())
        self.cb(self.b1.curselection(), self.b1.selection_get())

def listFactory(root,cb, items):
    listbox = ScrollyList(root, cb)
    for item in items:
        listbox.insert(END, item)
    return listbox

class ScrollyMenu(Frame):
    def __init__(self, parent, items):
        Frame.__init__ ( self, parent, relief=RAISED, borderwidth=2 )
        self.button = Button(self, text="Choose Component")
        self.button.pack(side=LEFT)
        self.LB_Container = Toplevel()
        self.LB_Container.withdraw()
        self.LB_Container.overrideredirect(1)
        self.list = listFactory(self.LB_Container, self.bingle, items)

        self.button.bind('<1>', self.showMenu)
        self.LB_Container.bind('<Escape>', self.hideMenu)

    def bingle(self,index, selection):
        self.hideMenu()
        self.button.configure(text=selection)

    def hideMenu(self,*args):
        self.LB_Container.withdraw()
        self.LB_Container.overrideredirect(1)


    def showMenu(self, *args):
        self.LB_Container

        redirect = self.LB_Container.overrideredirect()
        if not redirect:
            self.LB_Container.overrideredirect(1)
        self.LB_Container.deiconify()

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + \
            self.button.winfo_height()
        w = self.button.winfo_width() + self.button.winfo_width()
        h =  self.list.b1.winfo_height()
        sh = self.winfo_screenheight()

        if y + h > sh and y > sh / 2:
            y = self.button.winfo_rooty() - h

        self.LB_Container.geometry('+%d+%d' % (x, y))
        self.LB_Container.focus()


root = Tk()
x = ScrollyMenu(root, ["one", "two", "three", "four"]*20)
x.pack(side=LEFT)
y = ScrollyMenu(root, ["one", "two", "three", "four"]*20)
y.pack(side=LEFT)

mainloop()
