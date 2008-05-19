#!/usr/bin/python

from Axon.Component import component, scheduler, linkage, newComponent
from Axon.Ipc import producerFinished
import Kamaelia.KamaeliaIPC
import string, os, time

try:
   import pygame
   pygame.init()
except:
   pass 

class ClientProtocolHandler(component):
   Inboxes = ["inbox","control", "_displayFinished"]
   Outboxes = ["outbox","signal", "_filteredControlMessages"]

   def __init__(self, tempDir, initialsendmessage, delay, demo_mode=False):
      self.__super.__init__()

      self.requestmessage = initialsendmessage
      self.tempDir = tempDir
      self.delay = delay
      self.demo_mode = demo_mode
 
   def initialiseComponent(self):

      if self.requestmessage == ".mpg":
         self.requestmessage = ".jpg"

      myPacketCombiner = combinePackets()
      myFile = createFile(self.tempDir, self.requestmessage)
      myDisplay = show(self.requestmessage, self.tempDir, self.delay, self.demo_mode)

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
   """
   Get file contents from inbox
   create a name for the file using arugments tempDir and file_type
   write contents to the file
   close file
   send filename to outbox
   check control for a message that is an instance of producerFinished, shutdown if true
   """
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

   def __init__(self, file_type, tempDir, delay, demo_mode=False):
      self.__super.__init__()
      
      self.file_type = file_type
      self.tempDir = tempDir ##used to check if using phone or PC
      self.delay = delay
      self.demo_mode = demo_mode

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

               if self.tempDir == "C:\\ClientContent\\":
                  import pygame
                  pygame.init()
                  self.display_pygame_text_string(self.text)  #display string in Pygame Window
               else:    
                  self.display_text_string(self.text)
        
            elif self.file_type == ".jpg":
               print "show: preparing to display a picture"

               if self.tempDir == "C:\\ClientContent\\":
                   import pygame
                   pygame.init()
                   self.display_pygame_image_file(self.fullfilename) # display image using pygame
               else:    
                   self.display_nokia6600(self.fullfilename)         # display image on nokia6600

            self.timeOfDisplay = time.time()
            return 1

      if isinstance(self.controlMessage, producerFinished) and len(self.filesToDisplay) == 0:
         if self.tempDir == "C:\\ClientContent\\" and self.hadAFile == True:
            if self.demo_mode == False:
                self.pygame_eventHandler_2()
            else:
                IP_toConnectTo = "132.185.133.36"
                IP_toConnectTo = "127.0.0.1"
                print IP_toConnectTo 
                serverport = 1616
                delay = 5
                windows_ClientContentDir = "C:\\ClientContent\\"
                mac_ClientContentDir = "/temp/"
                phone_ClientContentDir = "E:\\Ciaran's Files\\Temp"
                ClientContentDir = [windows_ClientContentDir, mac_ClientContentDir, phone_ClientContentDir]
                demo_mode = True
                
                t = UserInterface(IP_toConnectTo, serverport, delay, ClientContentDir, demo_mode)
                t.activate()
#                scheduler.run.runThreads(slowmo=0)
                return 0
         elif self.file_type == ".jpg" and self.hadAFile == True: 
            self.display_nokia6600_2(self.fullfilename)      # display image on nokia6600
            
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
      

   def display_pygame_text_string(self,
                                  filecontents,
                                  font_size=20,
                                  screensize=[800,600],
                                  back_colour=(0,0,0),
                                  font_colour=(255,255,255)):
      if filecontents != "":
#         print "display_pygame_text_string: Preparing display"
         font = pygame.font.Font(None,font_size)                   #Font
         text_surface = font.render(filecontents, 1, font_colour)  #Surface       
#         print "display_pygame_text_string: creating display"           
         self.pygame_displayHandler(text_surface, screensize, back_colour)
         self.pygame_eventHandler()


   def display_pygame_image_file(self,
                                 image_location,
                                 screensize=[800,600],
                                 back_colour=(0,0,0)):

#      print "display_pygame_image_file: creating image surface"
      image_surface = pygame.image.load(image_location)
#      print "display_pygame_image_file: creating display"           
      self.pygame_displayHandler(image_surface, screensize, back_colour)
      self.pygame_eventHandler()


   def display_pygame_image_string(self,
                                   image_string,
                                   format,
                                   resolution,
                                   screensize=[800,600],
                                   back_colour=(0,0,0)):      
#      print "display_pygame_image_string: creating image surface"
      image_surface = pygame.image.fromstring(image_string, resolution, format)
#      print "display_pygame_image_string: creating display"           
      self.pygame_displayHandler(image_surface, screensize, back_colour)
      self.pygame_eventHandler()

      
   def pygame_displayHandler(self,
                             surface,
                             screensize=[800,600],
                             back_colour=(0,0,0)):
