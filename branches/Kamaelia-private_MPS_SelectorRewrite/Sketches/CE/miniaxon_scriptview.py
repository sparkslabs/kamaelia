#!/usr/bin/python

import pygame, pygame_display, os, string

class microprocess:
   def __init__(self): pass
   def main(self):
      yield -1

class scheduler:
   def __init__(self):
      self.active = []
   def main(self):
       while 1:
#      for i in range(100):
         newqueue = []
         for current in self.active:
            if current.next() != -1:
               newqueue.append(current)
         self.active = newqueue
         yield 1
   def activateMicroprocess(self,someprocess):
      x = someprocess.main()
      self.active.append(x)


class simplecomponent(microprocess):
   def __init__(self):
      self.boxes = { "inbox": [],  "outbox": [] }
   def send(self, boxname, value):
      "Appends the message to the named inbox"
      self.boxes[boxname].append(value)
   def recv(self,boxname):
      "Removes the first message in the named inbox"
      result = self.boxes[boxname][0]
      del self.boxes[boxname][0]
      return result
   def dataReady(self, boxname):
      "See if there's any messages returns True if there are any messages on the named inbox"
      return len(self.boxes[boxname])



class producer(simplecomponent):
   "Reads a line of text from a named file then sends it to its outbox indefinitely"
   def __init__(self, filename):
       self.boxes = { "inbox": [],  "outbox": [] }
       self.filename = filename      
   def main(self):
#      print "producer: Opening file"
      f = open(self.filename, "r")       
      while 1:
#         print "producer: Reading file"
         text = f.readline()
#         print "producer: Posting to outbox"
         self.send("outbox", text)
#         print "producer: Finished"
         yield 1



class demodulation(simplecomponent):
    "Filters out messages 'ACT', 'SCENE' and actions. All others messages are forwarded indefinitely"
    def main(self):
        while 1:
#            print "demodulation: Checking inbox"
            if self.dataReady("inbox"):
#                print "demodulation: Message received!"
                text = self.recv("inbox")
#                print "demodulation: Checking..."
                if text[:3] == "ACT":
                    pass
#                    print "demodulation: Ignoring ACT"
                elif text[:5] ==  "SCENE":
                    pass                     
#                    print "demodulation: Ignoring SCENE"
                elif text[4:9] == "Enter":
                    pass
#                    print "demodulation: Ignoring Action"
                elif text[4:10] == "Exeunt":
                    pass
#                    print "demodulation: Ignoring Action"
                elif text[4:8] == "Exit":
                    pass
#                    print "demodulation: Ignoring Action"
                else:
                    get_rid_of_newline = len(text)-1
                    text = text[:get_rid_of_newline]

                    if text == "":
                        text = "     "
                        
#                    print "demodulation: Posting to outbox"
                    self.send("outbox",text)
#                    print "demodulation: Finished"
            yield 1



class error_correction(simplecomponent):
    "Creates a banner if the message starts with 'Twelfth' and sends it to it's outbox indefinitely"
    def main(self):
        while 1:
#            print "error_correction: Checking inbox"
            if self.dataReady("inbox"):
#                print "error_correction: Message received!"
                text = self.recv("inbox")
#                print "error_correction: Checking..."
                if text[:7] == "Twelfth":
                    title_string = []                   
                    title_string.append("TWELFTH NIGHT")
                    title_string.append("by")
                    title_string.append("William Shakespeare")

#                    print title_string
                    
                    #this stuff deals with displaying the strings in title
                    pygame.init()
                    
                    string_surface = myDisplay.surface_from_string(title_string, alignment=1)
                    
                    self.string_surface_components = [string_surface, [0,0], 4]
                    self.list_surface_components = [self.string_surface_components]
                    myDisplay.prepare_display(self.list_surface_components)

                    myDisplay.display()
                    
                    #debug
#                    raw_input()

                else:
#                    print "error_correction: Posting to outbox"
                    self.send("outbox",text)
#                    print "error_correction: Finished"
            yield 1


class demultiplexing(simplecomponent):
    "Looks for the name of someone about to speak and adds it to a list together with what they say."
    def main(self):
        got_name = 0
        blank_line_flag = 0  #flag used to prevent extra blank lines being printed
        dialogue = []        #list to store what is said and name of speaker ( dialogue[0] )

        while 1:
#            print "demultiplexing: Checking inbox"
            if self.dataReady("inbox"):
#                print "demultiplexing: Message received!"
                text = self.recv("inbox")
#                print "demultiplexing: Checking..."
                if text[0] != " " and text != "     ":                #Checking for a name
                    if got_name == 1:             #Someone else about to start speaking
#                        print "demultiplexing: Someone stopped speaking"
#                        print "demultiplexing: Posting to outbox what was said and who said it"
                        message = dialogue
                        self.send("outbox",message)
#                        print dialogue
#                        print "demultiplexing: Reseting variables"
                        got_name = 0
                        blank_line_flag = 0
                        dialogue = []
#                        print "demultiplexing: Finished"  
                    if got_name == 0:                              #No one speaking
                        dialogue.append(text[0:])
#                        print "demultiplexing: Got the name of the speaker...", dialogue[0]
                        got_name = 1     
                elif text[0] == " " and got_name == 1:             #Build up a string of speech
