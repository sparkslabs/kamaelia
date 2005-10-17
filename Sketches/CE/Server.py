#!/usr/bin/env python

import os, pygame, random, time, string, Image
from Axon.Component import component, scheduler, linkage
from Axon.Ipc import producerFinished, newComponent
from Kamaelia.KamaeliaIPC import socketShutdown


class ServerProtocolHandler(component):
   """ 
   takes the following argument(s):
      contentDirectory - the directory in which the handler will search for content to send.
      tempFileDirectory - the directory in which the handler will temporaily store snapshots from mpeg
                          video streams (bmp and jpeg files).                  
      delay - the delay between the sending of each file. Do not expect it to be entirely accurate.
      number_of_files_to_find - number of files to send. In the case of a mpeg file being requested this
                                number reverted to 1.
      number_of_snapshots_to_get - number of files/snapshots that will be sent when a mpeg files is
                                   requested.

   mainbody:
      Component checks control, inbox then _readFinished for messages.
       - if a message received in control is an instance of socketShutdown then component shuts down.
       - if message received in inbox check to see if a valid request was made (either ".txt",".txt\n",
         ".jpg",".jpg\n",".mpg" or ".mpg\n").
           - if file type to look for is ".txt" or ".jpg" then create components random_file_selector
             and component char_count_and_read.
           - if file type to look for is ".mpg" then create components random_file_selector,
             grab_image_from_video and char_count_and_read.
       - if message received in _readFinished and the message is an instance of producerFinished proceed
         to shutdown.
   
   shutdown condition(s):
      - Socket shutdown message in control box  (i.e. client disconnected).
      - producerFinished message in _readFinished.
      - invalid request message (i.e. message from inbox was neither of the following: ".txt",
        ".txt\n", ".jpg", ".jpg\n", ".mpg", ".mpg".

   on shutdown:
      Component checks _tempFilesList for message (the message is expected to be a list of temp files
      that are to be deleted). If a message is present then the component will procede to try
      and delete each file within the list one by one.
   """
    
   Inboxes = ["inbox","control","_readFinished", "_tempFilesList"]
   Outboxes =  ["outbox","signal"]
   
   def __init__(self,
                contentDirectory="servercontent",
                tempFileDirectory=os.path.join("servercontent","temp"),
                delay=5,
                number_of_files_to_find=5,
                number_of_snapshots_to_get=10):
       
      self.__super.__init__()
      
      self.directory = contentDirectory
      self.tempFileDirectory = tempFileDirectory
      self.delay = delay
      self.number_of_files_to_find = number_of_files_to_find
      self.number_of_snapshots_to_get = number_of_snapshots_to_get

      self.files_sent = 0
  
   def mainBody(self):
