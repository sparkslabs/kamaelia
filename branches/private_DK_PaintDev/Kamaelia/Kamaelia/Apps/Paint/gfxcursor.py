"""
This is a nice little GfxCursor class that gives you arbitrary mousecursor
loadable from all SDL_image supported filetypes. 

Author: Raiser, Frank aka CrashChaos (crashchaos at gmx.net)
Author: Shinners, Pete aka ShredWheat
Version: 2001-12-15

Usage:
Instantiate the GfxCursor class. Either pass the correct parameters to
the constructor or use setCursor, setHotspot and enable lateron.

The blitting is pretty optimized, the testing code at the bottom of
this script does a pretty thorough test of all the drawing cases.
It enables and disables the cursor, as well as uses a changing background.

In your mainloop, the cursor.show() should be what you draw last
(unless you want objects on top of the cursor?). Then before drawing
anything, be sure to call the hide(). You can likely call hide() immediately
after the display.flip() or display.update().

The show() method also returns a list of rectangles of what needs to be
updated. You can also move the cursor with pygame.mouse.set_pos()


That's it. Have fun with your new funky cursors.
"""

import pygame

class GfxCursor:
    """
    Replaces the normal pygame cursor with any bitmap cursor
    """

    def __init__(self,surface,cursor=None,hotspot=(0,0)):
        """
        surface = Global surface to draw on
        cursor  = surface of cursor (needs to be specified when enabled!)
        hotspot = the hotspot for your cursor
        """
        self.surface = surface
        self.enabled = 0
        self.cursor  = None
        self.hotspot = hotspot
        self.bg      = None
        self.offset  = 0,0
        self.old_pos = 0,0
        
        if cursor:
            self.setCursor(cursor,hotspot)
            self.enable()

    def enable(self):
        """
        Enable the GfxCursor (disable normal pygame cursor)
        """
        if not self.cursor or self.enabled: return
        pygame.mouse.set_visible(0)
        self.enabled = 1

    def disable(self):
        """
        Disable the GfxCursor (enable normal pygame cursor)
        """
        if self.enabled:
            self.hide()
            pygame.mouse.set_visible(1)
            self.enabled = 0

    def setCursor(self,cursor,hotspot=(0,0)):
        """
        Set a new cursor surface
        """
        if not cursor: return
        self.cursor = cursor
        self.hide()
        self.show()
        self.offset = 0,0
        self.bg = pygame.Surface(self.cursor.get_size())
        pos = self.old_pos[0]-self.offset[0],self.old_pos[1]-self.offset[1]
        self.bg.blit(self.surface,(0,0),
            (pos[0],pos[1],self.cursor.get_width(),self.cursor.get_height()))

        self.offset = hotspot

    def setHotspot(self,pos):
        """
        Set a new hotspot for the cursor
        """
        self.hide()
        self.offset = pos

    def hide(self):
        """
        Hide the cursor (useful for redraws)
        """
        if self.bg and self.enabled:
            return self.surface.blit(self.bg,
                (self.old_pos[0]-self.offset[0],self.old_pos[1]-self.offset[1]))

    def show(self):
        """
        Show the cursor again
        """
        if self.bg and self.enabled:
            pos = self.old_pos[0]-self.offset[0],self.old_pos[1]-self.offset[1]
            self.bg.blit(self.surface,(0,0),
                (pos[0],pos[1],self.cursor.get_width(),self.cursor.get_height()))
            return self.surface.blit(self.cursor,pos)

    def update(self,event):
        """
        Update the cursor with a MOUSEMOTION event
        """
        self.old_pos = event.pos

if __name__ == '__main__': #test it out
    import pygame.draw
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    screen.fill((50, 50, 111), (0, 0, 400, 150))
    pygame.display.flip()
    pygame.display.set_caption('Test the GfxCursor (and paint)')
    
    image = pygame.Surface((20, 20))
    pygame.draw.circle(image, (50, 220, 100), (10, 10), 8, 0)
    pygame.draw.circle(image, (220, 200, 50), (10, 10), 8, 2)
    image.set_at((9, 9), (255,255,255))
    image.set_colorkey(0, pygame.RLEACCEL)
    
    magicbox = pygame.Rect(10, 10, 100, 90)
    magiccolor = 0
    
    cursor = GfxCursor(screen, image, (10, 10))
    finished = 0
    downpos = None
    while not finished:
        dirtyrects = []
        dirtyrects.extend([cursor.hide()])
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN):
                finished = 1
                break
            elif e.type == pygame.MOUSEBUTTONDOWN:
                cursor.disable()
                downpos = e.pos
            elif e.type == pygame.MOUSEBUTTONUP:
                cursor.enable()
                downpos = None
            elif downpos and e.type == pygame.MOUSEMOTION:
                r = pygame.draw.line(screen, (100,100,100), downpos, e.pos, 10)
                dirtyrects.append(r)
                downpos = e.pos
                cursor.update(e)
            elif not downpos and e.type == pygame.MOUSEMOTION:
                cursor.update(e)
        
        magiccolor = (magiccolor + 2) % 255
        r = screen.fill((0, 0, magiccolor), magicbox)
        dirtyrects.append(r)
        
        #here's how we sandwich the flip/update with cursor show and hide
        dirtyrects.extend([cursor.show()])
        pygame.display.update(dirtyrects)
        
        pygame.time.delay(5) #should be time.wait(5) with pygame-1.3 :]
