#!/usr/bin/python

from Axon.Component import component, scheduler, linkage, newComponent
from Axon.Ipc import producerFinished
import Kamaelia.KamaeliaIPC
import string, os, time
#import appuifw

import pygame
pygame.init()

class ClientProtocolHandler(component):
   Inboxes = ["inbox","control", "_displayFinished"]
   Outboxes = ["outbox","signal", "_filteredControlMessages"]

   def __init__(self, tempDir, initialsendmessage, delay):
      self.__super.__init__()

      self.requestmessage = initialsendmessage
      self.tempDir = tempDir
      self.delay = delay
 
   def initialiseComponent(self):

      if self.requestmessage == ".mpg":
         self.requestmessage = ".jpg"

      myPacketCombiner = combinePackets()
      myFile = createFile(self.tempDir, self.requestmessage)
      myDisplay = show(self.requestmessage, self.tempDir, self.delay)

      "Linkages for myPacketCombiner"
      self.link(source=(self, "inbox"), sink=(myPacketCombiner, "inbox"), passthrough=1)
      self.link(source=(self, "_filteredControlMessages"), sink=(myPacketCombiner, "control"), passthrough=0)

      "Linkages for myFile"
      self.link(source=(myPacketCombiner, "outbox"), sink=(myFile, "inbox"), passthrough=0)
      self.link(source=(myPacketCombiner, "signal"), sink=(myFile, "control"), passthrough=0)

      "Linkages for myDisplay"
      self.link(source=(myFile, "outbox"), sink=(myDisplay, "inbox"), passthrough=0)
      self.link(source=(myFile, "signal"), sink=(myDisplay, "control"), passthrough=0)
      
      self.link(source=(myDisplay, "signal"), sink=(self, "_displayFinished"), passthrough=0)
      
      self.addChildren(myPacketCombiner, myFile, myDisplay)
      return newComponent(myPacketCombiner, myFile, myDisplay)
      
   def mainBody(self):
#      print "ClientProtocolHandler: Checking mail..."
                      
      if self.dataReady("_displayFinished"):
         print "ClientProtocolHandler: Message received! (_displayFinished)"
         self.message = self.recv("_displayFinished")
         
         if isinstance(self.message, producerFinished):
            self.send(producerFinished("Done"),"signal") 
            return 0
         else:
            print "ClientProtocolHandler: Message from _displayFinished is..."
            print self.message

      if self.dataReady("control"):
          print "ClientProtocolHandler: Message received! (control)"
          self.controlMessage = self.recv("control")

          if isinstance(self.controlMessage, Kamaelia.KamaeliaIPC.socketShutdown) or self.controlMessage == "StoppedThread":
              self.send(self.controlMessage, "_filteredControlMessages")
          else:
              print "ClientProtocolHandler: Message from control is..."
              print self.controlMessage
      return 1
    
   def closeDownComponent(self):
      print "ClientProtocolHandler: Shutting down"



class combinePackets(component):
   """
   Checks messages on inbox then control. If a message is received in the component's inbox it is appended to a list/buffer.

   take chunk from buffer list
   add chunk to a new buffer
   search new buffer for "\n" and get it's index
   get what comes before the "\n" (by using it's index)
   what came before the \n should be the number of characters the file should contain
   """
   def __init__(self):
      self.__super.__init__()
      
      self.list_packets = []
      self.buffer = ""
      self.buffers = []
        
   def mainBody(self):
#      print "combinePackets: Checking mail..."

      if  self.dataReady("inbox"):
#         print "combinePackets: Message received! (inbox)"
         self.data = self.recv("inbox")
         self.buffers.append(self.data)
        
      while len(self.buffer)>0 or len(self.buffers)>0:
         if len(self.buffers) > 0:                     
            self.chunk = self.buffers[0]
            del self.buffers[0]
         else:
            self.chunk = ""
         self.buffer = self.buffer + self.chunk
#         print "combinePackets: BUFF:",repr(self.buffer)
         self.end_of_length = self.buffer.find("\n")
         if self.end_of_length != -1:
#            print "combinePackets: EOL:", self.end_of_length
            try:
               self.length_of_picture = int(self.buffer[:self.end_of_length])
            except Exception,e:
               print e
               print "buffer:", self.buffer
               print "EOL:", self.end_of_length
               print "LOP:", self.length_of_picture