#      print "ServerProtocolHandler: Checking mail..."
      if self.dataReady("control"):
         print "ServerProtocolHandler: Message received (control)"
         self.controlMessage = self.recv("control")

         if isinstance(self.controlMessage, socketShutdown):
             print "ServerProtocolHandler: Message from control is", socketShutdown
             return 0
            
      if self.dataReady("inbox"):
         print "ServerProtocolHandler: Message received (inbox)"
         self.requestMessage = self.recv("inbox")
         print "ServerProtocolHandler: Message contained this...", self.requestMessage

         self.file_type, self.number_of_files_to_find, self.clientConnect = self.checkMessage(self.requestMessage, self.number_of_files_to_find)

         if self.file_type == None:
            print "ServerProtocolHandler: Invalid request made" 
            self.send("Invalid request", "outbox")
            return 0
  
         print "ServerProtocolHandler: going to look in this directory", self.directory

         if self.file_type == ".mpg":
            FileChooser = random_file_selector(self.directory, self.file_type, self.number_of_files_to_find)
            ImageGrabber = grab_image_from_video(self.tempFileDirectory, self.delay, self.number_of_snapshots_to_get)
            MyFileReader = char_count_and_read(self.clientConnect)

            self.link(source=(FileChooser, "outbox"), sink=(ImageGrabber, "inbox"), passthrough=0)

            self.link(source=(ImageGrabber, "outbox"), sink=(MyFileReader, "inbox"), passthrough=0)
            self.link(source=(ImageGrabber, "signal"), sink=(MyFileReader, "control"), passthrough=0)
            self.link(source=(ImageGrabber, "tempFilesList"), sink=(self, "_tempFilesList"), passthrough=0)
            
            self.link(source=(MyFileReader, "outbox"), sink=(self, "outbox"), passthrough=2)
            self.link(source=(MyFileReader, "signal"), sink=(self, "_readFinished"), passthrough=0)
            
            self.addChildren(FileChooser, ImageGrabber, MyFileReader)
            return newComponent( FileChooser, ImageGrabber, MyFileReader )
         else:
            FileChooser = random_file_selector(self.directory, self.file_type, self.number_of_files_to_find)
            MyFileReader = char_count_and_read(self.clientConnect, self.delay)

            self.link(source=(FileChooser, "outbox"), sink=(MyFileReader, "inbox"), passthrough=0)
            self.link(source=(FileChooser, "signal"), sink=(MyFileReader, "control"), passthrough=0)

            self.link(source=(MyFileReader, "outbox"), sink=(self, "outbox"), passthrough=2)
            self.link(source=(MyFileReader, "signal"), sink=(self, "_readFinished"), passthrough=0)
            
            self.addChildren(FileChooser, MyFileReader)
            return newComponent( FileChooser, MyFileReader )             
        
      if self.dataReady("_readFinished"):
         print "ServerProtocolHandler: Message received (_readFinished)"
         self.readFinished = self.recv("_readFinished")
         for child in self.childComponents():
           self.postoffice.deregister(component=child)

           
         if isinstance(self.readFinished, producerFinished): 
            self.send(producerFinished("Done"), "signal")
            return 0
      return 1  
        
   def closeDownComponent(self):
      """
      Retrieve list of temp files (both .jpeg's and .bmp's).
      Attempt to delete each file one by one.
      """
      if self.dataReady("_tempFilesList"):
         self.tempFiles = self.recv("_tempFilesList")
          
         for file in self.tempFiles:
            try:
               print "ServerProtocolHandler: Removing", file
               os.remove(file)
            except Exception, e:
               print "ServerProtocolHandler: ", e
               
      print "ServerProtocolHandler: Shutting down"
      

   def checkMessage(self, message, number_of_files_to_find):
      """
      Remove newline characters (\n) from message so it will work as a file type.
      If newline character present in message flag that the client handler wasn't used.
      If mpeg requested then change the number_of_files_to_find to 1 (only want 1 video file but
      many snapshots).
      """
      self.file_type = message 
      self.clientConnect = True
      message = message.rstrip()
      
      if message == ".jpg":
         print "ServerProtocolHandler: Image Requested"
             
      elif message == ".txt":
         print "ServerProtocolHandler: Text Requested"
         
      elif message == ".mpg":
         number_of_files_to_find = 1
         print "ServerProtocolHandler: Snapshots from MPEG Requested"
         
      elif message == ".jpg\n":
         self.file_type = ".jpg"
         self.clientConnect = False
         print "ServerProtocolHandler: Image Requested"
             
      elif message == ".txt\n":
         self.file_type = ".txt"
         self.clientConnect = False
         print "ServerProtocolHandler: Text Requested"

      elif message == ".mpg\n":
         self.file_type = ".mpg"
         self.clientConnect = False
         number_of_files_to_find = 1
         print "ServerProtocolHandler: Snapshots from MPEG Requested"
      else:
         self.file_type = None
      return self.file_type, number_of_files_to_find, self.clientConnect


