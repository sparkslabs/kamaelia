#!/usr/bin/python

import pygame, string
pygame.init()

class MyDisplay:

    def surface_from_image_file(self, fullfilename):
        """
        Takes the filename, loads it and finally returns the surface
        """
        try:
#            print "surface_from_image_file: loading file", fullfilename
            return pygame.image.load(fullfilename)
        except:
            print 'Invalid filename or location', fullfilename
            print 'Using default picture... No Picture.jpg'
            file = os.path.split(fullfilename)
            filename_components = [file[1], "No Picture.jpg"]
            fullfilename = string.join(filename_components, "") 
            return pygame.image.load(fullfilename)
            

       
    def surface_from_string(self,
                            list_strings,
                            alignment=0,
                            font_size=20,
                            back_colour=(0,0,0),
                            font_colour=(255,255,255)):
        """
        Cycles through the list of the strings.
        Converts each string into a surface containing that string.
        In display terms, it places each string surface below the previous.
        Returns a single surface of all the string surfaces.

        The strings can be centre, left or right aligned depending upon the value assigned to
        'alignment':
           alignment = 0, Left
           alignment = 1, Centre
           alignment = 2, Right
        """
        
        self.list_surface = []
        self.list_rect = []
        line_coords = [0,0]

        if alignment != 0 and alignment != 1 and alignment != 2:
           #Check whether valid alignment value was used
           raise "Invalid aligment value!", alignment
        
        for string in list_strings:
           #Loops through the list of strings converting them into surfaces
           #Gets a rect for each surface
           #Adds each created surface to a list of surfaces
           #Adds each created rect to a list of rects
            
#           print "surface_from_string: creating surface and rect from string"
           font = pygame.font.Font(None,font_size)                      #Font
           self.string_surface = font.render(string, 1, font_colour)    #Surface
           self.string_rect = self.string_surface.get_rect()            #Rect

#           print "surface_from_string: appending surface and rect to thier respective lists" 
           self.list_surface.append(self.string_surface)
           self.list_rect.append(self.string_rect)

#        print "surface_from_string: getting the width and height dimensions for new surface"
        max_width = self.get_max_width(self.list_surface)     #find the longest width of all the string surfaces
        max_height = self.get_total_height(self.list_surface) #get total height of all the surfaces

        #Maximum dimensions the new surface will need to be to contain all the strings
        self.dialoguesize = max_width, max_height

#        print "surface_from_string: creating surface to contain the strings"
        surface_dialogue = pygame.Surface(self.dialoguesize)
        surface_dialogue.fill(back_colour)

#        print "surface_from_string: arranging string surfaces"
        for index in range(len(list_strings)):
            #Cycles through the list rects using an index.
            #Moves each surface below the previous
            #Any horizontal movement is also done at this stage
            #NOTE: should be the same number of items in list_strings, list_surfaces, list_rects.
            
            line_coords[1] = (font_size * index)       #calculate distance needed to move surface below the previous
            surface_position = ( 0, line_coords[1] )   #coords of where the surface is to be
            surface = self.list_surface[index]         #get surface

            self.list_rect[index] = self.align_surface(surface, surface_position, alignment, self.dialoguesize) #move surface
            
            surface_dialogue.blit(surface, self.list_rect[index]) #copy string surface to dialogue surface

        return surface_dialogue

    
    def prepare_display(self,
                        list_surface_components,
                        back_colour=[0,0,0],
                        display_size=[1000, 800]):
        """
        surface_components = [surface, position=[0,0], alignment_type=[0,0]]
        Takes a list of surfaces and thier components.
        Cycles through the list moving and blitting the provided surfaces to the screen surface.
        """
        
#        print "prepare_display: Creating display"
        screen = pygame.display.set_mode(display_size)        #Surface
        screen.fill(back_colour)

        for surface_components in list_surface_components:
            
            self.surface = surface_components[0]
            self.position = surface_components[1]
            self.alignment_type = surface_components[2]

            #creates a rect and moves it.
            rect = self.align_surface(self.surface, self.position, self.alignment_type, display_size)