#            print "combinePackets: LEN:", self.length_of_picture
            if len(self.buffer) >= self.end_of_length + self.length_of_picture + 1:
               self.picture = self.buffer[self.end_of_length + 1: self.end_of_length + self.length_of_picture + 1]
               self.send(self.picture,"outbox")
#               print "combinePackets: CONSUMED:", repr(self.picture)
               self.buffer = self.buffer[self.end_of_length + self.length_of_picture + 1:]
            else:
               pass
#               print "combinePackets: buffer needs data"
         return 1

      if self.dataReady("control"):
         print "combinePackets: Message received! (control)"
         self.controlMessage = self.recv("control")
         
         print "combinePackets: Message from control is..."
         print self.controlMessage
            
         if isinstance(self.controlMessage, Kamaelia.KamaeliaIPC.socketShutdown) or self.controlMessage == "StoppedThread":
            self.send(producerFinished("Done"),"signal")
            return 0        
      return 1  

   def closeDownComponent(self):
      print "combinePackets: Shutting down"  



class createFile(component):
   Inboxes = ["inbox","control"]
   Outboxes = ["outbox","signal"]
                      
   def __init__(self, tempDir, file_type):
      self.__super.__init__()
      self.tempDir = tempDir
      self.file_type = file_type

      self.fileNumber = 0
       
   def mainBody(self):
#      print "createFile: Checking mail..."
      if self.dataReady("inbox"):
         print "createFile: Message received! (inbox)"
         self.filecontents = self.recv("inbox")

         self.fullfilename = self.create_TempFilename(self.tempDir, file_type=self.file_type) 
         
         try:      
#            print "createFile: creating file object"
            self.file_object = open(self.fullfilename,"wb")
            print "createFile: writing contents to file"
            self.file_object.write(self.filecontents)
#            print "createFile: closing file object"
            self.file_object.close()
         except Exception, e:
            print "createFile: Exception..."
            print e
                                   
         self.send(self.fullfilename, "outbox")

      if self.dataReady("control"):
         print "createFile: Message received! (control)"
         self.controlMessage = self.recv("control")
         
         if isinstance(self.controlMessage, producerFinished):
            self.send(producerFinished("Done"), "signal")
            return 0
      return 1
     
   def closeDownComponent(self):
      print "createFile: Shutting down"

   def create_TempFilename(self, tempDirectory, filename_without_ext=None, file_type=".bmp"):
      """
      Creates a new, unique full filename each time it is called by incrementing the digit at the
      end of the filename. 
      """
      if filename_without_ext == None:
         filename_without_ext = "TempFile"
         
      filename = filename_without_ext + str(self.fileNumber) + file_type
      self.fileNumber = self.fileNumber + 1
      
      fullfilename = os.path.join(tempDirectory, filename)
#      print "createFile: Temp file will be...", fullfilename
      return fullfilename


      
class show(component):
   Inboxes = ["inbox","control"]
   Outboxes = ["outbox","signal"]

   def __init__(self, file_type, tempDir, delay):
      self.__super.__init__()
      
      self.file_type = file_type
      self.tempDir = tempDir ##used to check if using phone or PC
      self.delay = delay

      self.tempFiles = []
      self.filesToDisplay = []
      self.timeOfDisplay = 0
      self.controlMessage = ""
      self.hadAFile = False

   def mainBody(self):
#      print "show: Checking mail..."      
      if self.dataReady("inbox"):          
         print "show: Message received (inbox)"
         self.fullfilename = self.recv("inbox")
         print "show: Message from inbox is...", self.fullfilename
         self.tempFiles.append(self.fullfilename)
         self.filesToDisplay.append(self.fullfilename)
         self.hadAFile = True

      if self.dataReady("control"):
         print "show: Message received (control)"
         self.controlMessage = self.recv("control")
         
      if len(self.filesToDisplay) > 0:
         if (time.time() - self.timeOfDisplay) > self.delay:
             
            self.file = self.filesToDisplay[0]
            del self.filesToDisplay[0]             
            if self.file_type == ".txt":
               print "show: preparing to display text"
               self.file_object = open(self.fullfilename, "r")
               self.text = self.file_object.read()

               "Choose method for displaying text files"
               if self.tempDir == "C:\\ClientContent\\":
                  import pygame
                  pygame.init()
                  self.display_pygame_text_string(self.text)  #display string in Pygame Window
               else:    
                  self.display_text_string(self.text)
        
            elif self.file_type == ".jpg":
               print "show: preparing to display a picture"

               "Choose method for displaying images"
