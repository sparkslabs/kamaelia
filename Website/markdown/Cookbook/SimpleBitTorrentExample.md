---
pagename: Cookbook/SimpleBitTorrentExample
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
\

A Simple BitTorrent Helper 
==========================

This cookbook is based on a small tool that I built to solve a problem I
had that required the use of BitTorrent. I wanted a script that would do
the following:

-   \'Publish\' files to a BitTorrent network when given a file name\
-   Download files from the network when given a \*.torrent file name
-   Accept all input from stdin
-   Send meaningful messages to stdout that could be parsed by another
    tool

The idea was to use this from another Python program and to communicate
via pipes (hence the need for IO to happen via stdin and stdout. Using
components found in the Kamaelia MegaBundle along with a couple of small
modifications, a reliable and robust tool was put together in very
little time and very few lines of code. The network needed is as
follows:

![BitTorrent Helper !graph](/images/ktorrent_network_cookbook.png){style=width:100%}

Let\'s consider each component in turn.


reader and parser 
-----------------

This pair takes in commands from the parent program. It reads from the
console, so we use the ready made Kamaelia **ConsoleReader** to get the
input and pass it to the **InstructionParser**.\

The **InstructionParser** will take a kind of URI and, based on what it
is given, put it in one of three outboxes:

-   \"outbox\" if the URI starts \'*file:*\' - a torrent must be made of
    this file and then seeding must commence
-   \"retrieveHtml\" if the URI starts \'*torrent:http:* - a torrent
    file must be retrieved from the web and the file(s) downloaded
-   \"retrieveFile\" if the URI starts \'torrent:\' - a \*.torrent file
    must be read from the file system and passed to BitTorrent to start
    downloading the file(s)

\
The code is as follows:\
\

    class InstructionParser(component):
        """
        Instructions on the inbox are processed according to the following rules:
        
        - If starts with 'file:' this is a path to a file that needs seeding. The 
          name is put on the outbox for the torrent making process to start. This
          leads to the TorrentPatron seeding the file
          
        - If starts with 'torrent:http://...' then the torrent file is obtained from 
          the http URL supplied and passed to the patron
          
        - If starts with 'torrent:...' (not http) then the torrent file is obtained
          from the filesystem and passed to the patron
        """
        Inboxes = ["inbox", "control"]
        Outboxes = ["outbox", "retrieveHtml", "retrieveFile", "signal"]
        def main(self):
            self.running = True
            while 1:
                if self.dataReady():
                    d = chop(self.recv())
                    if d.startswith("file:"):
                        self.send(d[5:])
                    elif d.startswith("torrent:http"):
                        self.send(d[8:], "retrieveHtml")
                    elif d.startswith("torrent:"):
                        self.send(d[8:], "retrieveFile")
                    else:
                        print("Message not understood: %s" % d)
                    
                if not self.anyReady() and self.running:
                    self.pause()
                if self.running:
                    yield 1

Notes:

-   The chop(f) function simply removes trailing *\\r* and *\\n*
    characters

Reading \*.torrent files
------------------------

If a torrent file URI has been given it needs to be downloaded.
Fortunately the components already exist: to download an HTML file, we
use the **SimpleHTTPClient** and reading a file is done with the
**TriggeredFileReader**. No code needed there!\
\

Making a torrent file
---------------------

If the name of a local file has been given, we need (a) to make a
torrent file, (b) to publish this to the BitTorrent tracker and (c) to
start seeding. In the network diagram above we have a number of
components to do this. Firstly **fnSplitter** is simply a Kamelia
**Fanout** component. This takes input on its inbox and *fans it out* to
a number of outboxes specified when the component is instantiated (which
we\'ll see later). We use this because we want the ready-made
**TorrentMaker** component to know what file it needs to make a torrent
from, and another set of components to create a new file named as per
the source file with a \'.torrent\' suffix into which we can write the
torrent so that we can pass it to anyone who may wish to download the
file we\'re publishing.\
\
**suffixTorrent** is a Kamaelia **PureTransformer** which takes a
function (can be a lambda) with which it transforms input into output.
We will use it to append \'.torrent\' to the string on the inbox.
**torrentNamer** is a **TwoSourceListifier** which takes input on two
inboxes and pairs them up to output them as a list. This component was
copied from Ryan Lothian\'s **torrentseeder.py** and is copied without
permission as follows:\
\

    class TwoSourceListifier(component):
        """Wait until inboxes "a" and "b" have messages, then
        take the first from each and combine them into a new list
        of the form [a,b]. Repeat.
        """
        Inboxes = ["a", "b", "control"]
        def main(self):
            while 1:
                yield 1
                
                while self.dataReady("a") and self.dataReady("b"):
                    self.send([self.recv("a"), self.recv("b")], "outbox")
                    
                while self.dataReady("control"):
                    msg = self.recv("control")
                    if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                        self.send(producerFinished(self), "signal")
                        return
                
                self.pause()

The final component, the **torrentWriter**, takes this list as input and
writes to disk the file named in element 0 with content in element 1 of
the list.\
\

Meanwhile\... let\'s seed or download
-------------------------------------

Now we have a torrent file. It may have been generated just now to
describe a local file that we wish to seed, or it may have been obtained
from elsewhere and describe a file we wish to download. Either way, the
**TorrentPatron** needs to know about it. TorrentPatron is a Kamaelia
component written by Ryan Lothian that manages the Mainline BitTorrent
code for Kamaelia. All we need to do is give it the torrent file *et
voila!* Any BitTorrent client givent torrent files generated by this
utility will now be able to download your file!\
\
The output is OK, but it could be made easier for upstream tools to
process. What I\'d like is to pass output of the form
\'*id:file:percentage complete*\' and this is just what the
**MonitorParser** does. Output from the **TorrentPatron** appears on its
inbox. The lines are re-formatted and sent to the outbox whereupon they
can be sent to the **ConsoleEchoer** (as in this case) or split off to
any other interested components (how about an **EmailEchoer**, or an
**IRCEchoer**? Or perhaps status messages could go to your phone - just
need an **SMSEchoer**!). The **MonitorParser** is simply as follows:\
\

    class MonitorParser(component):
        """Parses output from the TorrentPatron, keeping track of what torrents
    are made and how they are progressing. Outputs structured messages only when
    changes are observed."""
        def main(self):
            self.running = True
            # map torrent id to properties
            self.torrentMapper = {} 
            while 1:
                if self.dataReady():
                    d = chop(str(self.recv()))
                    tokens = d.split()
                    if tokens[0]=='New':
                        fn=tokens[5][2:]
                        id = int(tokens[2])
                        self.torrentMapper[id] = [fn, -1]
                        self.send(self.fmtOutput(id))
                    elif tokens[0]=='Torrent':
                        id = int(tokens[1])
                        finished = int(tokens[-1][:-1])
                        if self.torrentMapper[id][1] < finished:
                            self.torrentMapper[id][1] = finished
                            self.send(self.fmtOutput(id))
                    
                if not self.anyReady() and self.running:
                    self.pause()
                if self.running:
                    yield 1

        def fmtOutput(self, id):
            details = self.torrentMapper[id]
            return "%d:%s:%d" % (id,details[0],details[1])

Putting it all together
-----------------------

Now that we have all the components we need, we must link them together
with a **GraphLine**.\
\

        tracker = 'http://my.tracker.host:6969/announce'
        torrentdir = '/var/torrent'

        Graphline( reader = ConsoleReader(prompt=''),
                           parser = InstructionParser(),
                           fnsplitter = Fanout(['torrentmaker','torrentwriter']),
                           suffixtorrent = PureTransformer(lambda x : torrentdir + x + ".torrent"),
                           torrentNamer = TwoSourceListifier(),
                           torrentMaker = TorrentMaker(defaulttracker=tracker),
                           torrentWriter = WholeFileWriter(),
                           metasplitter = Fanout(['torrentwriter','patron']),
                           fileReader = DefaultTriggeredFileReader(torrentdir),
                           httpReader = SimpleHTTPClient(),
                           patron = TorrentPatron(),
                           console = ConsoleEchoer(),
                           monitor = MonitorParser(),
                           addCR = PureTransformer(lambda x : x+"\n"),
                           linkages = {
                                   ("reader","outbox") : ("parser","inbox"),
                                   ("parser","outbox") : ("fnsplitter","inbox"),
                                   ("fnsplitter","torrentmaker") : ("torrentMaker","inbox"),
                                   ("fnsplitter","torrentwriter") : ("suffixtorrent", "inbox"),
                                   ("suffixtorrent","outbox") : ("torrentNamer", "a"),
                                   ("torrentNamer","outbox") : ("torrentWriter","inbox"),
                                   ("parser","retrieveHtml") : ("httpReader","inbox"),
                                   ("parser","retrieveFile") : ("fileReader","inbox"),
                                   ("torrentMaker","outbox") : ("metasplitter","inbox"),
                                   ("metasplitter","torrentwriter") : ("torrentNamer","b"),
                                   ("metasplitter","patron") : ("patron","inbox"),
                                   ("fileReader", "outbox") : ("patron", "inbox"),
                                   ("httpReader","outbox") : ("patron", "inbox"),
                                   ("patron", "outbox") : ("Monitor", "inbox"),
                                   ("monitor", "outbox") : ("addCR","inbox"),
                                   ("addCR", "outbox") : ("console", "inbox"),
                               }
                          ).run()

This puts the components into the graph structure described in the image
at the top of this document, then commands the Kamaelia system to start
running.

Required infrastructure
-----------------------

None of this will work unless you have access to a BitTorrent tracker.
The tracker is a server application that lets all clients know where to
find files and which chunks to download from which machines. You can use
either a public server or, perhaps better for experimentation, simply
run one of your own. The BitTorrent package in the Kamaelia MegaBundle
that you must install for any of this to work contains a tracker; start
it with:\
\

     bittorrent-tracker --port port_number

You may encounter some problems with BitTorrent as it can be a touch
sensitive. Make note of the following:

1.  You cannot run more than one client on one machine. In otherwords,
    Host\_A can run a tracker and one seeder/downloader, Host\_B another
    seeder/downloader. Neither can run a second seeder/downloader.
2.  The Mainline BitTorrent code seems ony to want to seed files in the
    current working directory and only downloads files to the cwd also.
    However, you can use softlinks to collect files in one place without
    moving them from their normal location.
3.  Once downloaded do not immediately move the file away - this will
    prevent other clients downloading from a host that has the full
    file. As with collecting files together for seeding, if a downloaded
    file needs to reside elsewhere, soft-linking may provide the
    solution.\
4.  Occasionaly the tracker will ignore requests to seed a torrent. This
    may occur if you\'ve been testing and seeded the same torrent a few
    times. To rectify I\'ve found it best to stop the tracker, delete
    *\~/.bittorrent* and */tmp/dfile\**, then re-start the tracker. I\'m
    not sure where the tracker keeps its config and state files when run
    under Windows (please edit if you know!)\

\
