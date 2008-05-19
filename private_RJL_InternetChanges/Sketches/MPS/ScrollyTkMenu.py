#!/usr/bin/python

from Tkinter import *

def _defaultCallback(*args):
    pass

class ScrollyList:
    def __init__(self, master, callback=_defaultCallback):
        scrollbar = Scrollbar(master, orient=VERTICAL)
        self.listbox = Listbox(master, 
                          yscrollcommand=scrollbar.set)
        self.listbox.bind("<ButtonRelease-1>", self.lbcallback)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.insert = self.listbox.insert
        self.cb = callback
    
    def yview(self, *args):
        apply(self.listbox.yview, args)

    def lbcallback(self, *args):
        self.cb(self.listbox.curselection(), self.listbox.selection_get())

class ScrollyMenu(Frame):
    def __init__(self, parent, items, width=0, minwidth = 10, maxwidth=1000):
        Frame.__init__ ( self, parent, relief=RAISED, borderwidth=2 )
        self.SelectedItem = 0
        self.SelectedItemText = items[0]
        if width is 0:
            w = 0
            for item in items:
                w = max(len(item), w)
            if width <minwidth:
                width = minwidth
            if width > maxwidth:
                width = maxwidth
        self.button = Button(self, text=self.SelectedItemText, width=width)
        self.button.pack(side=LEFT)
        self.LB_Container = Toplevel()

        self.list = ScrollyList(self.LB_Container, self.bingle)
        for item in items:
            self.list.insert(END, item)

        self.items = items
        self.button.bind('<1>', self.buttonClicked)
        self.button.bind('<5>', self.scrollDown)
        self.button.bind('<4>', self.scrollUp)
        self.LB_Container.bind('<Escape>', self.hideMenu)
        self.DropDownVisible = None
        self.hideMenu()

    def scrollDown(self, *args):
        self.SelectedItem += 1
        if self.SelectedItem >= len(self.items):
            self.SelectedItem = len(self.items) - 1
        self.SelectedItemText = self.items[self.SelectedItem]
        self.button.configure(text=self.SelectedItemText)

    def scrollUp(self, *args):
        self.SelectedItem -= 1
        if self.SelectedItem < 0:
            self.SelectedItem = 0
        self.SelectedItemText = self.items[self.SelectedItem]
        self.button.configure(text=self.SelectedItemText)

    def bingle(self,index, selection):
        self.hideMenu()
        self.button.configure(text=selection)
        self.SelectedItem = index
        self.SelectedItemText = selection

    def hideMenu(self,*args):
        print self.LB_Container.winfo_width()
        self.LB_Container.withdraw()
        self.LB_Container.overrideredirect(1)
        self.DropDownVisible = False

    def buttonClicked(self, *args):
        if self.DropDownVisible:
            self.hideMenu(*args)
        else:
            self.showMenu(*args)

    def showMenu(self, *args):
        redirect = self.LB_Container.overrideredirect()
        if not redirect:
            self.LB_Container.overrideredirect(1)
        self.LB_Container.deiconify()

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + \
            self.button.winfo_height()
        w = self.button.winfo_width()
        h =  self.list.listbox.winfo_height()

        sh = self.winfo_screenheight()

        if y + h > sh and y > sh / 2:
            y = self.button.winfo_rooty() - h

        self.LB_Container.geometry('%dx%d+%d+%d' % (w,100,x, y))
        self.LB_Container.focus()
        self.DropDownVisible = True


if __name__ == "__main__":

    root = Tk()
    x = ScrollyMenu(root, ["one", "two", "three", "four"]*20)
    x.pack(side=LEFT)
    y = ScrollyMenu(root, ["one", "two", "three", "four"]*20)
    y.pack(side=LEFT)

    mainloop()
