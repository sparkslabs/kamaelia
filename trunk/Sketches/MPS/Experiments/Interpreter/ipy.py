#!/usr/bin/python
"""
Initial version of an interactive console in Kamaelia. Provides a nice way
of playing with Kamaelia components it seems.

First working/nice transcript:

> def send(arg):
>    self.send(arg)
>

ok
> from Kamaelia.UI.Pygame.Ticker import Ticker

ok
> X=Ticker()

ok
> def outputto(C):
>     self.link((self, "outbox"), (C, "inbox"))
>

ok
> outputto(X)

ok
> X.activate()

ok
> send("hello")

ok
> send("Chickens eat fish")

ok
> send("OK")

ok
> send("OKOKOKOKOK")

ok
> send("Interesting, that actually seems to work, I wonder what happens if I type alot in here")

ok
> send("Neat!")

ok

"""
import code
import traceback
import StringIO
import string

import Axon

class Interpreter(Axon.ThreadedComponent.threadedcomponent):
    def console(self):
        while 1:
            yield raw_input("> ")

    def main(self):
        __script__ = ""
        __SCRIPT__ = self.console()
        last = ""
        __co__ = None
        env = {}
        for __line__ in __SCRIPT__:
            _ = None
            __script__ = __script__ + __line__ + "\n"
            try:
                __co__ = code.compile_command(__script__, "<stdin>", "exec")
            except:
                f = StringIO.StringIO()
                traceback.print_exc(file=f)
                print "EPIC FAIL"
                print f.getvalue()
                f.close()
                print __script__
                print repr(__script__)
                __script__ = ""

            if __line__[:1] != " ":
                if __co__:
    #                if ("=" not in __script__ and 
    #                    ":" not in __script__ and
    #                    "print" not in __script__ ):
                    print "\nok"
                    try:
                        __co__ = code.compile_command("_="+__script__, "<stdin>", "exec")
                    except:
                        pass

    #                print "successful statement"
    #                # got a complete statement.  execute it!
    #                print "-"*40
    #                print __script__,
    #                print "-"*40
                    try:
                        env.update(globals())
                        env.update(locals())
                        exec __co__ in env
                    except:
                        f = StringIO.StringIO()
                        traceback.print_exc(file=f)
                        print "EPIC FAIL"
                        print f.getvalue()
                        f.close()
                    else:
                        if _:
                            print _
                            _ = None
                    __script__ = ""
                else:
                    last = __line__
            else:
                last = __line__

Interpreter().run()
