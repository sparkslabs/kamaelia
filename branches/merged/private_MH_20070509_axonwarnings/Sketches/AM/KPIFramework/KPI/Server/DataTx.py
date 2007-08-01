import Axon

class DataTx(Axon.Component.component):
   Inboxes = {"inbox" : "data to be encrypted",
              "keyIn" : "key updates"}

   def __init__(self):
      super(DataTx,self).__init__()

   def main(self):
       while 1:
           while self.dataReady("keyIn"):
               data = "KEY" + self.recv("keyIn")
               print "DataTx", data
               self.send(data, "outbox")
           yield 1
           if self.dataReady("inbox"):
               data = "DAT" + self.recv("inbox")
               print "DataTx", data               
               self.send(data, "outbox")
           yield 1
          
