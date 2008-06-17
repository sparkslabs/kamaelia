"""\
Rendering an OpenGL sphere to serve as particles of Topology 
TODO: add texture
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
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    global quadratic, textures
    
    # Create a quadratic object for sphere rendering
    quadratic = gluNewQuadric()
    #gluQuadricDrawStyle( quadratic, GLU_FILL );
    #gluQuadricNormals(quadratic, GLU_SMOOTH)
    #gluQuadricTexture(quadratic, GL_TRUE)
    #glEnable(GL_TEXTURE_2D)    
    
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    
    
    # Add light
    light_ambient =  [0.0, 0.0, 0.0, 1.0]
    light_diffuse =  [1.0, 1.0, 1.0, 1.0]
    light_specular =  [1.0, 1.0, 1.0, 1.0]
    light_position =  [1.0, 1.0, 1.0, 0.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
   
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

def draw():
    global xrot, yrot, zrot, quadratic

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);    
    glLoadIdentity();                    
    glTranslatef(0.0,0.0,-5.0)

    glRotatef(xrot,1.0,0.0,0.0)            # Rotate The Cube On It's X Axis
    glRotatef(yrot,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis
    glRotatef(zrot,0.0,0.0,1.0)            # Rotate The Cube On It's Z Axis           
    gluSphere(quadratic,1.3,32,32)
    
           
    xrot  = xrot + 0.2                # X rotation
    yrot = yrot + 0.2                 # Y rotation
    zrot = zrot + 0.2                 # Z rotation      
    

def main():

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode((640,480), video_flags)

    resize((640,480))
    init()
    
    
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

