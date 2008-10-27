# -*- coding: utf-8 -*-

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import logging
from logging.handlers import RotatingFileHandler

import os.path
    

class Logger(component):
    """Logs anything recieved on inbox at the level specified
    
    Everything at self.level is logged into one file (which is rotated and
    error is also logged to a separate file. The two log files will be called
    <log_name>_main.log and <log_name>_error.log and will both live in log_dir.
    
    :param log_name: What to call the first part of the log file
    :type log_name: string
    :param log_dir: Directory to write the log files into
    :type log_dir: string
    :param level: The logging level one of DEBUG, ERROR, INFO
    :type level: Uppercase string
    """
    
    Inboxes = {"inbox" : "Tuple ([debug | info | error], 'String to be logged')",
               "control" : "Closes the logger",}
    Outboxes = {"outbox" : "UNUSED",
                "signal" : "UNUSED",}
   
    def __init__(self, log_name, level, log_dir, size=50000):
        super(Logger, self).__init__()
        
        self.log_name = log_name
        self.log_dir = log_dir
        self.size = size
        self.level = getattr(logging, level)

    def main(self):
        self.setup_loggers()

        while 1:
            if self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or \
                        isinstance(mes, producerFinished):
                    self.logger.close()
                    self.send(producerFinished(), "signal")
                    break

            for level, msg in self.Inbox("inbox"):
                # TODO: need better error handling here to be reusable
                assert level in ['info', 'debug', 'error'],\
                                    "log level not allowed: %s" % level
                getattr(self.logger, level)(msg)

            if not self.anyReady():
                self.pause()
  
            yield 1
    
    def setup_loggers(self):
        """Sets up the general catchall log and the separate error log
        
        The catchall log uses :class:`~logging.handlers.RotatingFileHandler`
        and the error log is just a flat file with a simpler format (for later
        processing).
        """
        
        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.level)
        
        # Main log format an handler
        main_format = "[%(asctime)s]\t%(levelname)-8s\t%(name)-12s\t%(message)s"
        main_logfmt = logging.Formatter(main_format)
        main_log = RotatingFileHandler(self.get_full_path('main'),
                                        maxBytes=self.size, 
                                        backupCount=10)
        main_log.setFormatter(main_logfmt)
        
        # Error log format and handler
        error_log = logging.FileHandler(self.get_full_path('error'))
        error_logfmt = logging.Formatter("[%(asctime)s]\t%(name)-12s\t%(message)s")
        error_log.setFormatter(error_logfmt)
        error_log.setLevel(logging.ERROR)
        
        # Set them both up
        logger.addHandler(main_log)
        logger.addHandler(error_log)
        self.logger = logger
        
    def get_full_path(self, log_part):
        """Get a full path to a log file
        
        Will be in the form: ``/{self.log_dir}/{self.log_name}_{log_part}.log``
        """
        
        filename = "%s_%s.log" % (self.log_name, log_part)
        return os.path.join(self.log_dir, filename)
        
if __name__ == '__main__':
    
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    class ConsoleEval(ConsoleReader):
        """eval's its raw_input to create tuples"""
        
        def main(self):
            """Main thread loop."""
            while 1:
               line = eval(raw_input(self.prompt))
               line = line
               print line
               self.send(line, "outbox")
    
    Pipeline(ConsoleEval(), Logger('test', "DEBUG", '/tmp/')).run()
    