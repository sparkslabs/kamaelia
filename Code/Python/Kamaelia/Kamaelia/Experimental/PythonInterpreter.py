#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
"""
===========================
PythonInterpreter Component
===========================

Initial version of an interactive console in Kamaelia. Provides a nice way
of playing with Kamaelia components and examining running systems.

Example Usage
-------------

Show a pygame Textbox for reading user input, and a TextDisplayer, showing
the interpreter's response.

    from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer
    Pipeline(
        Textbox(size = (800, 300), position = (100,380)),
        InterpreterTransformer(),
        TextDisplayer(size = (800, 300), position = (100,40)),
    ).run()

This then operates as a normal python interpreter which happens to run in a
pygame window.

How to use it
-------------

This component takes python commands from its inbox "inbox", and spits out
normal python interpreter repsonses out its outbox "outbox". 


There are more examples in the examples directory.

Warning
-------

This component may well change its location in the Kamaelia namespace.

TODO
----

More detailed examples.

"""
import code
import traceback
from io import StringIO
import string

import Axon

class StandaloneInterpreter(Axon.ThreadedComponent.threadedcomponent):
    def console(self):
        while 1:
            yield input("> ")

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
                    print ("EPIC FAIL")
                    print (f.getvalue())
                    f.close()
                    print (__script__)
                    print (repr(__script__))
                    __script__ = ""

                if __line__[:1] != " ":
                    if __co__:
                        print ("\nok")
                        try:
                            __co__ = code.compile_command("_="+__script__, "<stdin>", "exec")
                        except:
                            pass

                        try:
                            pre = env.get("_", None)
                            env.update(globals())
                            env.update(locals())
                            env["_"] = pre
                            exec(__co__, env)
                            if env["_"]:
                                print (env["_"])
                                env["_"] = None
                        except:
                            f = StringIO.StringIO()
                            traceback.print_exc(file=f)
                            print ("EPIC FAIL")
                            print (f.getvalue())
                            f.close()
                        __script__ = ""
                    else:
                        last = __line__
                else:
                    last = __line__
        except EOFError:
            pass


class InterpreterTransformer(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        __script__ = ""
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
                            exec( __co__ , env)
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

    """
Some basic examples on how to use this interpreter.
"""

    from Kamaelia.Chassis.Pipeline import Pipeline

#FILE: STANDALONE
    if 0:
        StandaloneInterpreter().run()

#FILE: Console Embeddable
    if 0:
        from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
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
