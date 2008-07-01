from Kamaelia.File.ConfigFile import FormatterBase, ParseConfigFile, DictFormatter, ParseException
from Axon.Ipc import producerFinished, shutdownMicroprocess

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
            if key.find('.') == -1: #only prepend kp. if there isn't already a dot
                ret_val['kp.' + key] = value
            else:
                ret_val[key] = value
        return ret_val
    
def ParseUrlFile(location):
    return ParseConfigFile(location, [DictFormatter(), UrlListFormatter()])
