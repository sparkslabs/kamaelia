#!/usr/bin/python
#
# On the surface of things, this code *should* work completely correctly.
# However if you run it, you will see that it doesn't.
#
# This appears to be an issue with propogation of events in wxPython/wxWindows
# rather than a kamaelia issue. Quite why this happens is a little unclear.
#
#

import wx
import Axon
import Axon.ThreadedComponent
from Kamaelia.Util.Backplane import *

Backplane("ModelDataSource").activate()

class Model(Axon.Component.component):
    def __init__(self):
        super(Model, self).__init__()
        self.money = 0
        self.publish = PublishTo("ModelDataSource").activate()

    def notifyOutsideWorldOfModelChange(self): self.send(self.money, "outbox")

    def addMoney(self, value):    self.money += value
    def removeMoney(self, value): self.money -= value

    def main(self):
        self.link((self, "outbox"),(self.publish, "inbox"))
        while 1:
            while self.dataReady("inbox"):
                m = self.recv("inbox")
                if m[0] == "add":  self.addMoney(m[1])
                if m[0] == "remove":  self.removeMoney(m[1])
                self.notifyOutsideWorldOfModelChange()
            yield 1

class View(Axon.Component.component,wx.Frame):
    def __init__(self, parent):
        super(View, self).__init__()
        wx.Frame.__init__(self, parent, -1, "Main View")
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "My Money")
        ctrl = wx.TextCtrl(self, -1, "")
        sizer.Add(text, 0, wx.EXPAND|wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND|wx.ALL)
        self.moneyCtrl = ctrl
        ctrl.SetEditable(False)
        self.SetSizer(sizer)
        self.moneyCtrl = ctrl
        
        self.dataSource = SubscribeTo("ModelDataSource").activate()
        self.Show()

    def SetMoney(self, money):
        print "setting money", money
        self.moneyCtrl.SetValue(str(money))

    def main(self):
        self.link((self.dataSource, "outbox"), (self, "inbox"))
        while 1:
            while self.dataReady("inbox"):
                self.SetMoney(self.recv("inbox"))
            yield 1

class UserInput(Axon.Component.component, wx.Frame):
    def __init__(self, parent):
        super(UserInput,self).__init__()
        wx.Frame.__init__(self, parent, -1, "Main View")
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.add = wx.Button(self, -1, "Add Money")
        self.remove = wx.Button(self, -1, "Remove Money")
        sizer.Add(self.add, 0, wx.EXPAND|wx.ALL)
        sizer.Add(self.remove, 0, wx.EXPAND|wx.ALL)
        
        self.add.Bind(wx.EVT_BUTTON, self.addClicked)
        self.remove.Bind(wx.EVT_BUTTON, self.removeClicked)
        
        self.SetSizer(sizer)
        self.Show()
    
    def addClicked(self, evt): self.send("ADD", "outbox")
    def removeClicked(self, evt): self.send("REMOVE", "outbox")

    def main(self):
        while 1:
            yield 1
           
class Controller(Axon.Component.component):
    def __init__(self, app):
        super(Controller,self).__init__()
        self.model = Model()
        self.model = Model().activate()
        self.view1 = View(None).activate()
        self.view2 = UserInput(None).activate()
        self.view3 = View(None).activate()

    def main(self):        
        self.link((self.view2, "outbox"), (self, "inbox"))
        self.link((self,"outbox"), (self.model, "inbox"))
        while 1:
            while self.dataReady("inbox"):
                m = self.recv("inbox")
                if m == "ADD": self.AddMoney()
                if m == "REMOVE": self.RemoveMoney()
            yield 1

    def AddMoney(self):    self.send(("add", 10), "outbox")
    def RemoveMoney(self): self.send(("remove", 10), "outbox")

class MyWxApp(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        app = wx.PySimpleApp()
        Controller(app).activate()
        app.MainLoop()

MyWxApp().run()