#            print "prepare_display: blitting" 
            screen.blit(self.surface, rect)


    def display(self):
        """
        Displays what has been blitted to the screen surface
        """
#        print "display: flipping"
        pygame.display.flip()
#        print "display: waiting"
        self.display_wait()
#        print "display: finished"


    def align_surface(self, surface, position=[0,0], alignment_type=0, display_size=[1000, 800]):
        """
        Places the surface in a designanted place determined by the value of 'alignment_type'.
        These case's are true provided 'position' is [0,0]:
           alignment_type = 0, Top left / Custom (user defined using 'position')
           alignment_type = 1, Top middle
           alignment_type = 2, Top right
           alignment_type = 3, Middle left
           alignment_type = 4, Centre
           alignment_type = 5, Middle right
           alignment_type = 6, Bottom left
           alignment_type = 7, Bottom middle
           alignment_type = 8, Bottom right
        """
        
        self.surface = surface
        rect = self.surface.get_rect()
        d_size = display_size
        s_size = self.surface.get_size()
        
        if alignment_type == 0:
            return rect.move(position)
        
        elif alignment_type == 1:
            x_coord = self.mid_coord(s_size[0], d_size[0])
            return rect.move([ x_coord, position[1] ])
        
        elif alignment_type == 2:
            x_coord = self.rigORbot_coord(s_size[0], d_size[0])
            return rect.move([ x_coord, position[1] ])
        
        elif alignment_type == 3:
            y_coord = self.mid_coord(s_size[1], d_size[1])
            return rect.move([ position[0], y_coord ])
        
        elif alignment_type == 4:
            x_coord = self.mid_coord(s_size[0], d_size[0])
            y_coord = self.mid_coord(s_size[1], d_size[1])
            return rect.move([ x_coord, y_coord ])
        
        elif alignment_type == 5:
            x_coord = self.rigORbot_coord(s_size[0], d_size[0])
            y_coord = self.mid_coord(s_size[1], d_size[1])
            return rect.move([ x_coord, y_coord ])
        
        elif alignment_type == 6:
            y_coord = self.rigORbot_coord(s_size[1], d_size[1])
            return rect.move([ position[0], y_coord ])
        
        elif alignment_type == 7:
            x_coord = self.mid_coord(s_size[0], d_size[0])
            y_coord = self.rigORbot_coord(s_size[1], d_size[1])
            return rect.move([ x_coord, y_coord ])
        
        elif alignment_type == 8:
            x_coord = self.rigORbot_coord(s_size[0], d_size[0])
            y_coord = self.rigORbot_coord(s_size[1], d_size[1])
            return rect.move([ x_coord, y_coord ])
        else:
            raise 'Invalid alignment_type was used!'

        
    def rigORbot_coord(self, surface_length, display_length):
        """
        Returns a coordinate of the top left corner of a surface which is
        to be right or bottom aligned in the display surface. 
        """
        return (display_length - surface_length)

    
    def mid_coord(self, surface_length, display_length):
        """
        Returns a coordinate of the top left corner of a surface which is
        to be centred in the display surface.
        """
        return (display_length - surface_length)/2
    

    def get_max_width(self, list_of_surfaces):
        """
        Checks the width of each surface to find out the maximum width.
        """
        max_width = 0
        for surface in list_of_surfaces:
           width = surface.get_width()
           if max_width == 0:
               max_width = width
           elif width > max_width:
               max_width = width
        return max_width

    def get_total_height(self, list_of_surfaces):
        total_height = 0
        for surface in list_of_surfaces:
            total_height = total_height + surface.get_height()
        return total_height
    

    def display_wait(self):
        """
        Continueously polls an event queue for two particular events (closure
        of window and a keyboard key press). Closes image upon discovery of either event.
        """
        import time
        timeout=3
        t = time.time()
        while 1:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
#                   print "display_wait: User interaction, shutting down"
                   pygame.quit()
               if event.type == pygame.KEYDOWN:
                   return 0
           if timeout and time.time()-t>timeout:
              return
