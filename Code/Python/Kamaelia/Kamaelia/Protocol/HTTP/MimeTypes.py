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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
Mapping of common file extensions to their associated MIME types.
"""

import string

extensionToMimeType = {
    "png"  : "image/png",
    "gif"  : "image/gif",
    "jpg"  : "image/jpeg",
    "jpeg" : "image/jpeg",
    "bmp"  : "image/bmp",
    "tif"  : "image/tiff",
    "tiff" : "image/tiff",
    "ico"  : "image/x-icon",

    "c"    : "text/plain",
    "py"   : "text/plain",
    "cpp"  : "text/plain",
    "cc"   : "text/plain",
    "h"    : "text/plain",
    "hpp"  : "text/plain",


    "txt"  : "text/plain",
    "htm"  : "text/html",
    "html" : "text/html",
    "css"  : "text/css",

    "zip"  : "application/zip",
    "gz"   : "application/x-gzip",
    "tar"  : "application/x-tar",

    "mid"  : "audio/mid",
    "mp3"  : "audio/mpeg",
    "wav"  : "audio/x-wav",


    "cool" : "text/cool" # our own made up MIME type
}

def workoutMimeType(filename):
    "Determine the MIME type of a file from its file extension"
    fileextension = string.rsplit(filename, ".", 1)[-1]
    if (fileextension in extensionToMimeType):
        return extensionToMimeType[fileextension]
    else:
        return "application/octet-stream"
