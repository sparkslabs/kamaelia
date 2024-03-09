#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import Axon
from Axon.background import background
from Axon.Handle import Handle
from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
import time

bg = background(slowmo=0.01).start()

ticker1 = Handle(Pipeline(
                            Ticker(background_colour=(128,48,128),
                                   render_left = 1,
                                   render_top = 1,
                                   render_right = 600,
                                   render_bottom = 200,
                                   position = (100, 250),
                            )
                   )
          ).activate()
ticker2 = Handle(Pipeline( 
                            Ticker(background_colour=(128,48,128),
                                render_left = 1,
                                render_top = 1,
                                render_right = 600,
                                render_bottom = 200,
                                position = (100, 0),
                            )
                   )
          ).activate()

ticker3 = Handle(Pipeline( 
                            Ticker(background_colour=(128,48,128),
                                render_left = 1,
                                render_top = 1,
                                render_right = 600,
                                render_bottom = 200,
                                position = (100, 500),
                            )
                   )
          ).activate()

for line in open("Ulysses", 'r'):
    line = line.rstrip() # kill the newlines - printing them in reverse order messes with the ticker.
    ticker1.put(line[::-1], "inbox")
    ticker2.put(line, "inbox")

time.sleep(5)

for line in open("Ulysses", 'r+b'):
    ticker3.put(line, "inbox")

time.sleep(10)

# we'll unceremoniously die now, since the ticker has no way to indicate when it's done drawing, or indeed to cleanly remove it from the pygame window. Sending
# a producerfinished would end it, but it'd remain in pygame.


