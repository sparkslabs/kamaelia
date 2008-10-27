from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent

from base import S3Component, S3Completion, S3Exception, BUCKET_SEP
from base import S3KeyHandler, S3UploadRequest, UploadDownloadMixin

import os.path

__all__ = ["S3KeyFetcher", "S3FilePathUploader", "S3KeyDeleter", "S3KeyToFile"]

class S3KeyFetcher(S3Component, component):
    """Fetches :class:`boto.s3.key.Key` objects"""
    
    Inboxes = { "inbox"   : "Path of key to fetch",
                "control" : "Control",
              }
    Outboxes = { "outbox" : "boto.s3.key.Key",
                 "signal" : "NOT USED",
                 "log"    : "Log messages from here",
               }
    
    def main(self):
        while not self.shutdown():
            for path in self.Inbox():
                self.debug("Requesting path %s" % path)
                try:
                    key = self.get_key(path)
                except Exception, e:
                    self.error("Error getting key %s: %s" % (path, e))
                else:
                    if key is None:
                        self.error("Couldn't find key %s" % path)
                        continue
                    self.send(key, "outbox")
                    self.info("Got key %s" % key)
            yield 1
                    
    def get_key(self, path):
        """Fetch Keys from an S3 bucket
        
        :param path: Path of the key
        :type path: string
        """
        
        return self.bucket.get_key(path)


class S3FilePathUploader(S3Component, UploadDownloadMixin, threadedcomponent):
    """Uploads a local file to S3"""
    
    def main(self):
        while not self.shutdown():
            for upload_req in self.Inbox():
                if not isinstance(upload_req, S3UploadRequest):
                    self.error("%s is not an S3UploadRequest" % str(upload_req))
                    continue
                self.create_key(upload_req)
            #yield 1
                
    def create_key(self, upload_req, name=None):
        """Create a :class:`~boto.s3.key.Key` from this S3UploadRequest
        
        :param upload_req:
        :type upload_req: An instance of aws.s3.S3UploadRequest
        """
        
        if not name:
            name = os.path.split(upload_req.file_path)[-1]
        key = self.bucket.new_key(name)
        key.update_metadata(upload_req.metadata)
        try:
            key.set_contents_from_filename(upload_req.file_path,
                                           cb=self._update_progress(key))
        except Exception, e:
            self.error("Setting key from %s failed: %s" % \
                       (upload_req.file_path, e.replace('\n', ' ')))
        else:
            self.info("%sb sent to %s:%s" % (key.size, self.bucket_name, key.name))
            path = "%s%s%s" % (key.bucket.name, BUCKET_SEP, key.name)
            completion = S3Completion(path, key.metadata)
            self.send(completion.to_dict(), "outbox")


class S3KeyDeleter(S3KeyHandler, threadedcomponent):
    """Deletes :class:`~boto.s3.key.Key` objects recieved in inbox"""
    
    def process_key(self, key):
        """Delete a key
        
        :params key: The key to delete
        :type key: Instance of boto.s3.key.Key
        """
        try:
            key.delete()
        except Exception, e:
            self.error("Deleting key %s failed: %s" % \
                       (key.name, str(e).replace('\n', ' ')))
        else:
            self.info("Key %s deleted from %s" % (key.name, key.bucket.name))
            path = "%s%s%s" % (key.bucket.name, BUCKET_SEP, key.name)
            completion = S3Completion(path, key.metadata)
            self.send(completion.to_dict(), "outbox")

    
class S3KeyToFile(S3KeyHandler, threadedcomponent):
    """Downloads a file from S3 from :class:`~boto.s3.key.Key` objects in "inbox"
    
    Files downloaded are saved into :attr:`directory` which must exist. After
    the key is processed an :class:`S3Completion` is created and put into the
    outbox"""
    
    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise S3Exception("Directory %s doesn't exist" % directory)
        super(S3KeyToFile, self).__init__()
        self.dir = directory
    
    def process_key(self, key):
        """Create a file in self directory with contents of key
        
        :params key: The key to download
        :type key: Instance of boto.s3.key.Key
        """
        path = os.path.join(self.dir, key.name)
        try:
            self.info("Trying key: %s" % key.name)
            key.get_contents_to_filename(path,
                                         cb=self._update_progress(key))
        except Exception, e:
            self.error("Downloading from %s failed: %s" % \
                       (key.name, str(e).replace('\n', ' ')))
        else:
            self.info("%sb downloaded to %s" % (key.size, path))
            completion = S3Completion(path, key.metadata)
            self.send(completion.to_dict(), "outbox")

class S3KeyToText(S3KeyHandler, threadedcomponent):
    """Downloads text from S3 from :class:`~boto.s3.key.Key` objects in "inbox"
    
    After the key is retrieved the text is sent to "outbox"."""
    
    def process_key(self, key):
        """Extract the key's text and send it to "outbox"
        
        :params key: The key to extract text from
        :type key: Instance of boto.s3.key.Key
        """
        if not key.content_type == 'text/plain':
            self.error("Key %s has content_type %s" % \
                       (key.name, key.content_type))
            return
        try:
            self.info("Trying key: %s" % key.name)
            message = (key.metadata,
                       key.get_contents_as_string(cb=self._update_progress(key))
                      )
            self.send(message, "outbox")
        except Exception, e:
            self.error("Downloading from %s failed: %s" % \
                       (key.name, str(e).replace('\n', ' ')))
        else:
            self.info('Text retrieved from "%s"' % key.name)