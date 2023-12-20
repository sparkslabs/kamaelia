#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
====================
Pygame Button Widget
====================

A button widget for pygame display surfaces. Sends a message when clicked.

Uses the Pygame Display service.



Example Usage
-------------
Three buttons that output messages to the console::
    
    button1 = Button(caption="Press SPACE or click",key=K_SPACE).activate()
    button2 = Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0)).activate()
    button3 = Button(caption="Mary...",msg="Mary had a little lamb", position=(200,100)).activate()
    
    ce = ConsoleEchoer().activate()
    button1.link( (button1,"outbox"), (ce,"inbox") )
    button2.link( (button2,"outbox"), (ce,"inbox") )
    button3.link( (button3,"outbox"), (ce,"inbox") )
    


How does it work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the surface of the button. It also binds event
listeners to the service, as appropriate.

Arguments to the constructor configure the appearance and behaviour of the
button component:

- If an output "msg" is not specified, the default is a tuple ("CLICK", id) where
  id is the self.id attribute of the component.

- A pygame keycode can be specified that will also trigger the button as if it
  had been clicked

- you can set the text label, colour, margin size and position of the button

- the button can have a transparent background

- you can specify a size as width,height. If specified, the margin size is
  ignored and the text label will be centred within the button

If a producerFinished or shutdownMicroprocess message is received on its
"control" inbox. It is passed on out of its "signal" outbox and the component
terminates.

Upon termination, this component does *not* unbind itself from the Pygame Display
service. It does not deregister event handlers and does not relinquish the
display surface it requested.
"""

import pygame

from Kamaelia.UI.Pygame.Button import Button



class ImageButton( Button ):
    def __init__(self, caption=None, position=None, margin=8, bgcolour = (224,224,224), fgcolour = (0,0,0), msg=None,
                key = None,
                transparent = False, size=None):
        super(ImageButton,self).__init__(caption, position, margin, bgcolour, fgcolour, msg, key, transparent, size)
        
    def buildCaption(self, text):
       """Pre-render the image to go on the button label."""
       #TODO: render an image to the button instead of the caption
       self.image = pygame.image.load(text)
      
       (w,h) = self.image.get_size()
       if not self.size:
           self.size = (w + 2*self.margin, h + 2*self.margin)
           self.imagePosition = (self.margin, self.margin)
       else:
           self.imagePosition = ( (self.size[0]-w)/2, (self.size[1]-h)/2 )

__kamaelia_components__  = ( ImageButton, )


if __name__ == "__main__":

    from Kamaelia.Chassis.PAR import PAR
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
   
    import os
    Pipeline(
        PAR(
            ImageButton(caption='../../../Examples/SupportingMediaFiles/cat-logo.png',key=pygame.K_SPACE,msg="cat"),
            Button(caption="Press SPACE or click",key=pygame.K_SPACE, msg="space"),
            Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0), msg="reverse"),
            Button(caption="Mary...",msg="Mary had a little lamb", position=(200,100)),
        ),
        ConsoleEchoer(),
    ).run()
