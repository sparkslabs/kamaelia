from Axon.Component import component
from Axon.Ipc import producerFinished
from ConfigParser import SafeConfigParser
from pprint import pprint
import os


##################################
#The config file reader
##################################
class ConfigFileReader(component):
    def __init__(self, filename, defaults=None, vars=None):
        super(ConfigFileReader, self).__init__()
        self.config_parser = SafeConfigParser(defaults)
        filename = os.path.expanduser(filename)
#        print 'filename = %s' % (filename)
        self.config_parser.read(filename)
        self.isections = iter(self.config_parser.sections())
        self.vars = None

    def main(self):
        while 1:
            try:
                section = self.isections.next()
#                print 'section ='
#                pprint(section)
            except StopIteration:
                break

            self.send((section, self.config_parser.items(section, vars=self.vars)))
            yield 1

        self.send(producerFinished(self), 'signal')

##################################
#The config file formatters
##################################

class FormatterBase(component):
    Inboxes = {'inbox' : 'used to receive input from the ConfigFileReader',
               'control' : 'used to receive producerFinished'}
    Outboxes = {'outbox' : 'Used to forward results piece by piece for formatter chaining',
                'signal' : 'used to send producerFinished'}

    def __init__(self, **argd):
        super(FormatterBase, self).__init__(argd)
        self.results = None
    def getResults(self):
        """
        This method is used to pull results once processing is finished.
        """
        return self.results

class DictFormatter(FormatterBase):
    def __init__(self):
        super(DictFormatter, self).__init__()
        self.results = {}

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                signal = self.recv('control')
                if isinstance(signal, producerFinished):
                    not_done = False

            while self.dataReady('inbox'):
                section, options = self.recv('inbox')
                self.results[section] = dict(options)
                self.send((section, dict(options)))

            if not self.anyReady() and not_done:
                self.pause()

            yield 1

        self.send(producerFinished(self), 'signal')

class UrlListFormatter(FormatterBase):
    """
    This component expects to be linked to a DictFormatter
    """
    def __init__(self):
        super(UrlListFormatter, self).__init__()
        self.results = []
        self.error_404 = None

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                signal = self.recv('control')
                if isinstance(signal, producerFinished):
                    not_done = False

            while self.dataReady('inbox'):
                section, data = self.recv('inbox')
                if section == 'error_404':
                    if data.has_key('regex'):
                        raise ParseException('error_404 cannot contain a regex')
                    data['regex'] = '.*'
                    self.error_404 = self.normalizeDict(data)
                else:
                    self.results.append(self.normalizeDict(data))
            if not self.anyReady() and not_done:
                self.pause()

            yield 1
        if not self.error_404:
            raise ParseException('Urls list must contain an error_404 item!')
        self.results.reverse()
        self.results.append(self.error_404)

    def normalizeDict(self, dic):
        ret_val = {}
        for key, value in dic.iteritems():
            ret_val['kp.' + key] = value
        return ret_val

##################################
#Support functions
##################################

def ParseConfigFile(filename, formatters, defaults=None, vars=None):
    if isinstance(formatters, FormatterBase):
        Pipeline(
            ConfigFileReader(filename),
            formatters
        ).run()
        return formatters.getResults()
    else:
        try:
            components = [ConfigFileReader(filename)] + formatters
        except TypeError:
            raise ParseException('formatters must be a list')
        [x.activate() for x in formatters]
        RecursiveLink(iter(components)).run()
    return formatters[-1].getResults()

def RecursiveLink(iterable, current=None):
    """
    This will link up components just as a pipeline does but in a recursive
    fashion and over an iterator.  You should always leave out current when
    calling this function.

    This function will return the first component in the iterable
    """
    if current is None:
        try:
            comp1 = iterable.next()
            comp2 = iterable.next()
        except StopIteration:
            return comp1
    else:
        try:
            comp1 = current
            comp2 = iterable.next()
        except StopIteration:
            return comp1

    comp1.link((comp1, 'outbox'), (comp2, 'inbox'))
    comp1.link((comp1, 'signal'), (comp2, 'control'))

    RecursiveLink(iterable, comp2)
    return comp1
##################################
#Exceptions
##################################

class ParseException(Exception):
    pass


##################################
#Example
##################################
if __name__ == '__main__':
    from pprint import pprint
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = '~/urls'

    pprint(ParseConfigFile(filename, [DictFormatter(), UrlListFormatter()]))