#      print "pygame_displayHandler: getting dimensions"
      width = surface.get_width()
      height = surface.get_height()

      horizonal_to_move = (screensize[0] - width)/2
      vertical_to_move = (screensize[1] - height)/2
      
#      print "pygame_displayHandler: moving rect"
      rect = surface.get_rect()
      rect = rect.move([horizonal_to_move,vertical_to_move])

#      print "pygame_displayHandler: creating display"
      FULLSCREEN = pygame.constants.FULLSCREEN
      screen_surface = pygame.display.set_mode(screensize)
  #    screen_surface = pygame.display.set_mode(screensize,FULLSCREEN)

#      print "display_pygame_image: display"
      screen_surface.fill(back_colour)
      screen_surface.blit(surface, rect)
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
               return 0
         return 1

        
   def pygame_eventHandler_2(self):
      print "pygame_eventHandler_2: Waiting for user response..." 
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


   def display_nokia6600(self, fullfilename):
      try:
         print "display_nokia6600_2: Opening file..."
         appuifw.Content_handler().open(fullfilename)
         print "display_nokia6600_2: opened it"
         return 1
      except IOError:
         print "display_nokia6600_2: Could not fetch the image."
      except Exception, e:
         print e
         print "display_nokia6600_2: Could not open data received."

         
   def display_nokia6600_2(self, fullfilename):
      try:
         print "display_nokia6600: Opening file..."
         lock=e32.Ao_lock()
         content_handler = appuifw.Content_handler(lock.signal)
         content_handler.open(fullfilename)
         # Wait for the user to exit the image viewer.
         lock.wait()
         print "display_nokia6600: Image viewer finished."
         return 0
      except IOError:
         print "display_nokia6600: Could not fetch the image."
      except Exception, e:
         print e
         print "display_nokia6600: Could not open data received."


   def display_nokia6600_eventHandler(self):
      e32.Ao_lock().wait()
      print "display_nokia6600: Image viewer finished."
      return 0


class Client(component):
   def __init__(self,
                IP_toConnectTo,
                serverport,
                delay,
                requestmessage,
                tempDir,
                demo_mode=False):
       
      self.__super.__init__()

      self.IP_toConnectTo = IP_toConnectTo
      self.serverport = serverport
      self.delay = delay
      self.requestmessage = requestmessage
      self.tempDir = tempDir
      self.demo_mode = demo_mode
         
   def initialiseComponent(self):

      self.client = ThreadedTCPClient.ThreadedTCPClient(self.IP_toConnectTo,self.serverport, delay=1, initialsendmessage=self.requestmessage)
      self.display = ClientProtocolHandler(self.tempDir, self.requestmessage, self.delay, self.demo_mode)
       
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