class random_file_selector(component):
   """
   Randomly selects X number of files of Y file type from directory Z. Where:
      X is the argument number_of_files_to_find
      Y is the argument file_type
      Z is the argument directory

   mainbody:
      - While haven't sent X number of messages, containing the full filename of randomly selected
        files, to outbox.
        - Get a list of all files in directory Z.
        - Remove all files not of file type Y from list.
        - Randomly select a file.
        - Create full filename by joining directory Z with selected file.
        - Send full filename as message to outbox.
      - Send producerFinished message to signal.  
      - Shutdown.
   
   shutdown condition(s):
      - Sent X number of files
   """
   def __init__(self, directory, file_type, number_of_files_to_find=1):
      self.__super.__init__()
        
      self.directory = directory
      self.file_type = file_type.rstrip()
      self.number_of_files = number_of_files_to_find
      
      self.list = ""
      self.filenames_mailed = 0

   def mainBody(self):            
      while self.number_of_files > self.filenames_mailed:
               
         "create a list of all the files in the provided directory" 
         self.filelisting = os.listdir(self.directory)
      
         self.filelisting = self.find_files_of_type(self.filelisting, self.file_type) #remove files from list that are not of the right file type

         if len(self.filelisting) == 0:
            print "random_file_selector: No files of that type in the directory!", repr(self.file_type)
            self.send(producerFinished("Done"),"signal")
            return 0
          
         file_index = random.randrange(0, len(self.filelisting))  #index for a random file
         random_file = self.filelisting[file_index]               #get the name of random file
      
         print "random_file_selector: The randomly choosen file is", random_file
   
         fullfilename = os.path.join(self.directory, random_file) #"root\file"
         
         self.send(fullfilename,"outbox")
         self.filenames_mailed = self.filenames_mailed + 1
         return 1
         
      self.send(producerFinished("Done"),"signal")  
      return 0
    
   def closeDownComponent(self):
      print "random_file_selector: Shutting down"


   def find_files_of_type(self, list_of_files, file_type):
      """
      Remove files from list_of_files which do not have a file extension of file_type.
      Returns a list containing the files which were not removed from list_of_files.
      """
      list_FilesOfWantedType = []
#      print "find_files_of_type: The list provided is", list_of_files
#      print "find_files_of_type: The following file type is requested", file_type
      for file in list_of_files:
          split_filename = os.path.splitext(file)    #[ filename, file extension ]
          if split_filename[1] == file_type:
              list_FilesOfWantedType.append(file)
#      print "find_files_of_type: These files fit the description", files_of_wanted_type
      return list_FilesOfWantedType


class grab_image_from_video(component):
   """
   Takes X number of snapshots from mpeg file, Y, at intervals of D. When each snapshot is taken it is
   saved as a bmp file, with an unique name, in directory Z. This bmp file is then converted to jpeg
   format, given the same filename as the bmp (except for the extension) and also saved in directory Z.
   Once the jpeg is created it's full filename is sent, as a message, to it's outbox. The full filename
   of both the jpeg and bmp files are then appended to a list. The component then increments counter of snapshots
   taken and compares this to X. If X is greater than counter than the stages to take a snapshot are repeated.
   When counter is equal to or greater than X then the list of jpeg and bmp files that were created is sent to
   tempFilesList and a producerFinished message is sent to the components signal box.

   Where:
      X is the argument number_of_snapshots_to_get
      Y is the full filename of a mpeg file which is gained from a message received the components inbox
      D is the argument delay
      Z is the argument tempDirectory
   
   shutdown condition(s):
      - X number of snapshots taken
   """
   Inboxes = ["inbox"]
   Outboxes =  ["outbox","signal","tempFilesList"]
   
   def __init__(self,
                tempDirectory,
                delay=10,
                number_of_snapshots_to_get=10):

      self.__super.__init__()
      pygame.init()

      self.tempDirectory = tempDirectory
      self.delay = delay
      self.number_of_snapshots_to_get = number_of_snapshots_to_get

      self.snapshots_saved = 0   #snapshot counter
      self.timeOfLastSnapshot = 0
      self.gotMovie = False
      self.fileNumber = 0

   def mainBody(self):
      if self.gotMovie == True:    #if already have a video file loaded
         while self.number_of_snapshots_to_get > self.snapshots_saved:       #while haven't sent enough snapshots
            if (time.time() - self.start_time) < self.movie_length:          #if the movie hasn't ended
               if (time.time() - self.timeOfLastSnapshot) > self.delay:      #if waited long enough
#                  print "grab_image_from_video: Pausing movie for snapshot" 
                  self.myMovie.pause()
          
#                  print "grab_image_from_video: Temp filename"
                  self.tempfile = self.create_TempFilename(self.tempDirectory, self.randomFilename)
                  
                  print "grab_image_from_video: Saving snapshot..."
                  pygame.image.save(self.image_surface, self.tempfile)
                  
                  self.jpeg_fullfilename = self.convert_fileFormat(self.tempfile, ".jpg")

                  self.send(self.jpeg_fullfilename, "outbox")   #tell next component where to find file

                  self.tempFiles.append(self.tempfile)
                  self.tempFiles.append(self.jpeg_fullfilename)

