#! /usr/bin/env python
##
## (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
## You may only modify and redistribute this under the terms of any of the
## following licenses(2): Mozilla Public License, V1.1, GNU General
## Public License, V2.0, GNU Lesser General Public License, V2.1
##
## (1) Kamaelia Contributors are listed in the AUTHORS file and at
##     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
##     not this notice.
## (2) Reproduced in the COPYING file, and at:
##     http://kamaelia.sourceforge.net/COPYING
## Under section 3.5 of the MPL, we are using this text since we deem the MPL
## notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
## notice is prohibited.
##
## Please contact us via: kamaelia-list-owner@lists.sourceforge.net
## to discuss alternative licensing.
## -------------------------------------------------------------------------

"""
=========================
Kamaelia IRC Support Code
=========================
This provides support for Kamaelia.Protocol.IRC.*

Specifically it provides 2 core functions and 2 utility methods.

Core functions
--------------

informat(text,defaultChannel='#kamtest')
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Summary - Puts a string input into tuple format for IRC_Client. Understands
irc commands preceded by a slash ("/"). All other text is formatted such
that sending it would send the message to the default channel.

Detail - If the text starts with a "/" it is treated as a command. Informat
understands some specific commands which it helps you format for sending to
the IRCClient. The commands it understands are::
       QUIT
       PRIVMSG
       MSG
       NOTICE
       KILL
       TOPIC
       SQUERY
       KICK
       USER
       ME

For commands it doesn't recognise, it makes a guess at how to forward it.

If you send it text which does NOT start with "/", it is assumed to be badly
formatted text, intended to be sent to the current default channel. It is
then formatted appropriately for sending on to an IRC_Client component.

For an example of usage, see Examples/TCP_Systems/IRC/BasicDemo.py

outformat(data, defaultChannel='#kamtest')
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Takes tuple output from IRC_Client and formats for easier reading  If a
plaintext is received, outformat treats it as a privmsg intended for
defaultChannel (default "#kamtest").

Specific commands it understands and will make a an attempt to format
appropriately are::
        PRIVMSG
        JOIN
        PART
        NICK
        ACTION
        TOPIC
        QUIT
        MODE

It will also identify certain types of errors.

For an example of usage, see Examples/TCP_Systems/IRC/BasicDemo.py

Utility functions
-----------------

channelOutformat(channel)
^^^^^^^^^^^^^^^^^^^^^^^^^
Creates a customised outformat function with defaultChannel predefined to
channel. (ie Returns a lambda)


channelInformat(channel)
^^^^^^^^^^^^^^^^^^^^^^^^
Creates a customised informat function with defaultChannel predefined to
channel. (ie Returns a lambda)

Open Issues
-----------
Should these really be components rather than helper functions?

"""

import string


def informat(text,defaultChannel='#kamtest'):
    """\
    Puts a string input into tuple format for IRC_Client.
    Understands irc commands preceded by a slash ("/")
    """
    if text[0] != '/' or text.split()[0] == '/': #in case we were passed "/ word words", or simply "/"
        return ('PRIVMSG', defaultChannel, text)
    words = text.split()
    tag = words[0]
    tag = tag.lstrip('/').upper()
    if tag == 'MSG':
        tag = 'PRIVMSG'
    try:
        if tag == 'QUIT' and len(words) >= 2:
            return (tag, string.join(words[1:]))
        elif tag in ('PRIVMSG', 'MSG', 'NOTICE', 'KILL', 'TOPIC', 'SQUERY') and len(words) >= 3:
            return (tag, words[1], string.join(words[2:]))
        elif tag == 'KICK' and len(words) >= 4:
            return (tag, words[1], words[2], string.join(words[3:]))
        elif tag == 'USER':
            return (tag, words[1], words[2], words[3], string.join(words[4:]))
        elif tag == 'ME' and len(words) >= 2:
            return (tag, defaultChannel, string.join(words[1:]))
        else: 
            words[0] = tag
            if tag: #only false if we were passed "/" as text
                return words
    except IndexError:
        words[0] = tag
        return words


def outformat(data, defaultChannel='#kamtest'):
    """\
    Takes tuple output from IRC_Client and formats for easier reading.
    If a plaintext is received, outformat treats it as a privmsg intended for
    defaultChannel (default "#kamtest").
    """
    msgtype, sender, recipient, body = data
    end = '\n'
    if msgtype == 'PRIVMSG':
        text = '<%s> %s' % (sender, body)
    elif msgtype == 'JOIN' :
        text = '*** %s has joined %s' % (sender, recipient)
    elif msgtype == 'PART' :
        text = '*** %s has parted %s' % (sender, recipient)
    elif msgtype == 'NICK':
        text = '*** %s is now known as %s' % (sender, body)
    elif msgtype == 'ACTION':
        text = '*** %s %s' % (sender, body)
    elif msgtype == 'TOPIC':
        text = '*** %s changed the topic to %s' % (sender, body)
    elif msgtype == 'QUIT': #test this, channel to outbox, not system
        text = '*** %s has quit IRC' % (sender)
    elif msgtype == 'MODE' and recipient == defaultChannel:
        text = '*** %s has set channel mode: %s' % (sender, body) 
    elif msgtype > '000' and msgtype < '400':
        text = 'Reply %s from %s to %s: %s' % data
    elif msgtype >= '400' and msgtype < '600':
        text = 'Error! %s %s %s %s' % data
    elif msgtype >= '600' and msgtype < '1000':
        text = 'Unknown numeric reply: %s %s %s %s' % data
    else:
        text = '%s from %s: %s' % (msgtype, sender, body)
    return text + end

def channelOutformat(channel): # FIXME: Probably ought to be a nested "def" instead
    """returns outformat with the specified channel as the default channel"""
    return (lambda data: outformat(data, defaultChannel=channel))

def channelInformat(channel): # FIXME: Probably ought to be a nested "def" instead
    """returns informat with the specified channel as the default channel"""
    return (lambda text: informat(text, defaultChannel=channel))

if __name__ == '__main__':
    print "This file currently has no example/integral test code"

