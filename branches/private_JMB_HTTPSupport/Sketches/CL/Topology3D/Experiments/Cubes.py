"""\
Rendering an OpenGL sphere to serve as particles of Topology 

References: pygame + PyOpenGL version of Nehe's OpenGL (Paul Furber) and PyOpenGL demos
THF's OpenGL codes
"""

from OpenGL.GL import *
from OpenGL.GLU import *
#from OpenGL.GLUT import *

import pygame
from pygame.locals import *

#xrot = yrot = zrot = 0.0

xrot = yrot = 0.0
xspeed = yspeed = 0.0
x = y = 0.0
z = -5.0

textures = []
filter = 0
light = 0
blend = 0



def resize((widthIn, heightIn)):
    global width, height
    height=heightIn
    width=widthIn
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 1.0, 100.0)
    #glOrtho(-5.0*width/height, 5.0*width/height, -5.0, 5.0, 5.0, -5.0)
    
#    glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    global quadratic
    
    # Create a quadratic object for sphere rendering
    quadratic = gluNewQuadric()
    #gluQuadricDrawStyle( quadratic, GLU_FILL )
    #gluQuadricDrawStyle( quadratic, GLU_LINE )
    #gluQuadricDrawStyle( quadratic, GLU_SILHOUETTE )
    gluQuadricNormals(quadratic, GLU_SMOOTH)
    gluQuadricTexture(quadratic, GL_TRUE)
    glEnable(GL_TEXTURE_2D)    
    
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 1.0, 0.0, 0.0)
    glClearDepth(1.0)
    
      
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    
    LightAmbient  = ( (0.5, 0.5, 0.5, 1.0) )
    LightDiffuse  = ( (1.0, 1.0, 1.0, 1.0) )
    LightPosition = ( (0.0, 0.0, 2.0, 1.0) )
    glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
    glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
    glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
    glEnable( GL_LIGHT1 )
    glColor4f( 1.0, 1.0, 1.0, 0.5)
    glBlendFunc( GL_SRC_ALPHA, GL_ONE )
    
#    # Add light
#    light_ambient =  [0.0, 0.0, 0.0, 1.0]
#    light_diffuse =  [1.0, 1.0, 1.0, 1.0]
#    light_specular =  [1.0, 1.0, 1.0, 1.0]
#    light_position =  [1.0, 1.0, 1.0, 0.0]
#
#    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
#    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
#    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
#    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
#   
#    glEnable(GL_LIGHTING)
#    glEnable(GL_LIGHT0)
#    glEnable(GL_DEPTH_TEST)


def buildLabel(text):
    """Pre-render the text to go on the label."""    
    
    global textures, imageSize, textureSize
    fontColor = (0,0,255)
    imageColor = (128,128,128)
    textureColor = (244,244,244)
    
    
    # Text texture
    pygame.font.init()
    font = pygame.font.Font(None, 20)
    image = font.render(text,True, fontColor, imageColor)
    
    imageSize = image.get_width(), image.get_height()
    textureSize = (64, 64)
    
    textureSurface = pygame.Surface(textureSize) # The size has to be power of 2
    textureSurface.fill(textureColor)
    textureSurface.blit(image, ((textureSurface.get_width()-image.get_width())/2,
                                (textureSurface.get_height()-image.get_height())/2))
    textureSurface = textureSurface.convert_alpha()
    
    print image.get_width(), image.get_height()
    
#    # Picture texture
#    texturefile = os.path.join('data','nehe.bmp')
#    textureSurface = pygame.image.load('nehe.bmp')
    
    textureData = pygame.image.tostring(textureSurface, "RGBX", 1)
    
    textures = glGenTextures(3)
    #glBindTexture(GL_TEXTURE_2D, texID)        
#    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
#                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
#    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, textures[1])
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )

    glBindTexture( GL_TEXTURE_2D, textures[2])
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    gluBuild2DMipmaps( GL_TEXTURE_2D, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                       GL_RGBA, GL_UNSIGNED_BYTE, textureData);



