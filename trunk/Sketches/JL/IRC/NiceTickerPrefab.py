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

from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Chassis.Pipeline import Pipeline

def NiceTickerPrefab(**other_ticker_args):
    """Ticker that displays black text on a white background, and transforms
    any non-string arguments passed to it into strings.
    Do not pass in keywords text_height, line_spacing, background_colour,
    outline_colour, or text_colour."""
    return Pipeline(PureTransformer(lambda x: str(x)),
             Ticker(text_height=16, line_spacing=2,
                    background_colour=(255, 255, 245), text_colour=(10,10,10),
                    outline_colour = (0,0,0),
                    **other_ticker_args)
             )