#                    print "demultiplexing: Someone is speaking"
                    dialogue.append(text[4:])
                    blank_line_flag = 0
                elif text == "     " and got_name == 1:               #Make sure paragraphs in speech are kept
                    if blank_line_flag == 0:                       #but dont create blank lines for no reason
                        dialogue.append(text)
                        blank_line_flag = 1
            yield 1

class decode(simplecomponent):
    "Takes a message from it's inbox, decodes it and sends it to it's outbox indefinitely"
    def __init__(self, picture_directory):
       self.boxes = { "inbox": [],  "outbox": [] }
       self.picture_directory = picture_directory
    def main(self):
        dict_spea_sur = {}
        while 1:
            
#            print "decode: Checking inbox"
            if self.dataReady("inbox"):
                
               pygame.init()
               
#               print "decode: Message received!"
               dialogue = self.recv("inbox")
               
               name_of_speaker = dialogue[0]
                  
               if os.path.isdir(self.picture_directory)==True: #check validity of supplied directory
                   
#                  print "decode: Valid directory was provided" 
                     
                  #creating possible pathname of where to locate the picture file for this speaker 
                  filename_components = [name_of_speaker, ".jpg"]
                  filename_of_speaker = string.join(filename_components, "")
                  fullfilename = os.path.join(self.picture_directory, filename_of_speaker)

#                  print filename_components
#                  print filename_of_speaker
#                  print fullfilename

                  #check validity of possible picture source. Use a default picture if it is not valid   
                  if os.path.isfile(fullfilename)==False:
#                      print "decode: The speaker doesn't have a personal picture so using default"
                      fullfilename = os.path.join(self.picture_directory, "No Picture.jpg")

#                  print "decode: Got the picture surface"  
                  picture_surface = myDisplay.surface_from_image_file(fullfilename)
                  
#                  print "decode: creating message"
                  message = [dialogue, picture_surface]
#                  print "decode: Posting to outbox"
                  self.send("outbox",message)
#                  print "decode: Finished"

               else:
                  raise "Invalid directory used for source of pictures", self.picture_directory
                
            yield 1



class video_scaling(simplecomponent):
    "Takes a message from it's inbox, does stuff to it and sends it to it's outbox indefinitely"
    def main(self):
        while 1:
#            print "video_scaling: Checking inbox"
            if self.dataReady("inbox"):
                
                pygame.init()                
                self.list_surface_components = []
                
#                print "video_scaling: Message received!"
                message = self.recv("inbox")

                dialogue_list = message[0]
                self.dialogue_surface = myDisplay.surface_from_string(dialogue_list, alignment=0)
                self.string_surface_components = [self.dialogue_surface, [0,0], 4]
                self.list_surface_components.append(self.string_surface_components)

                self.picture_surface = message[1]
                self.picture_surface_components = [self.picture_surface, [0,0], 3]
                self.list_surface_components.append(self.picture_surface_components)

#                print "video_scaling: Posting to outbox"
                self.send("outbox",self.list_surface_components)
#                print "video_scaling: Finished"
            yield 1

class display(simplecomponent):
    "Takes a message from it's inbox, does stuff to it and sends it to it's outbox indefinitely"
    def main(self):
        while 1:
#            print "display: Checking inbox"
            if self.dataReady("inbox"):
               pygame.init()
#               print "display: Message received!"
               self.list_surface_components = self.recv("inbox")
               
               myDisplay.prepare_display(self.list_surface_components)
               myDisplay.display()  
               #debug
#               raw_input()
               
            yield 1



class postman(simplecomponent):
   "Takes messages from outboxes of one simplecomponent and places in the inbox of another simplecomponent"
   def __init__(self, source, destination):
      self.source = source
      self.destination = destination
   def main(self):
      "Takes one message at a time from the outbox of one simplecomponent, and sends it to the inbox of the other simplecomponent only when there are messages"
      while 1:
         if self.source.dataReady("outbox"):
            collectedvalue = self.source.recv("outbox")
            self.destination.send("inbox", collectedvalue)
         yield 1


       
myDisplay = pygame_display.MyDisplay()
display_size = [1000, 800]

filename = "twelfthnight.txt"
picture_directory = "characters"

Pro = producer(filename)
Demo = demodulation()
Err = error_correction()
Demu = demultiplexing()
Deco = decode(picture_directory)
Vid = video_scaling()
Display = display()

postie1 = postman(Pro,Demo)
postie2 = postman(Demo,Err)
postie3 = postman(Err,Demu)
postie4 = postman(Demu,Deco)
postie5 = postman(Deco,Vid)
postie6 = postman(Vid,Display)

myscheduler = scheduler()

myscheduler.activateMicroprocess(Pro)
myscheduler.activateMicroprocess(postie1)
myscheduler.activateMicroprocess(Demo)
myscheduler.activateMicroprocess(postie2)
myscheduler.activateMicroprocess(Err)
myscheduler.activateMicroprocess(postie3)
myscheduler.activateMicroprocess(Demu)
myscheduler.activateMicroprocess(postie4)
myscheduler.activateMicroprocess(Deco)
myscheduler.activateMicroprocess(postie5)
myscheduler.activateMicroprocess(Vid)
myscheduler.activateMicroprocess(postie6)
myscheduler.activateMicroprocess(Display)
for i in myscheduler.main():
   pass







