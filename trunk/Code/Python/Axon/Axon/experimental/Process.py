#!/usr/bin/python

import Axon
from Axon.Scheduler import scheduler
import Axon.experimental._pprocess_support
import pprocess
import time
import pprint

# --- Support code, this will go back into the library. ---------------------------------------------------------
class ProcessWrapComponent(object):
    def __init__(self, somecomponent):
#        print "somecomponent.name",somecomponent.name
        self.exchange = pprocess.Exchange()
        self.channel = None
        self.inbound = []
        self.thecomponent = somecomponent
        self.ce = None
        self.tick = time.time()

    def ticking(self):
        if time.time() - self.tick > 1:
#            print "TICK", self.thecomponent.name
            self.tick = time.time()

    def run(self, channel):
        self.exchange.add(channel)
        self.channel = channel
#        print "ZZZZZZZZ"
        from Axon.experimental._pprocess_support import likefile, background
#        print "Hi",scheduler.run.threads
        background(zap=True).start()
        time.sleep(0.1)
#        print "Bye",scheduler.run.threads
#        print "Here???"

        self.ce = likefile(self.thecomponent)
        for i in self.main():
            pass

    def activate(self):
#        print "XXXXXXX"
        channel = pprocess.start(self.run)
#        print "YYYYYYY"
        return channel

    def main(self):
#        print "Running?"
        t = 0
        while 1:
#            self.ticking()
            if time.time() - t > 0.2:
                t = time.time()

            if self.exchange.ready(0):
                chan = self.exchange.ready(0)[0]
                D = chan._receive()
#                print "pwc:- SEND", D, "TO", self.thecomponent.name, ".",".", 
                self.ce.put(*D)
#                print ".","SENT"

            D = self.ce.anyReady()
            if D:
                for boxname in D:
#                    print "DUM, DUM DUM! 1 ",D
                    D = self.ce.get(boxname)
#                    print "DUM, DUM DUM! 2 ",D
                    self.channel._send((D, boxname))
#                    print "DUM, DUM DUM! 3 ",D
#                print "GAH!"
            yield 1
#            if self.channel.closed:
#                print self.channel.closed

def ProcessPipeline(*components):
    exchange = pprocess.Exchange()
    debug = False
    chans = []
#    print "TESTING ME"
    for comp in components:
        A = ProcessWrapComponent( comp )
        chan = A.activate()
        chans.append( chan )
        exchange.add(chan )

    mappings = {}
    for i in xrange(len(components)-1):
         mappings[ (chans[i], "outbox") ] = (chans[i+1], "inbox")
         mappings[ (chans[i], "signal") ] = (chans[i+1], "control")

    while 1:
        for chan in exchange.ready(0):
            D = chan._receive()
            try:
                dest = mappings[ ( chan, D[1] ) ]
                dest[0]._send( (D[0], dest[1] ) )
#                print "FORWARDED", D
            except KeyError:
                # This error means that some component in the graphline spat out some data,
                # but the outbox it was sent to isn't linked anyway. This may be an error,
                # but generally speaking is not likely to be. 
                #
                # As a result, we suppress this error.
                # This would be nicer to make conditional, but at present we don't have a
                # naming mechanism in general to do this. Though __debug=1 as a parameter
                # seems reasonable.
                #
                # If someone needs to debug this, they can enable this:
                #
                if debug:
                    print "WARNING: Data sent to outbox not linked to anywhere. Error?"
                    print "chan, D[1] D[0]", chan, D[1], repr(D[0])
                    pprint.pprint( mappings )

        time.sleep(0.1)


def ProcessGraphline(**graphline_spec):
    chans = []
    count = 0
    component_to_chan = {}
    mappings = {}
    debug = graphline_spec.get("__debug", False)

    chan_to_compname = {}
    exchange = pprocess.Exchange()
    for comp in graphline_spec:
        if comp != "linkages" and comp[:2] != "__":
            A = ProcessWrapComponent( graphline_spec[comp] )
            chan = A.activate()
            chans.append( chan )
            chan_to_compname[ chan ] = comp
            exchange.add(chan )
            component_to_chan[comp] = chan
#            print comp, chan
            count += 1

    linkages = graphline_spec.get("linkages", {})
    for source in linkages:
        sink = linkages[source]
        mappings[ component_to_chan[source[0]], source[1] ] = component_to_chan[sink[0]], sink[1]

    while 1:
        for chan in exchange.ready(0):
#            print "CHAN", chan, chan_to_compname[ chan ]
            D = chan._receive()
