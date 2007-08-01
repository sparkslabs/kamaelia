# IRC IPC messages

class IRCIPC(object):
    "explanation %(foo)s did %(bar)s"
    Parameters = [] # ["foo", "bar"]
    def __init__(self, **kwds):
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
    Parameters = ["nick", "?password", "?username"]
    
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
