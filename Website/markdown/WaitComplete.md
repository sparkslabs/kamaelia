---
pagename: WaitComplete
last-modified-date: 2008-10-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Axon.Ipc.WaitComplete
=====================

The purpose behind WaitComplete is to allow a generator based component
to say cleanly: run this other generator for a while and when they\'re
done, return to me. This allows for more direct representation of
certain kinds of code structure. It is likely to be joined at somepoint
with a \"continue with this\" style message. There are two common
usecases where it is nice to use:\

One is with regard to reading lines of data from a network connection.
This allows for a more direct form of writing code, and essentially
provides a mechanism of dealing with the idea that \"you can\'t nest
yield statements cleanly\". But telling the scheduler \"run this until
it\'s finished, not me\" you essentially gain that ability.

The other is where you are requesting a resource from a Kamaelia service
using the idiom

Find the service, create links to talk to it

Send it a message

Wait for the response, containing the resource\

Move on

-   A good example of a resource that\'s like this is pygame displays\

Basic Usage
-----------

To give an example which isn\'t tied up with a usecase, but just shows
the mechanism, you use it like this:\

>     class myComponent(Axon.Component.component):
>         def main(self):
>             print "Running inside main"
>             yield WaitComplete( self.someGenerator() )
>             print "Back Running inside main"
>             yield WaitComplete( self.anotherGenerator() )
>             print "Back Running inside main again"
>
>         def someGenerator(self):
>             print "running in the secondary generator"
>             yield 1
>             print "still running in the secondary generator"
>             yield 1
>
>         def anotherGenerator(self):
>             print "running in the other secondary generator"
>             yield 1
>             print "still running in the other secondary generator"
>             yield 1

The way that runs it would result in the following output:\

>     Running inside main
>     running in the secondary generator
>     still running in the secondary generator
>     Back Running inside main
>     running in the other secondary generator
>     still running in the other secondary generator
>     Back Running inside main again

This doesn\'t look like a big deal, but it\'s worth asking \"what would
this look like without WaitComplete\" ?\
\
If we were doing this without WaitComplete, it would look like this:\

    class myComponent(Axon.Component.component):
        def main(self):
            print "Running inside main"
            for i in self.someGenerator():
                yield i
            print "Back Running inside main"
            for i self.anotherGenerator():
                yield i
            print "Back Running inside main again"

        def someGenerator(self):
            print "running in the secondary generator"
            yield 1
            print "still running in the secondary generator"
            yield 1

        def anotherGenerator(self):
            print "running in the other secondary generator"
            yield 1
            print "still running in the other secondary generator"
            yield 1

Whilst it\'s not that much worse, it does obfuscate things, as we\'ll
see with real world examples.\

Real world example - Connecting to a POP3 server & Logging in
-------------------------------------------------------------

The following code is from a basic POP3 client skeleton (as used in the
client side spam tools):\

>         def waitForBanner(self):
>             yield WaitComplete(self.getline(), tag="_getline1")
>             self.banner = self.line.strip()
>
>             if self.banner[:3] == "+OK":
>                 self.connectionSuccess = True
>             else:
>                 self.connectionSuccess = False
>
>         def doLogin(self, username, password):
>             self.sendCommand("USER "+username)
>             yield WaitComplete(self.getline(), tag="_getline2")
>             if self.line[:3] == "+OK":
>                 self.sendCommand("PASS "+ password)
>                 yield WaitComplete(self.getline(), tag="_getline3")
>                 if self.line[:3] == "+OK":
>                     self.loggedIn = True
>
>         def main(self):
>             self.control_message = None
>             self.connectionSuccess = False
>             self.loggedIn = False
>
>             yield WaitComplete(self.waitForBanner())
>
>             if self.connectionSuccess:
>                 yield WaitComplete( self.doLogin(self.username, self.password))
>
>                 if self.loggedIn:
>                     run = True
>                     while run:
>                         while not self.anyReady():
>                             self.pause()
>                             yield 1
>                         while self.dataReady("client_inbox"):
>                             command = self.recv("client_inbox")
>                             yield WaitComplete(self.handleCommand(command))
>                             if command[0] == "QUIT":
>                                run = False
>
>                     self.sendCommand("QUIT")
>                     yield WaitComplete(self.getline(), tag="_getline5")
>     #                print "SERVER RESPONSE", self.line

