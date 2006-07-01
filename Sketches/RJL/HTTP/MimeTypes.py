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
    fileextension = string.rsplit(filename,".",1)[-1]
    if extensionToMimeType.has_key(fileextension):
        return extensionToMimeType[fileextension]
    else:
        return "application/octet-stream"