#               if self.tempDir == "C:\\ClientContent\\":
               if 1:
                   import pygame
                   pygame.init()
                   self.display_pygame_image_file(self.fullfilename) # display image using pygame
#               else:    
#                   self.display_nokia6600(self.fullfilename)                 # display image on nokia6600

            self.timeOfDisplay = time.time()
            return 1

      if isinstance(self.controlMessage, producerFinished) and len(self.filesToDisplay) == 0:
#         if self.tempDir == "C:\\ClientContent\\" and self.hadAFile == True:
         if self.hadAFile == True:
            self.pygame_eventHandler_2()
#         elif self.file_type == ".jpg" and self.hadAFile == True: 
#            self.display_nokia6600_2(self.fullfilename)      # display image on nokia6600
            
         self.send(producerFinished("Done"), "signal")      
         return 0
      return 1

   def closeDownComponent(self):
      for file in self.tempFiles:
         try:
            print "show: Removing", file
            os.remove(file)
         except Exception, e:
            print "show: ", e         
      print "show: Shutting down"


   def display_text_string(self, filecontents):
      """
      Takes a string in filecontents argument and displays it in the Python Shell. It then waits
      for keyboard return carriage. When user does push return key a producerFinished message is
      sent to signal box.
      """       
      print "display_text: the message is..."
      print filecontents
      raw_input()
      self.send(producerFinished("Done"),"signal")


   def display_pygame_text_string(self,
                                  pygame,
                                  filecontents,
                                  font_size=20,
                                  screensize=[600,600],
                                  back_colour=(0,0,0),
                                  font_colour=(255,255,255)):
      if filecontents != "":
#         print "display_pygame_text_string: Preparing display"
         font = pygame.font.Font(None,font_size)                   #Font
         text_surface = font.render(filecontents, 1, font_colour)  #Surface       
#         print "display_pygame_text_string: creating display"           
         self.pygame_displayHandler(pygame, text_surface, screensize, back_colour)
         self.pygame_eventHandler(pygame)

   def display_pygame_image_file(self, image_location, screensize=[800,600], back_colour=(0,0,0)):

#      print "display_pygame_image_file: creating image surface"
      image_surface = pygame.image.load(image_location)
#      print "display_pygame_image_file: creating display"           
      self.pygame_displayHandler(image_surface, screensize, back_colour)
      self.pygame_eventHandler()


   def display_pygame_image_string(self, pygame, image_string, format, resolution, screensize=[600,600], back_colour=(0,0,0)):      
#      print "display_pygame_image_string: creating image surface"
      image_surface = pygame.image.fromstring(image_string, resolution, format)
#      print "display_pygame_image_string: creating display"           
      self.pygame_displayHandler(pygame, image_surface, screensize, back_colour)
      self.pygame_eventHandler(pygame)
      
   def pygame_displayHandler(self, surface, screensize=[600,600], back_colour=(0,0,0)):
#      print "pygame_displayHandler: getting dimensions"
      width = surface.get_width()
      height = surface.get_height()

      horizonal_to_move = (screensize[0] - width)/2
      vertical_to_move = (screensize[1] - height)/2
      
#      print "pygame_displayHandler: moving rect"
      rect = surface.get_rect()
      rect = rect.move([horizonal_to_move,vertical_to_move])

#      print "pygame_displayHandler: creating display"
      screen_surface = pygame.display.set_mode(screensize, pygame.FULLSCREEN)


