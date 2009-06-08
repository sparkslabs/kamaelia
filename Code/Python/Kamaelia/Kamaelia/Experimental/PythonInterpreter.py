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

class StandaloneInterpreter(Axon.ThreadedComponent.threadedcomponent):
    def console(self):
        while 1:
            yield raw_input("> ")

    def main(self):
        __script__ = ""
        __SCRIPT__ = self.console()
        last = ""
        __co__ = None
        env = {}
        try:
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
                        print "\nok"
                        try:
                            __co__ = code.compile_command("_="+__script__, "<stdin>", "exec")
                        except:
                            pass

                        try:
                            pre = env.get("_", None)
                            env.update(globals())
                            env.update(locals())
                            env["_"] = pre
                            exec __co__ in env
                            if env["_"]:
                                print env["_"]
                                env["_"] = None
                        except:
                            f = StringIO.StringIO()
                            traceback.print_exc(file=f)
                            print "EPIC FAIL"
                            print f.getvalue()
                            f.close()
                        __script__ = ""
                    else:
                        last = __line__
                else:
                    last = __line__
        except EOFError:
            pass


class InterpreterTransformer(Axon.ThreadedComponent.threadedcomponent):
    def console(self):
        while 1:
            yield raw_input("> ")

    def main(self):
        __script__ = ""
        __SCRIPT__ = self.console()
        last = ""
        __co__ = None
        env = {}
        self.send(" ")
        while True:
            for __line__ in self.Inbox("inbox"):
                _ = None
                __script__ = __script__ + __line__ + "\n"
                try:
                    __co__ = code.compile_command(__script__, "<stdin>", "exec")
                except:
                    f = StringIO.StringIO()
                    traceback.print_exc(file=f)
                    self.send( "EPIC FAIL", "outbox" )
                    self.send( f.getvalue() )
                    f.close()
                    self.send( repr(__script__) )
                    __script__ = ""

                if __line__[:1] != " ":
                    if __co__:
                        try:
                            __co__ = code.compile_command("_="+__script__, "<stdin>", "exec")
                        except:
                            pass

                        sent = False
                        try:
                            pre = env.get("_", None)
                            env.update(globals())
                            env.update(locals())
                            env["_"] = pre
                            exec __co__ in env
                            if env["_"]:
                                self.send( env["_"] )
                                env["_"] = None
                                sent = True
                        except:
                            f = StringIO.StringIO()
                            traceback.print_exc(file=f)
                            self.send( "EPIC FAIL" )
                            self.send( f.getvalue() )
                            f.close()
                            sent = True
                        __script__ = ""
                        if not sent:
                            self.send( " " )
                    else:
                        last = __line__
                else:
                    last = __line__

if __name__ == "__main__":

    from Kamaelia.Chassis.Pipeline import Pipeline

#FILE: STANDALONE
    if 0:
        StandaloneInterpreter().run()

#FILE: Console Embeddable
    if 0:
        from Kamaelia.Util.Console import *
        Pipeline(
            ConsoleReader(),
            InterpreterTransformer(),
            ConsoleEchoer(),
        ).run()


#FILE: Server Embeddable
    if 0:
        from Kamaelia.Chassis.ConnectedServer import ServerCore
        from Kamaelia.Util.PureTransformer import PureTransformer

        def NetInterpreter(*args, **argv):
            return Pipeline(
                        PureTransformer(lambda x: str(x).rstrip()),
                        InterpreterTransformer(),
                        PureTransformer(lambda x: str(x)+"\r\n>>> "),
                   )

        ServerCore(protocol=NetInterpreter, port=1236).run()


#FILE: Pygame Embeddable
    if 1:
        from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer
        Pipeline(
            Textbox(size = (800, 300), position = (100,380)),
            InterpreterTransformer(),
            TextDisplayer(size = (800, 300), position = (100,40)),
        ).run()