#                  print "grab_image_from_video:  Resuming movie"
                  self.myMovie.pause()                             #resume movie
                  self.snapshots_saved = self.snapshots_saved + 1  #increment snapshot counter                  
                  self.timeOfLastSnapshot = time.time()         
            else:
               print "grab_image_from_video: Movie ended so shutting down"
               self.send(producerFinished("Done"), "signal")
               self.myMovie.stop()
               self.gotMovie = False
#               pygame.quit()
               return 0
            return 1 
         print "grab_image_from_video: Saved the number of requested snapshots so shutting down"
         self.send(producerFinished("Done"), "signal")
         self.myMovie.stop()
         self.gotMovie = False
#         pygame.quit()
         return 0
       
#      print "grab_image_from_video: Checking mail..."
      if self.dataReady("inbox"):
         print "grab_image_from_video: Message received! (inbox)"
         self.fullfilename = self.recv("inbox")

#         print "grab_image_from_video: Message from inbox is...", self.fullfilename

         self.myMovie = pygame.movie.Movie(self.fullfilename)   #Load video file
         self.resolution = self.myMovie.get_size()              #Get it's dimensions
         self.movie_length = self.myMovie.get_length()          #Get it's play length
         
         self.image_surface = pygame.Surface(self.resolution)   #Create surface for the video
         self.image_surface.fill([0,0,0])                       #Fill surface black
    
         self.myMovie.set_display(self.image_surface)           #Assign video stream to the surface
         self.myMovie.play()                                    #Start video stream 
         self.start_time = time.time()                          #Get time the stream was started

         self.gotMovie = True
         self.tempFiles = []
         self.randomFilename = str(random.randint(0000000, 9999999))
      return 1  
          
   def closeDownComponent(self):
      self.send(self.tempFiles, "tempFilesList")
      print "grab_image_from_video: Shutting down"

   def create_TempFilename(self, tempDirectory, filename_without_ext, file_type=".bmp"):
      """
      Creates a new, unique full filename each time it is called by incrementing the digit at the
      end of the filename. 
      """
      filename = filename_without_ext + str(self.fileNumber) + file_type
      self.fileNumber = self.fileNumber + 1
      
      fullfilename = os.path.join(tempDirectory, filename)
#      print "grab_image_from_video: Temp file will be...", fullfilename
      return fullfilename
    
   def convert_fileFormat(self, fullfilename, new_format):
      """
      Convert an image file from one format to another
       - fullfilename being the full filename of the file to be converted
       - new_format being the format to convert the image to
      Returns the full filename of the newly created file (it should be the same as fullfilename except for the
      extension)
      """
      base, ext = os.path.splitext(fullfilename)
      outfile = base + new_format

      if fullfilename != outfile:
        try:
            Image.open(fullfilename).save(outfile)
            return outfile
        except IOError:
            print "Cannot convert", fullfilename 
      return 1



class char_count_and_read(component):
   """
   Checks inbox for a message containing the full filename for a file to read. When the component receives a message
   in it's inbox it procedes to check when the last file was read. If the last file to be read occured more than X ago
   then it reads the file and gets a character count, else it "waits" (checks inboxes then returns 1). If a connection
   was made via the client handler (Display6nokia) then the component will construct a message to be sent to it's
   outbox consisting of:
      character count + "\n" + file contents
   as a single string. If a connection was made not using the client handler (signified by clientConnect = False) then
   the component will construct a message to be sent to it's outbox consisting of:
      file contents          

   Where:
      X is the argument delay


   shutdown condition(s):
      - message received in control which is an instance of producerFinished
   """
   def __init__(self, clientConnect = True, delay=0):
      self.__super.__init__()

      self.delay = delay
      self.clientConnect = clientConnect

      self.current_time = 0
      self.fileRead = True
      
   def mainBody(self):
      while self.fileRead == False:
         if (time.time() - self.current_time) > self.delay:
            self.current_time = time.time()

#            print "char_count_and_read: opening file..."
            self.file_object = open(self.fullfilename,"rb") 

            self.fileContents = self.file_object.read()
            self.charCount = len(self.fileContents)

            if self.clientConnect == True:
               print "char_count_and_read: Sending size and content of file"
               self.message = str(self.charCount) + "\n" + self.fileContents
               #print self.message
               self.send(self.message, "outbox")

#            print "char_count_and_read: closing file..."
            self.file_object.close()
            
            self.fileRead = True
         return 1
        
