#!/usr/bin/python

import pygame, pygame_display, os, string

from Axon.Scheduler import scheduler
from Axon.Component import component 
from Kamaelia.Util.PipelineComponent import pipeline

class producer(component):
   "Reads a line of text from a named file then sends it to its outbox indefinitely"
   def __init__(self, filename):
       super(producer,self).__init__()
       self.boxes = { "inbox": [],  "outbox": [] }
       self.filename = filename      
   def main(self):
      f = open(self.filename, "r")       
      while 1:
         text = f.readline()
         self.send(text, "outbox")
         yield 1



class demodulation(component):
    "Filters out messages 'ACT', 'SCENE' and actions. All others messages are forwarded indefinitely"
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                text = self.recv("inbox")
                if text[:3] == "ACT":
                    pass
                elif text[:5] ==  "SCENE":
                    pass                     
                elif text[4:9] == "Enter":
                    pass
                elif text[4:10] == "Exeunt":
                    pass
                elif text[4:8] == "Exit":
                    pass
                else:
                    get_rid_of_newline = len(text)-1
                    text = text[:get_rid_of_newline]

                    if text == "":
                        text = "     "
                        
                    self.send(text, "outbox")
            yield 1



class error_correction(component):
    "Creates a banner if the message starts with 'Twelfth' and sends it to it's outbox indefinitely"
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                text = self.recv("inbox")
                if text[:7] == "Twelfth":
                    title_string = []                   
                    title_string.append("TWELFTH NIGHT")
                    title_string.append("by")
                    title_string.append("William Shakespeare")

                    
                    #this stuff deals with displaying the strings in title
                    pygame.init()
                    
                    string_surface = myDisplay.surface_from_string(title_string, alignment=1)
                    
                    self.string_surface_components = [string_surface, [0,0], 4]
                    self.list_surface_components = [self.string_surface_components]
                    myDisplay.prepare_display(self.list_surface_components)

                    myDisplay.display()
                    
                    #debug

                else:
                    self.send(text, "outbox")
            yield 1


class demultiplexing(component):
    "Looks for the name of someone about to speak and adds it to a list together with what they say."
    def main(self):
        got_name = 0
        blank_line_flag = 0  #flag used to prevent extra blank lines being printed
        dialogue = []        #list to store what is said and name of speaker ( dialogue[0] )

        while 1:
            if self.dataReady("inbox"):
                text = self.recv("inbox")
                if text[0] != " " and text != "     ":                #Checking for a name
                    if got_name == 1:             #Someone else about to start speaking
                        message = dialogue
                        self.send(message, "outbox")
                        got_name = 0
                        blank_line_flag = 0
                        dialogue = []
                    if got_name == 0:                              #No one speaking
                        dialogue.append(text[0:])
                        got_name = 1     
                elif text[0] == " " and got_name == 1:             #Build up a string of speech
                    dialogue.append(text[4:])
                    blank_line_flag = 0
                elif text == "     " and got_name == 1:               #Make sure paragraphs in speech are kept
                    if blank_line_flag == 0:                       #but dont create blank lines for no reason
                        dialogue.append(text)
                        blank_line_flag = 1
            yield 1

class decode(component):
    "Takes a message from it's inbox, decodes it and sends it to it's outbox indefinitely"
    def __init__(self, picture_directory):
       super(decode,self).__init__()
       self.boxes = { "inbox": [],  "outbox": [] }
       self.picture_directory = picture_directory
    def main(self):
        dict_spea_sur = {}
        while 1:
            
            if self.dataReady("inbox"):
                
               pygame.init()
               
               dialogue = self.recv("inbox")
               
               name_of_speaker = dialogue[0]
                  
               if os.path.isdir(self.picture_directory)==True: #check validity of supplied directory
                   
                     
                  #creating possible pathname of where to locate the picture file for this speaker 
                  filename_components = [name_of_speaker, ".jpg"]
                  filename_of_speaker = string.join(filename_components, "")
                  fullfilename = os.path.join(self.picture_directory, filename_of_speaker)


                  #check validity of possible picture source. Use a default picture if it is not valid   
                  if os.path.isfile(fullfilename)==False:
                      fullfilename = os.path.join(self.picture_directory, "No Picture.jpg")

                  picture_surface = myDisplay.surface_from_image_file(fullfilename)
                  
                  message = [dialogue, picture_surface]
                  self.send(message, "outbox")

               else:
                  raise "Invalid directory used for source of pictures", self.picture_directory
                
            yield 1



class video_scaling(component):
    "Takes a message from it's inbox, does stuff to it and sends it to it's outbox indefinitely"
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                
                pygame.init()                
                self.list_surface_components = []
                
                message = self.recv("inbox")

                dialogue_list = message[0]
                self.dialogue_surface = myDisplay.surface_from_string(dialogue_list, alignment=0)
                self.string_surface_components = [self.dialogue_surface, [0,0], 4]
                self.list_surface_components.append(self.string_surface_components)

                self.picture_surface = message[1]
                self.picture_surface_components = [self.picture_surface, [0,0], 3]
                self.list_surface_components.append(self.picture_surface_components)

                self.send(self.list_surface_components, "outbox")
            yield 1

class display(component):
    "Takes a message from it's inbox, does stuff to it and sends it to it's outbox indefinitely"
    def main(self):
        while 1:
            if self.dataReady("inbox"):
               pygame.init()
               self.list_surface_components = self.recv("inbox")
               
               myDisplay.prepare_display(self.list_surface_components)
               myDisplay.display()  
               #debug
               
            yield 1

myDisplay = pygame_display.MyDisplay()
display_size = [1000, 800]

filename = "twelfthnight.txt"
picture_directory = "characters"

app  = pipeline(producer(filename),
                demodulation(),
                error_correction(),
                demultiplexing(),
                decode(picture_directory),
                video_scaling(),
                display())

app.activate()
scheduler.run.runThreads(slowmo=0)