Now, ignoring the tag= parts at the end, restructuring this to use the
more tradition for \... in self.generator() syntax, you would get this:\

>         def waitForBanner(self):
>             for i in self.getline():
>                 yield i
>
>             self.banner = self.line.strip()
>
>             if self.banner[:3] == "+OK":
>                 self.connectionSuccess = True
>             else:
>                 self.connectionSuccess = False
>
>         def doLogin(self, username, password):
>             self.sendCommand("USER "+username)
>             for i in self.getline():
>                 yield i
>             if self.line[:3] == "+OK":
>                 self.sendCommand("PASS "+ password)
>                 for i in self.getline():
>                     yield i
>                 if self.line[:3] == "+OK":
>                     self.loggedIn = True
>
>         def main(self):
>             self.control_message = None
>             self.connectionSuccess = False
>             self.loggedIn = False
>
>             for i in self.waitForBanner():
>                 yield i
>
>             if self.connectionSuccess:
>                 for i in self.doLogin(self.username, self.password):
>                     yield i
>
>                 if self.loggedIn:
>                     run = True
>                     while run:
>                         while not self.anyReady():
>                             self.pause()
>                             yield 1
>                         while self.dataReady("client_inbox"):
>                             command = self.recv("client_inbox")
>                             for i in self.handleCommand(command):
>                                  yield i
>                             if command[0] == "QUIT":
>                                run = False
>
>                     self.sendCommand("QUIT")
>                     for i in self.getline():
>                         yield i
>     #                print "SERVER RESPONSE", self.line

Whilst each individual part is only slightly less clear, the overall
effect is significantly less clear.\
\
The tag= line incidentally allows us to give each call to a generator a
different tag. This allows us to determine if a generator is getting
stuck in any particular state. In the case of a network system, knowing
just where the system is getting unexpected data (or not getting
expected data) causing it to stay in an unexpected state is particularly
useful - hence the use of tags. In the second, non-WaitComplete version
we don\'t have that hinting available.\

Real World Example - Requesting A Pygame Display Surface
--------------------------------------------------------

In this example we have to do this:\

-   Find the pygame display
-   Send it a request
-   Wait for the response

This is a common task that would be nice to wrap up inside a method that
we can just call trivially. Again this is where WaitComplete comes in,
since it assists in wrapping up this functionality cleanly as follows:\

>         def __init__(self, **argd):
>     ....
>             self.disprequest = { "DISPLAYREQUEST" : True,
>                                "callback" : (self,"callback"),
>                                "size": self.displaysize}
>
>         def getDisplay(self):
>            displayservice = PygameDisplay.getDisplayService()
>            self.link((self,"display_signal"), displayservice)
>            self.send(self.disprequest, "display_signal")
>            while not self.dataReady("callback"):
>                self.pause()
>                yield 1
>            self.display = self.recv("callback")

This can then be used like this:\

>         def main(self):
>            yield WaitComplete(self.getDisplay())

And **that** is a significant simplication over the current structure.\
\
Furthermore, it also allows this:\

>         def getDisplay(self):
>
>            def gen():
>               displayservice = PygameDisplay.getDisplayService()
>               self.link((self,"display_signal"), displayservice)
>               self.send(self.disprequest, "display_signal")
>
>               while not self.dataReady("callback"):
>                   self.pause()
>                   yield 1
>
>               self.display = self.recv("callback")
>
>            return WaitComplete(get())

Which can itself be used like this:\

>         def main(self):
>            yield self.getDisplay()

It\'s perhaps worth noting that the common alternative here is this:\

>         def main(self):
>            displayservice = PygameDisplay.getDisplayService()
>            self.link((self,"display_signal"), displayservice)
>            self.send(self.disprequest, "display_signal")
>
>            while not self.dataReady("callback"):
>                self.pause()
>                yield 1
>
>            self.display = self.recv("callback")

And that for example is something that can be placed into a potential
baseclass to be used as a re-usable mixin, which can then just be used
in a simple manner of \"yield self.getDisplay()\".\
Given that this is a commonly used idiom, the ability to cleanly wrap
this is a massive advantage.\

Summary
-------

WaitComplete is a useful as:\

-   Syntactic sugar to make a common construct clearer
-   A mechanism for wrapping up functionality that needs to yield inside
    a seperate method for reuse
-   A mechanism for assisting debugging of more complex systems, due to
    the tag= notation.

\