#            print "DO WE EVEN GET HERE", D
            try:
                dest = mappings[ ( chan, D[1] ) ]
                dest[0]._send( (D[0], dest[1] ) )
            except KeyError:
                # This error means that some component in the graphline spat out some data,
                # but the outbox it was sent to isn't linked anyway. This may be an error,
                # but generally speaking is not likely to be. 
                #
                # As a result, we suppress this error.
                # This would be nicer to make conditional, but at present we don't have a
                # naming mechanism in general to do this. Though __debug=1 as a parameter
                # seems reasonable.
                #
                # If someone needs to debug this, they can enable this:
                #
                if debug:
                    print "WARNING: Data sent to outbox not linked to anywhere. Error?"
                    print "chan, D[1] D[0]", chan, D[1], repr(D[0])
                    pprint.pprint( mappings )
        time.sleep(0.001)


class ProcessPipelineComponent(Axon.Component.component):
    def __init__(self, *components, **argd):
        super(ProcessPipelineComponent,self).__init__(**argd)
        self.components = components

    def main(self):
        exchange = pprocess.Exchange()
        chans = []
        for comp in self.components:
            A = ProcessWrapComponent( comp )
            chan = A.activate()
            chans.append( chan )
            exchange.add(chan )

        mappings = {}
        for i in xrange(len(self.components)-1):
             mappings[ (chans[i], "outbox") ] = (chans[i+1], "inbox")
             mappings[ (chans[i], "signal") ] = (chans[i+1], "control")

        while 1:
            for chan in exchange.ready(0):
                D = chan._receive()
                dest = mappings[ ( chan, D[1] ) ]
                if chan != chans[-1]:
                    dest[0]._send( (D[0], dest[1] ) )
                else:
                    self.send(D[0], D[1]) # Pass through outbound
            while self.dataReady("inbox"):
                D = self.recv("inbox")
                chans[0]._send( (D, "inbox") ) # Pass through inbound

            while self.dataReady("control"):
                D = self.recv("inbox")
                chans[0]._send( (D, "control") ) # Pass through inbound
            yield 1


# --- End Support code ---------------------------------------------------------

if __name__ == "__main__":
    from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox

    if 0:
        from Kamaelia.Chassis.Pipeline import Pipeline
        ProcessGraphline(
                    component_one = Textbox(position=(20, 340),
                                     text_height=36,
                                     screen_width=900,
                                     screen_height=200,
                                     background_color=(130,0,70),
                                     text_color=(255,255,255)),
                    component_two = Pipeline(
                                        TextDisplayer(position=(20, 90),
                                            text_height=36,
                                            screen_width=900,
                                            screen_height=200,
                                            background_color=(130,0,70),
                                            text_color=(255,255,255)),
                                        Textbox(position=(20, 340),
                                             text_height=36,
                                             screen_width=900,
                                             screen_height=200,
                                             background_color=(130,0,70),
                                             text_color=(255,255,255)),
                                    ),
                    linkages = {
                        ("component_one", "outbox") : ("component_two", "inbox"),
                        ("component_one", "signal") : ("component_two", "control"),
                    },
                    __debug = True,
        )

    if 0:
        ProcessGraphline(
                    component_one = Textbox(position=(20, 340),
                                     text_height=36,
                                     screen_width=900,
                                     screen_height=200,
                                     background_color=(130,0,70),
                                     text_color=(255,255,255)),
                    component_two = TextDisplayer(position=(20, 90),
                                            text_height=36,
                                            screen_width=900,
                                            screen_height=200,
                                            background_color=(130,0,70),
                                            text_color=(255,255,255)),
                    linkages = {
                        ("component_one", "outbox") : ("component_two", "inbox"),
                        ("component_one", "signal") : ("component_two", "control"),
                    }
        )
    if 0:
        ProcessPipeline(
                    Textbox(position=(20, 340),
                                     text_height=36,
                                     screen_width=900,
                                     screen_height=200,
                                     background_color=(130,0,70),
                                     text_color=(255,255,255)),
                    TextDisplayer(position=(20, 90),
                                            text_height=36,
                                            screen_width=900,
                                            screen_height=200,
                                            background_color=(130,0,70),
                                            text_color=(255,255,255))
        )#.run()

    if 1:
        ProcessPipelineComponent(
                    Textbox(position=(20, 340),
                                     text_height=36,
                                     screen_width=900,
                                     screen_height=200,
                                     background_color=(130,0,70),
                                     text_color=(255,255,255)),
                    TextDisplayer(position=(20, 90),
                                            text_height=36,
                                            screen_width=900,
                                            screen_height=200,
                                            background_color=(130,0,70),
                                            text_color=(255,255,255))
        ).run()

    if 0:
        from Kamaelia.Chassis.Pipeline import Pipeline
        Pipeline(
#            ProcessPipelineComponent(
                    Textbox(position=(20, 340),
                                     text_height=36,
                                     screen_width=900,
                                     screen_height=200,
                                     background_color=(130,0,70),
                                     text_color=(255,255,255)),
#            ),
            ProcessPipelineComponent(
                    TextDisplayer(position=(20, 90),
                                            text_height=36,
                                            screen_width=900,
                                            screen_height=200,
                                            background_color=(130,0,70),
                                            text_color=(255,255,255))
            ),
        ).run()