#      print "display_pygame_image: display"
      screen_surface.fill(back_colour)
      screen_surface.blit(surface, rect)

      my_font = pygame.font.Font(None, 64)
      firstline = my_font.render("Simple Streaming Client", 1, (232,232,48) )

      my_font = pygame.font.Font(None, 48)
      secondline = my_font.render("(PC Version)", 1, (232,232,48) )

      my_font = pygame.font.Font(None, 32)
      tagline = my_font.render("Please also see the mobile version", 1, (232,232,48) )

      screen_surface.blit(firstline, (100,40))
      screen_surface.blit(secondline, (150,95))
      screen_surface.blit(tagline, (100,500))

      pygame.display.flip()


   def pygame_eventHandler(self):
      while 1:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               print "pygame_eventHandler: User closed window, shutting down"
               pygame.quit()
               return 0
            if event.type == pygame.KEYDOWN:
               print "pygame_eventHandler: User pushed a button, shutting down"
               pygame.quit()
               raise "Quit"
               return 0
         return 1

        
   def pygame_eventHandler_2(self):
      print "pygame_eventHandler_2: Waiting for user response..." 
      timeout=2
      t = time.time()
      while 1:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
               print "pygame_eventHandler_2: User closed window, shutting down"
               pygame.quit()
               return 0
            if event.type == pygame.KEYDOWN:
               print "pygame_eventHandler_2: User pushed a button, shutting down"
               pygame.quit()
               return 0
          if timeout and time.time()-t>timeout:
             return

                      #   def display_nokia6600(self, fullfilename):
                      #      try:
                      #         print "display_nokia6600_2: Opening file..."
                      #         appuifw.Content_handler().open(fullfilename)
                      #         print "display_nokia6600_2: opened it"
                      #         return 1
                      #      except IOError:
                      #         print "display_nokia6600_2: Could not fetch the image."
                      #      except Exception, e:
                      #         print e
                      #         print "display_nokia6600_2: Could not open data received."
                      #
                      #         
                      #   def display_nokia6600_2(self, fullfilename):
                      #      try:
                      #         print "display_nokia6600: Opening file..."
                      #         lock=e32.Ao_lock()
                      #         content_handler = appuifw.Content_handler(lock.signal)
                      #         content_handler.open(fullfilename)
                      #         # Wait for the user to exit the image viewer.
                      #         lock.wait()
                      #         print "display_nokia6600: Image viewer finished."
                      #         return 0
                      #      except IOError:
                      #         print "display_nokia6600: Could not fetch the image."
                      #      except Exception, e:
                      #         print e
                      #         print "display_nokia6600: Could not open data received."
                      #
                      #
                      #   def display_nokia6600_eventHandler(self):
                      #      e32.Ao_lock().wait()
                      #      print "display_nokia6600: Image viewer finished."
                      #      return 0

            

if __name__ == "__main__":
   from Kamaelia.Internet import ThreadedTCPClient
#   from Kamaelia.Internet import TCPClient
   from Axon.Component import component, scheduler, linkage
   from Axon.Ipc import newComponent
   try:
     import e32, appuifw   #nokia6600 libs
   except:
     pass

   class Client(component):
      def __init__(self):
         self.__super.__init__()
         
         self.serverport = 1616
         self.requestmessage = ".mpg"
         
#         self.tempDir = "E:\\Ciaran's Files\\Temp"  #use on phone
#         self.tempDir = "C:\\ClientContent\\"       #test on PC
         self.tempDir = "tmp"

         if self.tempDir != "E:\\Ciaran's Files\\Temp":

            self.delay = 1
            self.IP_toConnectTo = "127.0.0.1"
            self.serverport = 1616
            self.requestmessage = ".mpg"
            if 0:
                  print "Enter delay value"
                  self.delay = int(raw_input())
                  print "Enter IP of server"    
                  self.IP_toConnectTo = str(raw_input())
                  print "Enter port to connect to"
                  self.serverport = int(raw_input())
                  print "Enter request"    
                  self.requestmessage = raw_input()
         else:   
            self.delay = appuifw.query(u"Enter delay value.", "number")
            self.IP_toConnectTo = "127.0.0.1"
         
         self.client = None
         self.display = ClientProtocolHandler(self.tempDir, self.requestmessage, self.delay)
         
      def initialiseComponent(self):

         self.client = ThreadedTCPClient.ThreadedTCPClient(self.IP_toConnectTo,self.serverport, delay=1, initialsendmessage=self.requestmessage)
#         self.client = TCPClient.TCPClient(self.IP_toConnectTo,self.serverport, delay=1, initialsendmessage=self.requestmessage)
       
         self.addChildren(self.client, self.display)
      
         self.link((self.client,"outbox"), (self.display,"inbox") )
         self.link((self.display,"outbox"), (self.client,"inbox") )
      
         self.link((self.client,"signal"), (self.display,"control") )
         self.link((self.display,"signal"), (self,"control") )
      
         return newComponent( self.client, self.display)

      def mainBody(self):
         if self.dataReady("control"):
            something = self.recv("control")
            return 0
         return 1

      def closeDownComponent(self):
         print "ALL DONE! GOODBYE"

   t = Client()
   t.activate()
   scheduler.run.runThreads(slowmo=0)



