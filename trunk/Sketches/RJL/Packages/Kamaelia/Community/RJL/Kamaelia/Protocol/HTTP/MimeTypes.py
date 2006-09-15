#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
    if extensionToMimeType.has_key(fileextension):
        return extensionToMimeType[fileextension]
    else:
        return "application/octet-stream"
