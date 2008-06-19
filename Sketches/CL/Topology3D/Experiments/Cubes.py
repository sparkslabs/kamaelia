"""\
Rendering an OpenGL sphere to serve as particles of Topology 

References: pygame + PyOpenGL version of Nehe's OpenGL (Paul Furber) and PyOpenGL demos
"""

from OpenGL.GL import *
from OpenGL.GLU import *
#from OpenGL.GLUT import *

import pygame
from pygame.locals import *

xrot = yrot = zrot = 0.0

def resize((width, height)):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    global quadratic, textures
    
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
    
    global texID, imageSize, textureSize
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
    
    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texID)
    
    
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
#    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)



def draw():
    global xrot, yrot, zrot, quadratic, texID, imageSize, textureSize

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);    
    
    glLoadIdentity();                        
    glTranslatef(0.0,0.0,-5.0)

    glRotatef(xrot,1.0,0.0,0.0)            # Rotate The Cube On It's X Axis
    glRotatef(yrot,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis
    glRotatef(zrot,0.0,0.0,1.0)            # Rotate The Cube On It's Z Axis
    
    glColor3f(1.0,0.0,0.0)
   
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
    
    xrot  = xrot + 0.2                # X rotation
    yrot = yrot + 0.2                 # Y rotation
    zrot = zrot + 0.2                 # Z rotation      
    

def main():

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
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        
        draw()
        pygame.display.flip()
        frames = frames+1

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()

