#!/usr/bin/python


def greeting(self):
    try:
       greeting = self.greeting
    except AttributeError:
       greeting = "hello"
    print greeting

def get_name(self):
    try:
       self.outbox = self.name
    except AttributeError:
       self.outbox = raw_input(">>> ")

def farewell(self):
    print "goodbye", self.inbox

def seq(*funcs):
    class StateBundle(object):
        pass
    state = StateBundle()
    def run(**args):
        state.inbox = None
        state.outbox = None
        for arg in args:
           state.__setattr__(arg, args[arg])
        for i in funcs:
           i(state)
           state.inbox = state.outbox
        return state.outbox
    return run

Code = seq(greeting, get_name, farewell)

Code()
Code(greeting="bonjour", name="Michael")
