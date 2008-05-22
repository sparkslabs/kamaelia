from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline


class Gc (threadedcomponent):
    """
    This component builds a set of other components to track.  When this component receives
    a shutdownMicroprocess message on its control port it will kill off all components that are
    being tracked as well as their child components.  For a component to be collected, it must
    have a collectable(name) method and that method must return True.

    When the Gc attempts to collect an item, it first attempts to call the item's collectable method
    and passes its name as the first argument.  If the method does not exist or returns False, the
    item will not be collected.  If it has been determined that the item is collectable, then the
    Gc will determine if the box has a control inbox.  If it does, it will send a
    shutdownMicroprocess() message to its control inbox.  If it does not contain a control inbox,
    it will call its stop method unless it is a threadedcomponent, in which case it will raise
    an exception.

    Thus, you may define collectable components without a control inbox if they are not threaded and
    do not need any kind of notification upon destruction.
    """
    Inboxes = {'inbox' : 'Receive items to track',
               'control' : 'Receives Shutdown signals', }
    Outboxes = {'outbox' : 'Outputs items that are being tracked',
                'signal' : 'NOT USED',
                '_internal-signal' : 'Sends shutdown messages to tracked components',}
    def __init__(self, name, components = None):
        """
        -name - the name of the garbage collector
        -components - a list of components to be tracked
        """
        super(Gc, self).__init__()
        if components:
            self.components = components
        else:
            self.components = []
        self.name = name

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('inbox'):
                item = self.recv('inbox')
                try:
                    self.components.extend(item)
                except:
                    self.components.append(item)
                self.send(item, 'outbox')
                print 'received item!'

            while self.dataReady('control'):
                if isinstance(self.recv('control'),  shutdownMicroprocess):
                    print 'Collecting!'
                    [self.killComponent(x) for x in self.components if self.isCollectable(x)]
                    not_done = False

    def killComponent(self, component):
        """
        This method is the one that actually kills components.  It will send the component a
        shutdownMicroprocess message if it has a control inbox.  If it does not have a control inbox
        and is not a threadedcomponent, it will call the component's stop method.
        """
        component_list = [x for x in component.childComponents()if self.isCollectable(x)]
        component_list.append(component)

        for item in component_list:
            box_found = False
            for box in item.inboxes:
                if box == 'control':
                    self.link((self, '_internal-signal'), (item, 'control'))
                    self.send(shutdownMicroprocess(), item)
                    self.unlink(item)
                    box_found = True
            if not box_found:
                if not isinstance(item, threadedcomponent):
                    item.stop()
                    print 'stopping a component!'
                else:
                    raise 'Threaded component does not have a control inbox!'

    def isCollectable(self, component):
        """
        Returns true if component may be collected.  False otherwise.
        """
        try:
            return component.collectable(self.name)
        except:
            return False

if __name__ == '__main__':
    from Kamaelia.Chassis.Graphline import Graphline
    from Axon.Component import component

    class Killee(component):
        Inboxes = {'inbox' : 'NOT USED',}
        def __init__(self):
            super(Killee, self).__init__()
            print 'new killee made!'
        def main(self):
            not_done = True
            while not_done:
                yield 1

        def collectable(self,  name):
            return True

    class Killer(component):
        Outboxes = {'signal' : 'sends shutdown messages',
                    'outbox' : 'sends items to be tracked'}
        def __init__(self):
            super(Killer,  self).__init__()

        def main(self):
            not_done = True
            i = 0
            while not_done:
                i += 1
                if i == 50:
                    self.send(shutdownMicroprocess(), 'signal')
                    not_done = False
                else:
                    k = Killee()
                    k.activate()
                    self.send(k,  'outbox')
                yield 1

    Pipeline(Killer(), Gc('gc',  components=None)).run()
