from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Util.SequentialTransformer import SequentialTransformer

from aws.logger import Logger
from aws.s3 import S3KeyFetcher, S3FilePathUploader, S3KeyToFile, S3KeyDeleter
from aws.s3.base import S3UploadRequest
from aws.sqs import SQSRX, SQSJSONSender

from aws import settings

import os
import os.path

QUEUE_2_BUCKET = {
    "DOC_Q"   : "2degrees-raw-documents",
    "INDEX_Q" : "2degrees-text-documents",
    "testing" : "2deg-test",
}

DOC_Q = "DOC_Q"
INDEX_Q = "INDEX_Q"


def Keyfetcher(queue, log_dir):
    """Monitors queue and fetches :class:`~boto.s3.key.Key` objects from it
    
    :param queue: The name of the queue to monitor
    :type queue: string
    :param log_dir: Directory to log to
    :type log_dir: string
    """
    LOG = "KeyFetcherLog"
    bucket_name = QUEUE_2_BUCKET[queue]
    Backplane(LOG).activate()
    log_sub = Pipeline(SubscribeTo(LOG), Logger('Keyfetcher',
                                                settings.LOG_LEVEL,
                                                '/tmp/')).activate()
    return Graphline(RX     = SQSRX(queue, 5),
                     PG     = SequentialTransformer(lambda dct: dct.get('path')),
                     KF     = S3KeyFetcher(bucket_name),
                     KFLOG  = PublishTo(LOG),
                        linkages = {
                            ("self", "inbox") : ("RX", "inbox"),
                            ("RX", "outbox")  : ("PG", "inbox"),
                            ("PG", "outbox")  : ("KF", "inbox"),
                            ("KF", "log")     : ("KFLOG", "inbox"),
                            ("KF", "outbox")  : ("self", "outbox"),
                        }).activate()
    
def KeyActor(log_dir, log_name, actor, *actor_args, **actor_kwargs):
    """Component factory that acts upon :class:`~boto.s3.key.Key` objects
    
    :param log_dir: Directory to log to
    :type log_dir: string
    :param log_name: Name for the log file
    :type log_name: string
    :param actor: Class for processing Keys
    :type actor: Class - probably subclass of aws.KeyHandler
    :arg actor_args: Arguements to initialize actor
    :type actor_args: list of args or None or []
    :arg actor_kwargs: Any keyword arguements to initialize actor
    :type actor_kwargs: keyword args
    :rtype: An activated component
    """
    #import pdb; pdb.set_trace()
    LOG_LEVEL = settings.LOG_LEVEL
    key_processor = actor(*actor_args, **actor_kwargs)
    Backplane(log_name).activate()
    log_sub = Pipeline(SubscribeTo(log_name),
                       Logger(log_name, LOG_LEVEL, log_dir)).activate()
    
    return Graphline(PROC = key_processor,
                     LOG  = PublishTo(log_name),
                     COMP = ConsoleEchoer(),
                        linkages = {
                           ("self", "inbox") : ("PROC", "inbox"),
                           ("PROC", "log")    : ("LOG", "inbox"),
                           ("PROC", "prog") : ("COMP", "inbox"),
                        }).activate()
    
def Filedownloader(file_dir, log_dir):
    
    """Downloads files into file_dir
    
    recieves :class:`~boto.s3.key.Key` objects on inbox and downloads their
    contents to file_dir
    
    :param file_dir: Directory to download files to
    :type file_dir: string
    :param log_dir: Directory to log to
    :type log_dir: string
    """
    return KeyActor(log_dir, "FileDownload", S3KeyToFile, *(file_dir,))

def KeyDeleter(log_dir):
    
    """Downloads files into file_dir
    
    recieves :class:`~boto.s3.key.Key` objects on inbox and deletes them
    
    :param log_dir: Directory to log to
    :type log_dir: string
    """
    return KeyActor(log_dir, "KeyDelete", S3KeyDeleter)
    

#def Filedownloader(file_dir, log_dir):
#    
#    """Downloads files into file_dir
#    
#    recieves :class:`~boto.s3.key.Key` objects on inbox and downloads their
#    contents to file_dir
#    
#    :param file_dir: Directory to download files to
#    :type file_dir: string
#    :param log_dir: Directory to log to
#    :type log_dir: string
#    """
#    LOG = "FiledownloaderLog"
#    Backplane(LOG).activate()
#    log_sub = pipeline(SubscribeTo(LOG), Logger('Filedownloader', 'DEBUG', log_dir)).activate()
#    
#    return Graphline(K2F = S3KeyToFile(file_dir),
#                     LOG = PublishTo(LOG),
#                     COMP = ConsoleEchoer(),
#                        linkages = {
#                           ("self", "inbox") : ("K2F", "inbox"),
#                           ("K2F", "log")    : ("LOG", "inbox"),
#                           ("K2F", "prog") : ("COMP", "inbox"),
#                        }).activate()


def Fileuploader():
    uploader = Graphline(UL = S3FilePathUploader('2deg-test'),
                         LOG = Logger('testUL',
                                      settings.LOG_LEVEL,
                                      '/tmp'),
                         PROG = ConsoleEchoer(),
                         linkages = {
                              ("self", "inbox") : ("UL", "inbox"),
                              ("UL", "log")     : ("LOG", "inbox"),
                              ("UL", "outbox")  : ("PROG", "inbox"),
                            }).activate()
    
    return uploader
    
if __name__ == '__main__':
        
    Pipeline(Introspector(), TCPClient("127.0.0.1",1501) ).activate()
    
    path = '/home/ben/docs/vid/'
    
    def _avi_finder(path):
        gen = os.walk(path)
        for dir, _, fnames in gen:
            for f_name in fnames:
                full = os.path.join(dir, f_name)
                #print full
                if os.path.splitext(full)[1] == '.avi':
                    yield full
    
    #Pipeline(DataSource([S3UploadRequest(f) for f in _avi_finder(path)]),
    #         create_uploader()).run()
    #Pipeline(Keyfetcher('testing', '/tmp'),
    #         Filedownloader('/tmp/files', '/tmp')).run()
    Pipeline(Keyfetcher('testing','/tmp'), KeyDeleter('/tmp')).run()
