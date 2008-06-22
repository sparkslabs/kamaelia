from OpenGL.GL import *
from OpenGL.GLU import *
from THF.Kamaelia.UI.OpenGL.Vector import Vector

class Particle3D(object):
    def __init__(self, position = (-1,0,-10), ID='aaa', name='aaa', sidecolour=(200,200,244), size=(0.8,0.5,0.3)):
        self.pos = position
        self.sideColour = sidecolour
        self.size = size
        
    def render(self):
        """ Draw button cuboid."""
        print self.size
        hs = Vector(*self.size)/2
        print hs
        glLoadIdentity()                        
        #glTranslatef(self.pos[0],self.pos[1],self.pos[2])
        glTranslatef(*self.pos)
        glScalef(2.1,2.1,2.1)
        glRotatef(20.2,1.0,0.0,0.0)
        glRotatef(20.2,0.0,1.0,0.0)
        glRotatef(2.2,0.0,0.0,1.0)
        #print self.tex_w, self.tex_h
        # draw faces
        glBegin(GL_QUADS)
        glColor4f(self.sideColour[0]/256.0, self.sideColour[1]/256.0, self.sideColour[2]/256.0, 0.5)

        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)

        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)

        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)

        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glEnd()

#        glEnable(GL_TEXTURE_2D)
#        glBindTexture(GL_TEXTURE_2D, self.texID)
#        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

        glBegin(GL_QUADS)
        # back plane
        #glTexCoord2f(self.tex_w, 1.0-self.tex_h)
        glVertex3f(hs.x,hs.y,-hs.z)
        #glTexCoord2f(0.0, 1.0-self.tex_h)
        glVertex3f(-hs.x,hs.y,-hs.z)
        #glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        #glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x,-hs.y,-hs.z)
        # front plane
        #glTexCoord2f(0.0, 1.0-self.tex_h)
        glVertex3f(-hs.x,-hs.y,hs.z)
        #glVertex3f(-2.0, -1.0,  1.0)
        #glTexCoord2f(self.tex_w, 1.0-self.tex_h)
        glVertex3f(hs.x,-hs.y,hs.z)
        #glVertex3f( 2.0, -1.0,  1.0)
        #glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x,hs.y,hs.z)
        #glVertex3f( 2.0,  5.0,  1.0) 
        #glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x,hs.y,hs.z)
        #glVertex3f(-2.0,  5.0,  1.0)
        glEnd()
        
        #glDisable(GL_TEXTURE_2D)