def draw():
    global quadratic, textures, imageSize, textureSize, x, y, z, xspeed, yspeed, xrot, yrot, zrot

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    
    glLoadIdentity();                        
    glTranslatef(x,y,z)

    glRotatef(xrot,1.0,0.0,0.0)            # Rotate The Cube On It's X Axis
    glRotatef(yrot,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis
#    glRotatef(zrot,0.0,0.0,1.0)            # Rotate The Cube On It's Z Axis
    
#    glRotatef(30.0,1.0,0.0,0.0)            # Rotate The Cube On It's X Axis
#    glRotatef(30.0,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis
#    glRotatef(0.0,0.0,0.0,1.0)            # Rotate The Cube On It's Z Axis
    
    #glColor3f(1.0,0.0,0.0)
    
#    # viewing transformation 
#    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
#    glScalef (1.0, 2.0, 1.0)      # modeling transformation

#    glBegin(GL_QUADS)    
#    glVertex3f(-1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
#    glVertex3f( 1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
#    glVertex3f( 1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
#    glVertex3f(-1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad
#    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures[filter])
   
    glBegin(GL_QUADS)    
    
    # Front Face (note that the texture's corners have to match the quad's corners)
    glTexCoord2f((textureSize[0]-imageSize[0])*0.5/textureSize[0], (textureSize[1]-imageSize[1])*0.5/textureSize[1]); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1-(textureSize[0]-imageSize[0])*0.5/textureSize[0], (textureSize[1]-imageSize[1])*0.5/textureSize[1]); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1-(textureSize[0]-imageSize[0])*0.5/textureSize[0], 1-(textureSize[1]-imageSize[1])*0.5/textureSize[1]); glVertex3f( 1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f((textureSize[0]-imageSize[0])*0.5/textureSize[0], 1-(textureSize[1]-imageSize[1])*0.5/textureSize[1]); glVertex3f(-1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad
    
 
    # Back Face
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    # Bottom Left Of The Texture and Quad
    
    # Top Face
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
    
    # Bottom Face       
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
    
    # Right face
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
    
    # Left Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
        
    glEnd()
        
    xrot += xspeed
    yrot += yspeed
    
#    xrot  = xrot + 0.2                # X rotation
#    yrot = yrot + 0.2                 # Y rotation
#    zrot = zrot + 0.2                 # Z rotation      
    
    
def handleKeys(key):
    global filter, light, x, y, z, xspeed, yspeed, blend

    if key == K_ESCAPE:
        return 0
    if key == K_f:
        filter = filter + 1
        if filter == 3:
            filter = 0
    elif key == K_l:
        light = not light
        if not light:
            glDisable(GL_LIGHTING)
        else:
            glEnable(GL_LIGHTING)
    elif key == K_b:
        blend = not blend
        if blend:
            glEnable(GL_BLEND)
            glDisable(GL_DEPTH_TEST)
        else:
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_BLEND)
    elif key == K_PAGEUP:
        z -= 0.05
    elif key == K_PAGEDOWN:
        z += 0.05
    elif key == K_UP:
        xspeed -= 0.01
    elif key == K_DOWN:
        xspeed += 0.01
    elif key == K_LEFT:
        yspeed -= 0.01
    elif key == K_RIGHT:
        yspeed += 0.01
    elif key == K_w:
        y += 0.2
    elif key == K_s:
        y -= 0.2
    elif key == K_a:
        x -= 0.2
    elif key == K_d:
        x += 0.2
            
    
    return 1

def doPicking(pos):
    """\
    Uses OpenGL picking to determine objects that have been hit by mouse pointer.
    see e.g. OpenGL Redbook
    """
    global width, height
    
    # object picking
    glSelectBuffer(512)
    glRenderMode(GL_SELECT)
    
    glInitNames()
    glPushName(0)
    
    
    
    # prepare matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPickMatrix(pos[0], height-pos[1], 1, 1, viewport=None)
    gluPerspective(45, 1.0*width/height, 1.0, 100.0)
    


    # "draw" objects in select mode
    
    glMatrixMode(GL_MODELVIEW) # Always load GL_MODELVIEW before drawing
    glPushMatrix()

    glLoadName(1)
    draw()
    
#
    # restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    
    glMatrixMode(GL_MODELVIEW) # Always load GL_MODELVIEW before drawing
    glPopMatrix()
    
    # force completion
    glFlush()

    # process hits                
    hits = glRenderMode(GL_RENDER)
    print hits
    hitlist = []
    hitall = False
    if hitall:
        # list of hit objects
        hitlist = [hit[2][0] for hit in hits]
    else:
        nearest = 4294967295
        for hit in hits:
            if hit[0] < nearest:
                nearest = hit[0]
                hitlist = [hit[2][0]]
                
    return hitlist

def main():
    global yspeed
    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode((640,480), video_flags)

    resize((640,480))
    init()
    buildLabel('Particle')
    
    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT:
            break
        if event.type == KEYDOWN:
            if handleKeys(event.key) == 0:
                break
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hitobjects = doPicking(event.pos)
                    print hitobjects
                    if 1 in hitobjects:
                        if yspeed == 0.0:
                            yspeed = 0.02
                        else:
                            yspeed = 0.0
                
        
        draw()
        pygame.display.flip()
        frames = frames+1

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()

