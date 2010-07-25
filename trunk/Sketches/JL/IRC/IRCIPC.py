# -*- coding: utf-8 -*-
# IRC IPC messages
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class IRCIPC(object):
    "explanation %(foo)s did %(bar)s"
    Parameters = [] # ["foo", "bar"]
    def __init__(self, *args):
        super(IRCIPC, self).__init__()
        
        for param in self.Parameters:
            optional = False
            if param[:1] == "?":
                param = param[1:]
                optional = True
                
            if not kwds.has_key(param):
                if not optional:
                    raise ValueError(param + " not given as a parameter to " + str(self.__class__.__name__))
                else:
                    self.__dict__[param] = None
            else:
                self.__dict__[param] = kwds[param]
                del kwds[param]

        for additional in kwds.keys():
            raise ValueError("Unknown parameter " + additional + " to " + str(self.__class__.__name__))
            
        self.__dict__.update(kwds)

    def getText(self):
        return self.__class__.__doc__ % self.__dict__

# ====================== Messages to send to IRCClient =======================
class IRCIPCChangeNick(IRCIPC):
    "Change display name to %(nick)s"
    Parameters = ["nick"]
    #  nick - new nickname to assume

class IRCIPCDisconnect(IRCIPC):
    "Disconnect from the IRC server"
    Parameters = []
    
class IRCIPCConnect(IRCIPC):
    "Connect to the IRC server"
    Parameters = []

class IRCIPCLogin(IRCIPC):
    "Login to the IRC server"
    Parameters = ["nick", "username"]
    Optional = ["password"]
    
class IRCIPCJoinChannel(IRCIPC):
    "Join the chat channel %(channel)s"
    Parameters = ["channel"]
    #  channel - the name of the channel, e.g. "#kamaelia"

class IRCIPCLeaveChannel(IRCIPC):
    "Leave the chat channel %(channel)s"
    Parameters = ["channel"]
    #  channel - the name of the channel, e.g. "#kamaelia"
    
class IRCIPCSendMessage(IRCIPC):
    "Send the message \"%(msg)s\" to %(recipient)s"
    Parameters = ["recipient", "msg"]
    #  recipient - who/where to send the message to
    #  msg - the message to send
    
class IRCIPCSetChannelTopic(IRCIPC):
    "Set the topic on %(channel)s to \"%(topic)s\""
    Parameters = ["channel", "topic"]
    #  channel - the channel for which you want to set the topic 
    #  topic - the new topic
    
# ======================== Messages sent by IRCClient ========================
class IRCIPCDisconnected(IRCIPC):
    "We were disconnected from the IRC server"
    Parameters = []
    
class IRCIPCUserNickChange(IRCIPC):
    "We were disconnected from the IRC server"
    Parameters = []
    
class IRCIPCMessageReceived(IRCIPC):
    "We were disconnected from the IRC server"
    Parameters = ["sender", "recipient", "msg"]
