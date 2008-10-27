from boto.s3 import Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError

from aws import DebugMethodMixin
from aws.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY

import os.path

BUCKET_SEP = "-:-"


class S3Exception(Exception):
    """Raised if there's a problem creating an UploadRequest"""
    

class S3UploadRequest(object):
    """Creates a :class:`~boto.s3.key.Key` with the given metadata"""
    
    def __init__(self, file_path, metadata={}):
        if not os.path.isfile(file_path):
            raise S3Exception("File %s doesn't exist" % file_path)
        self.file_path = file_path
        self.metadata = metadata
        
    def __str__(self):
        return "%s, meta: %s" % (os.path.split(self.file_path)[-1],
                                 self.metadata)


class S3Completion(object):
    """A notification of a completed job"""
    
    def __init__(self, path, metadata):
        self.path = path
        self.metadata = metadata
        
    def __str__(self):
        return "%s, meta: %s" % (self.path,
                                 self.metadata)
    
    @property
    def s3(self):
        path.find(BUCKET_SEP)
    
    def to_dict(self):
        """Return a dict suitable for json encoding"""
        return dict(self.metadata.items() + [('path',self.path)])


class S3Component(DebugMethodMixin):
    """Base class for S3. Takes care of the connection to a bucket"""
    
    def __init__(self, bucket_name):
        super(S3Component, self).__init__()
        self.bucket_name = bucket_name
        try:
            self.con = Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        except Exception, e:
            self.send(('error', e), "log")
            raise
        self.init_bucket()
        
    def __str__(self):
        return u"%s: (bucket %s)" % (self.__class__.name, self.bucket_name)
    
    def init_bucket(self):
        """Sets up the bucket, logging errors for a 403 or 404 response"""
        
        self.debug("init_bucket called")
        try:
            self.bucket = self.con.get_bucket(self.bucket_name)
        except S3ResponseError, e:
            msg = "get_bucket for '%s' returned %s" % \
                                                (self.bucket_name, e.status)
            if e.status in [403, 404]:
                self.debug(msg)
            else:
                self.error(msg)
                raise


class UploadDownloadMixin(object):
    """Mixin with update progress functionality
    
    .. warning:: A component subclassing from this must have a "prog" outbox
    """
    
    Inboxes = { "inbox"   : "boto.s3.key.Key objects",
                "control" : "Control",
              }
    
    Outboxes = { "outbox" : "Completion Notifications",
                 "signal" : "Signals",
                 "prog"   : "Download progress",
                 "log"    : "Log messages from here",
               }
    
    def _update_progress(self, key):
        """Callback for S3 methods that update progress"""
        
        def callback(done, total):
            self.send((key.bucket.name, key.name, done, total), "prog")
        return callback

    
class S3KeyHandler(UploadDownloadMixin, DebugMethodMixin):
    """Base class for functionality dealing with :class:`~boto.s3.key.Key` objects in "inbox"
    
    .. warning:: You must subclass this and define :meth:`process_key` and it only works as a :class:`~Axon.ThreadedComponent.threadedcomponent`"""
        
    def main(self):
        while not self.shutdown():
            for key in self.Inbox():
                if not isinstance(key, Key):
                    self.error("%s is not a Key" % str(key))
                    continue
                self.process_key(key)
    
    def process_key(self, key):
        """Process :class:`~boto.s3.key.Key` instances recieved on inbox
        
        :raises NotImplementedError: Must be subclassed
        """
        raise NotImplementedError