class UserInterface(component):
   def __init__(self,
                IP_toConnectTo,
                serverport,
                delay,
                ClientContentDir,
                demo_mode):
       
      self.__super.__init__()

      self.IP_toConnectTo = IP_toConnectTo
      self.serverport = serverport
      self.delay = delay
      self.ClientContentDir = ClientContentDir
      self.demo_mode = demo_mode

      self.displaySet = False
      self.size = width, height = 800, 600
      self.black = 0, 0, 0
      FULLSCREEN = pygame.constants.FULLSCREEN
      
   #   self.screen = pygame.display.set_mode(self.size,FULLSCREEN)
      self.screen = pygame.display.set_mode(self.size) 
                
   def mainBody(self):
      self.setTempDir()
      #UserInterface
      if self.tempDir != "E:\\Ciaran's Files\\Temp":
         if self.demo_mode == True:
             if self.displaySet == False:             
                try: text_button = pygame.image.load("UI_Pics\\Text button.jpg")
                except: raise "ErrorLoadingImage", "couldn't load text button"
             
                try: image_button = pygame.image.load("UI_Pics\Image button.jpg")
                except: raise "ErrorLoadingImage", "couldn't load image button"
              
                try: movie_button = pygame.image.load("UI_Pics\\Movie button.jpg")             
                except: raise "ErrorLoadingImage", "couldn't load movie button"

                self.textRect = text_button.get_rect()
                self.imageRect = image_button.get_rect()
                self.movieRect = movie_button.get_rect()               

                self.textRect = self.textRect.move(100, 200)
                self.imageRect = self.imageRect.move(350, 200)
                self.movieRect = self.movieRect.move(600, 200)

                font = pygame.font.Font(None,18) 
                self.string_surface = font.render("What request would you like to make?", 1, [255,255,255])
                self.string_rect = self.string_surface.get_rect()

                self.string_rect = self.string_rect.move(300, 150)

                self.screen.fill(self.black)
                self.screen.blit(self.string_surface, self.string_rect)
                self.screen.blit(text_button, self.textRect)
                self.screen.blit(image_button, self.imageRect)
                self.screen.blit(movie_button, self.movieRect)
                
                pygame.display.flip()
                self.displaySet = True

             for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  pygame.quit()
                  return 0
               if event.type == pygame.MOUSEBUTTONDOWN:
                  pos = pygame.mouse.get_pos()
                  mouseRect = [[pos[0],pos[1]],[5,5]]
                  mouseRect = pygame.Rect(mouseRect)
                  
                  if pygame.mouse.get_pressed() == (1,0,0):                     
                     clickedText = mouseRect.colliderect(self.textRect)
                     clickedImage = mouseRect.colliderect(self.imageRect)
                     clickedMovie = mouseRect.colliderect(self.movieRect)
                     
                     if clickedText == True:
                        self.screen.fill(self.black)
                        pygame.display.flip()
                        self.requestmessage = ".txt"
                        self.client = Client(self.IP_toConnectTo, self.serverport, self.delay, self.requestmessage, self.tempDir, self.demo_mode)
                        self.addChildren(self.client)
                        return newComponent(self.client)
                        
                     if clickedImage == True:
                        self.screen.fill(self.black)
                        pygame.display.flip()
                        self.requestmessage = ".jpg"
                        self.client = Client(self.IP_toConnectTo, self.serverport, self.delay, self.requestmessage, self.tempDir, self.demo_mode)
                        self.addChildren(self.client)
                        return newComponent(self.client)
                        
                     if clickedMovie == True:
                        self.screen.fill(self.black)
                        pygame.display.flip()
                        self.requestmessage = ".mpg"
                        self.client = Client(self.IP_toConnectTo, self.serverport, self.delay, self.requestmessage, self.tempDir, self.demo_mode)
                        self.addChildren(self.client)
                        return newComponent(self.client)
                        
                  if pygame.mouse.get_pressed() == (0,0,1):
                     clickedFont = mouseRect.colliderect(self.string_rect)
                     pygame.quit()
                     return 0
                
         elif self.demo_mode == False:
            print "Enter Server IP"
            self.IP_toConnectTo = raw_input()

            print "Enter port (1616)"
            self.serverport = raw_input()
            
            print "Enter delay value"
            self.delay = raw_input()

            print "Enter request (.txt .jpg or .mpg)"
            self.requestmessage = raw_input()
      else:
         self.IP_toConnectTo = appuifw.query(u"Enter Server IP", "text", u"132.185.133.36")
         self.serverport = appuifw.query(u"Enter port", "number")
         self.delay = appuifw.query(u"Enter delay value.", "number")
         self.requestmessage = appuifw.query(u"Enter request ('.txt', '.jpg' or '.mpg')", "text", u".")
         
      return 1 

         
   def setTempDir(self):
      #Set tempDir appropriate to OS 
      if os.name == "nt":
         if os.path.exists(self.ClientContentDir[0]) == True: #Windows based machine
            self.tempDir = self.ClientContentDir[0]
         else:
            raise "tempDir_Error", "Invalid directory (win)"
      elif os.name == "posix":
         if os.path.exists(self.ClientContentDir[1]) == True: #Mac based machine
            self.tempDir = self.ClientContentDir[1]
         else:
            raise "tempDir_Error", "Invalid directory (mac)"
      elif phoneLibs == True:             
         if os.path.exists(self.ClientContentDir[2]) == True: #Phone based
            self.tempDir = self.ClientContentDir[2]
         else:
            raise "tempDir_Error", "Invalid directory (phone)"
      else:                
         raise "tempDir_Error", "Don't reconise OS"
         

if __name__ == "__main__":
   from Kamaelia.Internet import ThreadedTCPClient
   from Axon.Component import component, scheduler, linkage
   from Axon.Ipc import newComponent
   try:
       import e32, appuifw   #nokia6600 libs
       phoneLibs = True
   except:
       phoneLibs = False
       
 #  IP_toConnectTo = "132.185.133.36"
   IP_toConnectTo = "127.0.0.1"
   print IP_toConnectTo 
   serverport = 1616
   delay = 5
   windows_ClientContentDir = "C:\\ClientContent\\"
   mac_ClientContentDir = "/temp/"
   phone_ClientContentDir = "E:\\Ciaran's Files\\Temp"
   ClientContentDir = [windows_ClientContentDir, mac_ClientContentDir, phone_ClientContentDir]
   demo_mode = True

   import sys
   sys.path.append("..\Layout")
   from Introspector import Introspector
   from Kamaelia.Internet.TCPClient import TCPClient
   from Kamaelia.Util.PipelineComponent import pipeline
                    
   pipeline( Introspector(), 
             TCPClient("132.185.133.29",1500) 
            ).activate()
   
   t = UserInterface(IP_toConnectTo, serverport, delay, ClientContentDir, demo_mode)
   t.activate()
   scheduler.run.runThreads(slowmo=0)

#   t = Client()
#   t.activate()
#   scheduler.run.runThreads(slowmo=0)
