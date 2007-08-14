from Kamaelia.File.Writing import SimpleFileWriter
import os
import Kamaelia.Protocol.IRC.IRCClient
import time

"""
===================================
Supporting Functions for IRC Logger
===================================
BasicLogger and Logger depend heavily on this library. These functions are in a
separate module from the Logger components so we can reload these functions
without stopping Logger

There are no components in this module. 
"""

def respondToQueries(self, msg):
    """Takes a BasicLogger as its first argument. If this function recognizes
    "msg" as a command, then it sends back the appropriate response to IRC
    """
    replyLines = ""
    tag = 'PRIVMSG'

    if msg[0] == 'PRIVMSG' and msg[3].split(':')[0] == self.name:
        words = msg[3].split()
        if words[1] == 'logfile':
            replyLines = [self.logname]
        elif words[1] == 'infofile':
            replyLines = [self.infoname]
        elif words[1] == 'help':
            replyLines = ["Name: %s   Channel: %s" % (self.name, self.channel),
                          "I do a simple job -- recording all channel traffic.",
                          "Lines prefixed by [off] won't get recorded",
                          "I respond to the following: 'logfile', 'infofile', 'help', 'date', 'time', 'dance', 'poke', 'slap', 'ecky', 'boo', and 'reload {modulename}'."
                          ]
        elif words[1] == 'date':
            replyLines = [self.currentDateString()]
        elif words[1] == 'time':
            replyLines = [self.currentTimeString()]
        elif words[1] == 'dance':
            tag = 'ME'
            replyLines = ['does the macarena']
        elif words[1] == 'poke':
            replyLines = ['Not the eye! Not the eye!']
        elif words[1] == 'slap':
            replyLines = ['Ouch!']
        elif words[1] == 'ecky':
            replyLines = ['Ptang!']
        elif words[1] == 'boo':
            replyLines = ['Nice try, but that didn\'t scare me']
        
    if replyLines:
        for reply in replyLines:
            self.send((tag, self.channel, reply), "irc")
            self.send(self.format("Reply: %s \n" % reply), "outbox")


def TimedOutformat(data):
    """\
    prepends a timestamp onto formatted data and ignores all privmsgs prefixed
    by "[off]"
    """
    if data[0] == 'PRIVMSG' and data[3][0:5] == '[off]':
        return
    if type(data) == type(""):
        formatted = data
    else:
        formatted = Kamaelia.Protocol.IRC.IRCClient.outformat(data)
    curtime = time.gmtime()
    timestamp = time.strftime("[%H:%M] ", curtime)
    if formatted: return timestamp+formatted

def HTMLOutformat(data):
    """each formatted line becomes a line on a table."""
    head = "            <tr><td>"
    end = "</td></tr>\n"    
    formatted = TimedOutformat(data)
    if formatted:
        formatted = formatted.replace('<', '&lt ')
        formatted = formatted.replace('>', '&gt')
        return head + formatted.rstrip() + end

def AppendingFileWriter(filename):
    """appends to instead of overwrites logs"""
    return SimpleFileWriter(filename, mode='ab')

def LoggerWriter(filename):
    """
    puts an html header in front of every file it opens. Does not make well-
    formed HTML, as files are closed without closing the HTML tags. However,
    most browsers don't have a problem with this. =D
    """
    htmlhead = "<html><body><table>\n"
    if not os.path.exists(filename):
        f = open(filename, "wb")
        f.write(htmlhead)
        f.close()
    return SimpleFileWriter(filename, mode='ab')

def currentDateString():
    """returns the current date in YYYY-MM-DD format"""
    curtime = time.gmtime()
    return time.strftime("%Y-%m-%d", curtime)


def currentTimeString():
    """returns the current time in hour:minute:second format"""
    curtime = time.gmtime()
    return time.strftime("%H:%M:%S", curtime)

def getFilenames(logdir, channel):
    """returns tuple (logname, infoname) according to the parameters given"""
    name = logdir + channel.lstrip('#') + currentDateString()
    return name + "_log.html", name + "_info.html"

outformat = HTMLOutformat    
    
