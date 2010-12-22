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

__kamaelia_components__ = ()

try:
    from Kamaelia.UI.Pygame.Display import PygameDisplay as PygameDisplay
    have_pygame = True
#    __kamaelia_components__ = __kamaelia_components__ + ( PygameDisplay, )
except ImportError:
    have_pygame = False

#
# This will fail for the moment
#
try:
    from Kamaelia.UI.OpenGL.Display import OpenGLDisplay as OpenGLDisplay
    have_opengl = True
#    __kamaelia_components__ = __kamaelia_components__ + ( OpenGLDisplay, )
except ImportError:
    have_opengl = False

#
# TODO: allow update of the display manager service.
#

