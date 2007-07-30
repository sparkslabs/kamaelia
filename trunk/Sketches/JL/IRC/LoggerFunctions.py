def respondToQueries(self, msg):
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
                          "I respond to the following: 'logfile', 'infofile', 'help', 'date', 'time', 'dance', 'poke', 'slap', 'ecky', and 'reload {modulename}'."
                          ]
        elif words[1] == 'date':
            replyLines = [self.currentDateString()]
        elif words[1] == 'time':
            replyLines = [self.currentTimeString()]
        elif words[1] == 'dance':
            tag = 'ME'
            replyLines = ['does the macarena']
        elif words[1] == 'poke':
            replyLines = ['Hehe! That tickles!']
        elif words[1] == 'slap':
            replyLines = ['Ouch!']
        elif words[1] == 'ecky':
            replyLines = ['Ptang!']
        
    if replyLines:
        for reply in replyLines:
            self.send((tag, self.channel, reply), "irc")
            self.send("Reply: %s \n" % reply, "outbox")
