#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Written as an example of how to write a chassis which provides
# some sort of service. Wasn't initially intended to be useful in its
# own right, but hey :-)
#

import Axon

# So we declare our class and main inboxes in the usual way
class TaggingPluggableProcessor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {
        "inbox": "Stream of data to process",
        "processor": "Processor requests are sent here",
        "control" : "So we can shutdown"
    }
    Outboxes = {
        "outbox": "Stream of tagged processed data",
        "signal": "To pass on shutdown",
        "_cs" : "For shutting down internal components"
    }

    def main(self):
        self.lookup = {}
        while not self.dataReady("control"):
            for processor_request in self.Inbox("processor"):
                self.add_processor(processor_request)

            for data in self.Inbox("inbox"):
                self.process_messages(data)

            for child in self.childComponents():
                if child._isStopped(): # Means they've exitted
                    self.remove_processor(child)
                    self.removeChild(child)   # deregisters linkages for us

            if self.anyReady():
                # Means that we have data waiting from a processor
                self.send_on_results()

            if not self.anyReady():
                self.pause()
            yield 1

        self.send(self.recv("control"), "signal")

        for c in self.childComponents():
            L = self.link( (self, "_cs"), (c, "control"))
            self.send( Axon.Ipc.producerFinished(), "_cs")
            self.unlink(thelinkage=L)        

    def add_processor(self, processor_request):
        tag, filter_func, filter_component = processor_request
        # Link to component so we can send it data
        to_component =  self.addOutbox("_to_component")
        self.link( (self, to_component), (filter_component, "inbox"))

        # Link from component so we can recieve results
        from_component = self.addInbox("_from_component")
        self.link( (filter_component, "outbox"), (self, from_component))
        
        bundle = { "tag": tag,
                   "filter_func":filter_func,
                   "component": filter_component,
                   "to_component" : to_component,
                   "from_component" : from_component }

        self.lookup[filter_component] = bundle
        self.lookup[from_component] = bundle
        self.addChildren(filter_component)
        filter_component.activate()

    def process_messages(self, data):
        for child in self.childComponents():
            bundle = self.lookup[child]
            if bundle["filter_func"](data):
                self.send(data, bundle["to_component"])

    def send_on_results(self):
        inbox_ready = self.anyReady()
        while inbox_ready:
            bundle = self.lookup[inbox_ready]
            for message in self.Inbox(inbox_ready):
                self.send( (bundle["tag"], message), "outbox")
            inbox_ready = self.anyReady()

    def remove_processor(self, child):
        bundle = self.lookup[child]
        from_component = bundle["from_component"]
        del self.lookup[ from_component ]
        del self.lookup[ child ] 
        for k in bundle:
            bundle[k] = None

if __name__ == "__main__":
    import time

    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Chassis.Seq import Seq

    class Pauser(Axon.ThreadedComponent.threadedcomponent):
        def main(self):
            time.sleep(1)

    Graphline(
        DATASOURCE = Seq( Pauser(),DataSource([1,2,3,4,5,6])),
        PROCESSOR = TaggingPluggableProcessor(),
        PROCESSORSOURCE = DataSource([
                            ( "EVEN", lambda x: x % 2==0, PureTransformer(lambda x: "Even ! " + str(x)) ),
                            ( "ODD", lambda x: x % 2==1, PureTransformer(lambda x: "Odd ! " + str(x)) ),
                            ( "THREE", lambda x: x % 3==0, PureTransformer(lambda x: "Divisible by 3 ! " + str(x)) ),
                            ( "FOUR", lambda x: x % 4==0, PureTransformer(lambda x: "Divisible by 3 ! " + str(x)) ),
                        ]),
        CONSOLE = Pipeline( PureTransformer(lambda x: repr(x)+"\n"), ConsoleEchoer()),
        linkages = {
            ("DATASOURCE","outbox"): ("PROCESSOR", "inbox"),
            ("DATASOURCE","signal"): ("PROCESSOR", "control"),
            ("PROCESSORSOURCE","outbox"): ("PROCESSOR","processor"),
            ("PROCESSOR","outbox"): ("CONSOLE", "inbox"),
            ("PROCESSOR","signal"): ("CONSOLE", "control"),
        }
    ).run()