#      print "char_count_and_read: Checking mail..."
      if self.dataReady("inbox"):
         print "char_count_and_read: Message received! (inbox)"
         self.fullfilename = self.recv("inbox")
         print "char_count_and_read: Message from inbox is...", self.fullfilename
         self.fileRead = False         
         return 1

      if self.dataReady("control"):
         print "char_count_and_read: Message received! (control)" 
         self.controlMessage = self.recv("control")

         if isinstance(self.controlMessage, producerFinished):
            self.send(producerFinished("Done"), "signal")
            return 0
      return 1  

   def closeDownComponent(self):
      print "char_count_and_read: Shutting down"
      
            
class UserInterface(component):
   def __init__(self,
                protocol=ServerProtocolHandler,
                port=1616,
                demo_mode=False):
       
      #self.__super.__init__()
      super(UserInterface,self).__init__()

      self.protocol = protocol
      self.port = port
      self.demo_mode = demo_mode

      self.displaySet = False
      self.size = width, height = 800, 600
      self.black = 0, 0, 0
      FULLSCREEN = pygame.constants.FULLSCREEN
      
     # self.screen = pygame.display.set_mode(self.size,FULLSCREEN)
      self.screen = pygame.display.set_mode(self.size) 
                
   def mainBody(self):
      if self.demo_mode == True:
         if self.displaySet == False:                           
            try: self.start_button = pygame.image.load("UI_Pics/Start button.jpg")             
            except: raise "ErrorLoadingImage", "couldn't load start button"

            self.start_buttonRect = self.start_button.get_rect()               
            self.start_buttonRect = self.start_buttonRect.move(100, 100)

            try: self.reset_button = pygame.image.load("UI_Pics/Reset button.jpg")             
            except: raise "ErrorLoadingImage", "couldn't load start button"
            
            self.reset_buttonRect = self.reset_button.get_rect()               
            self.reset_buttonRect = self.reset_buttonRect.move(100, 100)

            self.screen.fill(self.black)
            self.screen.blit(self.start_button, self.start_buttonRect)
#            self.screen.blit(reset_button, self.reset_buttonRect)
                
            pygame.display.flip()
            self.displaySet = True

         for event in pygame.event.get():
           if event.type == pygame.QUIT:
              pygame.quit()
              raise "QUIT"
              return 0
           if event.type == pygame.MOUSEBUTTONDOWN:
              pos = pygame.mouse.get_pos()
              mouseRect = [[pos[0],pos[1]],[5,5]]
              mouseRect = pygame.Rect(mouseRect)
                  
              if pygame.mouse.get_pressed() == (1,0,0):                     
                 clickedStart = mouseRect.colliderect(self.start_buttonRect)
                 clickedReset = mouseRect.colliderect(self.reset_buttonRect)
                     
                 if clickedStart == True:
                    clickedStart = False

#                    try: self.reset_button = pygame.image.load("UI_Pics/Reset button.jpg")             
#                    except: raise "ErrorLoadingImage", "couldn't load start button"
#
#                    self.reset_buttonRect = self.reset_button.get_rect()               
#                    self.reset_buttonRect = self.reset_buttonRect.move(350, 350)

                    self.screen.fill(self.black)
#                    self.screen.blit(self.start_button, self.start_buttonRect)
                    self.screen.blit(self.reset_button, self.reset_buttonRect)
                
                    pygame.display.flip()

                    myServer = SimpleServer(self.protocol, self.port)
                    self.addChildren(myServer)
                    return newComponent(myServer)
                    
                 elif clickedReset == True:
                    clickedReset = False
                    sys.exit()
                
      elif self.demo_mode == False:
         myServer = SimpleServer(self.protocol, self.port)
         self.addChildren(myServer)
         return newComponent(myServer)
      return 1       
            
if __name__ == "__main__":
   from Kamaelia.SimpleServerComponent import SimpleServer
   
   protocol=ServerProtocolHandler
   port=1616
   demo_mode = True

   UserInterface(protocol, port, demo_mode).activate()
   
   import sys
   sys.path.append("../Layout")
   from Kamaelia.Utils.Introspector import Introspector
   from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
   from Kamaelia.Util.PipelineComponent import pipeline
   pipeline(Introspector(),_TCPClient("127.0.0.1",1500)).activate()
   
   scheduler.run.runThreads(slowmo=0)
