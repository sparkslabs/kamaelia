from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Scheduler import scheduler
from Axon.Ipc import shutdownMicroprocess, producerFinished

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline

from boto.sqs import Connection
from boto.sqs.jsonmessage import JSONMessage, JSONEncodingExeption

import time

from aws import DebugMethodMixin
from aws.logger import Logger
from aws.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, LOG_DIR, LOG_LEVEL

CONTINUE_MSG = "CONTINUE"


class Ticker(threadedcomponent):
    """A Component that sends out a message to wake up an asleep component"""
    
    def __init__(self, timeout=5):
        """Initialize the component with a timeout
        
        :param timeout: The time in second to wait for
        :type timeout: int
        """
        super(Ticker, self).__init__()
        self.timeout = timeout
        
    def __str__(self):
        return u"Ticker: %s secs" % self.timeout
        
    def main(self):
        while 1:
            time.sleep(self.timeout)
            self.send(CONTINUE_MSG, "signal")

      
class SQSJSONComponent(component, DebugMethodMixin):
    """Base functionality for components that interact with SQS"""
    
    def __init__(self, queue_name):
        """Initialize the Component
        
        Sets up a conection to SQS and a logger
        
        :param queue_name: The SQS queue to use
        :type queue_name: String
        :param timeout: Value to set the queue's timeout to
        :type timeout: Int
        """
        
        super(SQSJSONComponent, self).__init__()
        try:
            self.con = Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        except Exception, e:
            self.send(('error', e), "log")
            raise
        self.queue_name = queue_name
        self.init_queue()
        
        
    def __str__(self):
        return u"%s: (queue %s)" % (self.__class__.name, self.queue_name)
    
    def init_queue(self):
        self.debug("init_queue called")
        self.queue = self.con.get_queue(self.queue_name)
        if not self.queue:
            self.debug("Queue %s doesn't exist" % self.queue_name)
            return
        self.queue.message_class = JSONMessage

        
class SQSJSONReciever(SQSJSONComponent):
    """Gets JSON messages from an SQS queue"""
    
    Inboxes = { "inbox"   : "NOT USED",
                "control" : "Recieve wake up messages",
              }
    Outboxes = { "outbox" : "Python dicts fetched from a JSONMessage",
                 "signal" : "NOT USED",
                 "log"    : "Log messages from here",
               }
        
    def main(self):
        while 1:
            if self.dataReady('control'):
                control = self.recv('control')
                if control == CONTINUE_MSG:
                    self.debug("CONTINUE Recieved")
                    try:
                        #import pdb; pdb.set_trace()
                        rs = self.get_messages()
                    except JSONEncodingExeption, e:
                        self.error(e)
                        self.queue.delete_message(e.message)
                    else:
                        for msg in rs:
                            self.info(self.format_log_msg(msg))
                            self.send(msg.get_body())
                            try:
                                self.queue.delete_message(msg)
                            except:
                                self.error("Deleting message: %s - (id: %s) failed" % (msg, msg.id))
                if isinstance(control, shutdownMicroprocess) or \
                        isinstance(control, producerFinished):
                    self.send(producerFinished(), "signal")
                    break
            else:
                self.pause()
            yield 1
            
    def get_messages(self, number=1):
        """Fetch messages from an SQS queue
        
        :param number: The number of messages to get
        :type number: int between 1 and 10
        """
        
        if self.queue:
            return self.queue.get_messages(number)
        else:
            self.init_queue()
        return []
        
    def format_log_msg(self, msg):
        return "Recieved %s from %s" % (msg.get_body(), self.queue.id[1:])

class SQSJSONSender(SQSJSONComponent):
    """Sends JSON messages to an SQS queue"""
    
    Inboxes = { "inbox"   : "Python dict to send to the Queue",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "NOTUSED",
                 "failed"  : "Messages that failed to send go here",
                 "signal" : "NOT USED",
                 "log"    : "Log messages from here",
               }
        
    def main(self):
        while 1:
            for dct in self.Inbox("inbox"):
                self.send_message(dct)

            yield 1
            
    def format_log_msg(self, msg):
        return "Sent %s to %s" % (msg.get_body(), self.queue.id[1:])
            
    def send_message(self, dct):
        """Encode and send a dict to the queue
        
        :param dct: The information to be sent to the queue
        :type dct: A python dict
        """
        
        if self.queue:
            try:
                msg = self.queue.new_message(dct)
                self.queue.write(msg)
            except Exception, e:
                self.error("Exception sending message: %s" % e)
                self.send(dct, 'failed')
            else:
                self.info(self.format_log_msg(msg))
        else:
            self.init_queue()

def SQSRX(queue, timeout):
    return Graphline(
                    TICK = Ticker(timeout),
                    RX   = SQSJSONReciever(queue),
                    LOG  = Logger(queue + 'RX', LOG_LEVEL, '/tmp'),
                    linkages = {
                      ("TICK", "signal")  : ("RX", "control"),
                      ("RX", "log")       : ("LOG", "inbox"),
                      ("RX", "outbox")    : ("self", "outbox"),
                    }).activate()

if __name__ == '__main__':

    
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Util.Introspector import Introspector
        
    Pipeline(Introspector(), TCPClient("127.0.0.1",1501) ).activate()
    
    
    
    SQSRX('testing', 5).run()


