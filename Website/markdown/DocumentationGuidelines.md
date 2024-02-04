---
pagename: DocumentationGuidelines
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Documenting Components]{style="font-size: 19pt; font-weight: 600;"}

[Some hopefully helpful guidelines!]{style="font-size: 12pt;"}

These are the current guidelines for documenting Kamaelia components,
covering:

-   Writing style
-   Structure and format
-   Example(s)
-   A template for your reference

[It is better for there to be some documentation than none at
all]{style="font-weight: 600;"} \... even if it breaks these guidelines
or is incomplete. Don\'t let these guidelines stop you writing!
Documentation can be developed iteratively, just like code. No
documentation is perfect. Much of our existing documentation probably
breaks many of these guidelines! Think of this as documentation of our
current best practice. This is a
[descriptive]{style="font-weight: 600;"} set of
[guidelines]{style="font-weight: 600;"} explaining [\"how we have done
it and what works for us\"]{style="font-style: italic;"}. This is
[not]{style="font-weight: 600;"} a
[prescriptive]{style="font-weight: 600;"} demand that [\"things must be
documented this way\"]{style="font-style: italic;"}.

In these guidelines, examples of [good ways to write are
green]{style="color: rgb(0, 103, 0);"}. Examples of [how
]{style="color: rgb(170, 0, 3);"}[not]{style="font-style: italic; color: rgb(170, 0, 3);"}[
to write are red.]{style="color: rgb(170, 0, 3);"}

[Why document? Who is the
Reader?]{style="font-size: 12pt; font-weight: 600;"}

Documentation should serve two different sets of readers:

-   [USERS]{style="font-weight: 600;"} - I want to use this component:
    what does it do? how do I plug it together with other components?
    how does it behave?
-   [Component Developers/Maintainers]{style="font-weight: 600;"} - I
    want to modify this component: how does the component work inside?
    why does it work that way and not another?

Because most components are small and lightweight, the main focus of
these guidelines is on documenting for usage. Pretend you are the
reader: what questions would you ask if you were seeing this component
for the first time? What would a developer need to know?

[Writing style]{style="font-size: 12pt; font-weight: 600;"}

Aim to write in the following way:

Write as if you are talking to the reader

-   You [are ]{style="font-style: italic;"}talking to the reader - they
    are reading [your]{style="font-style: italic;"} words!

Use consistent, short, clear and unambiguous statements.

-   A sentence of more than 10 words is probably too long. Keep it Short
    and Simple! It may sound patronising, but it makes it much easier to
    understand.
-   Don\'t skip words.

Use the [present
tense](http://en.wikipedia.org/wiki/Present_tense#English_present_indicative_tense)

-   say [\"ConsoleEchoer is designed
    to\"]{style="color: rgb(0, 103, 0);"}
-   don\'t say [\"ConsoleEchoer was designed
    to\"]{style="color: rgb(170, 0, 3);"}

Use the imperative - tell the reader what to do:

-   say [\"Do X to make Y
    happen\"]{style="font-style: italic; color: rgb(0, 103, 0);"}
-   don\'t say [\"When you do X, Y
    happens\"]{style="font-style: italic; color: rgb(170, 0, 3);"}

Refer to inboxes, outboxes and components by name

-   state whether it is an inbox or outbox!
-   say: [the \"inbox\"
    inbox]{style="font-style: italic; color: rgb(0, 103, 0);"} or:
    [ConsoleEchoer]{style="font-style: italic; color: rgb(0, 103, 0);"}

A reasonably good example:

-   [The TopologyViewerComponent renders to a pygame display surface.
    Send topology information to its \"inbox\" inbox, and nodes with
    links between them will
    appear.]{style="font-style: italic; color: rgb(0, 103, 0);"}

It could have been much unnecessarily wordy:

-   [A pygame display surface is used by the TopologyViewerComponent.
    When topology information has been sent by another component, this
    one will display the nodes and linkages between
    them.]{style="font-style: italic; color: rgb(170, 0, 3);"}

This is clear and explains precisely what happens:

-   [If a shutdownMicroprocess or producerFinished message is received
    on this component\'s \"control\" inbox, it will pass it on out of
    its \"signal\" outbox and immediately
    terminate.]{style="font-style: italic; color: rgb(0, 103, 0);"}

But this is much more ambiguous (what is a shutdown message? where do I
send it?):

-   [The component shuts down when it receives a shutdown
    message.]{style="font-style: italic; color: rgb(170, 0, 3);"}

This can often simply be a matter of taste of course. Terse is often
good, but unnecessarily terse is bad. Always aim for clarity above all
else.

[Structure and format]{style="font-size: 12pt; font-weight: 600;"}

The formatting style being used is broadly the [reStructured
Text](http://docutils.sourceforge.net/rst.html) format. For an overview
of this, see the
[primer](http://docutils.sourceforge.net/docs/user/rst/quickstart.html).
This has been chosen because of its simplicity and readability, but also
because it can be machine processed to automate the generation of, for
example, website documentation.

Document component(s) within a sourcefile by writing:

Write a [detailed docstring at the top]{style="font-weight: 600;"},
containing:

-   One short paragraph introduction
-   \"Example Usage\" section
-   \"How does it work\" section
-   Extra sections/sub sections if needed

<div>

</div>

A [docstring for the class]{style="font-weight: 600;"}, containing:

-   Constructor syntax:

           MyComponent(arg1,arg2[,optarg3]) -> new MyComponent component. 

-   One sentence description:

          Component that does X. 

-   Description of initializer arguments:

            Keyword arguments:
            
            - arg1     -- what this is
            - arg2     -- what this is
            - optarg3  -- None, or what value it takes (default=None)

<div>

</div>

A [docstring for each inbox and outbox]{style="font-weight: 600;"}, as
the value of the key:value pair

        Inboxes = { "inbox" : "Items to be xxxx'ed",
                    "control" : "Shutdown signalling",
                  }

\
[unused boxes should be documented as
such]{style="font-family: sans serif;"}

<div>

</div>

A [standard docstring for the initalizer]{style="font-weight: 600;"}
method:

     """x.__init__(...) initializes x; see x.__class__.__doc__ for signature""" 

-   [I\'m not totally convinced about this. Having nothing there is
    occasionally a pain \-- Michael.]{style="font-style: italic;"}

<div>

</div>

Docstrings for other methods and comments within the code, to assist
developers

See the example(s) and template below for the recommended syntax for
these parts.

If your sourcefile contains more than one component, then concatenate
the detailed docstrings for each component into one. Preface it with a
top level heading and one or two paragraphs of introduction.

Some general consistency rules:

Wordwrap at 80 columns to aid readability

-   exceptions can be made for list items and other short indented
    pieces.

<div>

</div>

Leave 3 blank lines between the end of a section and the heading for the
next.

<div>

</div>

Write python data structures in the language\'s own syntax. For example,
a python list:

<div>

[\[ \"moveto\", width, height \]]{style="font-family: courier new;"}

</div>

[Example]{style="font-size: 12pt; font-weight: 600;"}

The best examples are within the Kamaelia codebase itself. Here is a
snapshot (April 2006) of
[Kamaelia/Internet/TCPClient.py]{style="font-family: Courier New;"}
containing the [TCPClient]{style="font-family: Courier New;"} component.
The documentation is highlighted in green:

[]{style="font-family: courier new; color: rgb(0, 103, 0);"}

    """\
    =================
    Simple TCP Client
    =================

    This component is for making a TCP connection to a server. Send to its "inbox"
    inbox to send data to the server. Pick up data received from the server on its
    "outbox" outbox.



    Example Usage
    -------------

    Sending the contents of a file to a server at address 1.2.3.4 on port 1000::

        pipeline( RateControlledFileReader("myfile", rate=100000),
                  TCPClient("1.2.3.4", 1000),
                ).activate()



    How does it work?
    -----------------

    TCPClient opens a socket connection to the specified server on the specified
    port. Data received over the connection appears at the component's "outbox"
    outbox as strings. Data can be sent as strings by sending it to the "inbox"
    inbox.

    An optional delay (between component activation and attempting to connect) can
    be specified. The default is no delay.

    It creates a ConnectedSocketAdapter (CSA) to handle the socket connection and
    registers it with a selectorComponent so it is notified of incoming data. The
    selectorComponent is obtained by calling
    selectorComponent.getSelectorService(...) to look it up with the local
    Coordinating Assistant Tracker (CAT).

    TCPClient wires itself to the "FactoryFeedback" outbox of the CSA. It also wires
    its "inbox" inbox to pass data straight through to the CSA's "DataSend" inbox,
    and its "outbox" outbox to pass through data from the CSA's "outbox" outbox.

    Socket errors (after the connection has been successfully established) may be
    sent to the "signal" outbox.

    This component will terminate if the CSA sends a socketShutdown message to its
    "FactoryFeedback" outbox.

    Messages sent to the "control" inbox are ignored - users of this component
    cannot ask it to close the connection.
    """

    class TCPClient(component):
        """\
        TCPClient(host,port[,delay]) -> new TCPClient component.
        
        Establishes a TCP connection to the specified server.
           
        Keyword arguments:
          
        - host   -- address of the server to connect to (string)
        - port   -- port number to connect on
        - delay  -- delay (seconds) after activation before connecting (default=0)
        """    Inboxes  = { "inbox"           : "data to send to the socket",
                                   "_socketFeedback" : "notifications from the ConnectedSocketAdapter",
                    "control"         : "NOT USED"
                  }
        Outboxes = { "outbox"         :  "data received from the socket",
                     "signal"         :  "socket errors",
                     "_selectorSignal" : "communicating with a selectorComponent",
                   }

        def __init__(self,host,port,delay=0):
            """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
                  super(TCPClient, self).__init__()
                  self.host = host
                  self.port = port
                  self.delay=delay

               ...

[A template]{style="font-size: 12pt; font-weight: 600;"}

The following \'template\' points out some of the formatting and
stylistic points already described:

[]{style="font-family: courier new;"}

    #!/usr/bin/env python
    # <>

    """\
    ============
    What it does
    ============

    Short, one paragraph description of what this component does, or the task it achieves.



    Example Usage
    -------------
    What this shows followed by double colon::
            def func():
        print "really really simple minimal code fragment"

    Indicate any runtime user input with a python prompt::       >>> func()
           really really simple minimal code fragment

    Optional comment on any particularly important thing to note about the above 
    example.


    How does it work?
    -----------------

    Statements, written in the present tense, describing in more detail what the 
    component does.

    Explicitly refer to "named" inbox an "named" outbox to avoid ambiguity.

    Does the component terminate? What are the conditions?

    If the 'xxxx' argument is set to yyy during initialization, then something
    different happens.

    What does the component *not* do?


    A subheading for a subtopic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lists of important items might be needed, such as commands:
        
        the item
            A description of the item, what it is and what it does, and maybe 
            consequences of that.

        another item
            A description of the item, what it is and what it does, and maybe 
                   consequences of that.

    You may also want bullet lists:

     - first item
     - second item



    Optional extra topics
    ---------------------

    May be necessary to describe something separately, eg. a complex data structure 
    the component expects to receive, or the GUI interface it provides.
    """

    class TheComponent(...):
        """\
            TheComponent(arg[,optarg]) -> new TheComponent component.
        
            Component that does something.
        
            Keyword arguments:
            
            - arg     -- specifys something
            - optarg  -- None, or something else (default=None)
            """
        
            Inboxes = { "inbox"   : "What you send to here",
                                   "control" : "Shutdown signalling",
                      }
            Outboxes = { "outbox" : "What comes out of here,
                                      "something" : "NOT USED",
                                     "signal" : "Shutdown signalling",
                       }

            def __init__(self, ...):
                    """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
                    ...

                ...rest of the component...
