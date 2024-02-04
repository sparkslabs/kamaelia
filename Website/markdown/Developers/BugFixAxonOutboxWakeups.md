---
pagename: Developers/BugFixAxonOutboxWakeups
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Feature: AxonOutboxWakeups
==========================

(This page describes an implementation of the above)\

If you\'re interested, this branch in the repository contains:\
\
1) (Long awaited) unpausing of components with outboxes in a chain of
linkages whenever messages are collected from the destination inbox.\
\
2) Additions to the axon test suite to cover this, and aspects of
size-limited boxes that previously lacked unittests.\
\
Apologies for the length of this posting, read the sections you\'re
interested in:\
WHAT DOES THIS FIX?\
ABOUT THE IMPLEMENTATION\
TIME COMPLEXITY\
TEST SUITE ADDITIONS\
\
If anyone has some spare time to take a look, I\'d be really grateful
for a sanity check on the implementation. In particular, checking
whether it breaks any code you\'ve written. It shouldn\'t, but you never
know!\
\
Constructive criticism of the implementation is also welcome - the
rationale is explained below.\
\
**WHAT DOES THIS FIX?**\
\
(1) is a bugfix \... this capability existed in the orginal 1.0 release
of Axon, before we make the message delivery optimisations. The
optimised version removed the postman from the equation, so messages
would be delivered immediately and directly into the destination inbox.\
\
What has actually been implemented? Here\'s a concrete example, or what
this bugfix makes possible:\
\

          from Axon.Component import component
          from Axon.ThreadedComponent import threadedcomponent
          from Axon.AxonExceptions import noSpaceInBox

          class Producer(component):
              def main(self):
                  for i in range(100):
                      sent=False
                      while not sent:
                          try:
                              self.send(i, "outbox")
                              sent=True
                          except noSpaceInBox:
                              self.pause()
                              yield 1

          class SlowConsumer(threadedcomponent):
              def __init__(self):
                  super(SlowConsumer,self).__init__(queuelengths=5)

              def main(self):
                  self.inboxes['inbox'].setSize(5)
                  while 1:
                      time.sleep(0.5)
                      while not self.dataReady("inbox"):
                          self.pause()
                      print self.recv("inbox")

          from Kamaelia.Pipeline import Pipeline
          Pipeline(Producer(),SlowConsumer()).run()

\
The slow consumer restricts its inbox to hold a maximum of 5 items (and
the internal queues to also a maximum of 5 items). This means the
producer receives noSpaceInBox exceptions when the box it is trying to
send to is full.\
\
This bugfix means that if the Producer pauses, it will be woken when the
Consumer consumes an item (implying there may\[\*\] now be space for it
to send more)\
\
\[\*\] \"may\" rather than \"is\" becuase if there are multiple
Producers sending to the same inbox, all are woken, but there might not
be enough free space for them all to send. Plus there are no fairness
guarantees at present.\
\
There are more complete examples like this in the branch in:\
\.../Tests/Python/Axon/wakeuptest.py\
\.../Tests/Python/Axon/wakeuptest2.py\
\
\
**ABOUT THE IMPLEMENTATION**\
\
This implementation is mainly changes to Box.py \... enabling postbox
objects to build and maintain a list of notification callbacks to be
triggered when a message is \'pop\'ed from a box.\
\
The postbox class now lets you specify a notification callback when it
is constructed. This will be called whenever a message is collected
(popped) in the chain of linkages this box is part of.\
\
Inboxes, obviously, do not use this notification callback. Outboxes do.\
\
Each postbox maintains, a list of all callback it needs to call if a
message is collected from it. When a linkage is added (addsource method
called on the destination of the linkage), it collects this list from
the new source, adds it to its own list, and instructs the next
component down the chain of linkages to do the same, ie. it recurses
down the chain to make sure all downstream boxes update their list of
callbacks.\
\
For example:\
\
outboxA \-\-\--\>\
outboxB \-\-\--\> inbox1 \-\-\--\> inbox2 \-\-\--\> inbox3\
\
outboxC \-\-\--\> inbox4\
\
The callbacks lists for all boxes will be:\
outboxA : \[\]\
outboxB : \[\]\
inbox1 : \[A,B\]\
inbox2 : \[A,B\]\
inbox3 : \[A,B\]\
outboxC : \[\]\
inbox4 : \[C\]\
\
If a linkage is added from inbox4 \-\--\> inbox2:\
\
outboxA \-\-\--\>\
outboxB \-\-\--\> inbox1 \-\-\--\> inbox2 \-\-\--\> inbox3\
A\
\|\
outboxC \-\-\--\> inbox4 \-\-\-\-\-\-\--\' new linkage\
\
Then the callback lists change for inbox2 and inbox3 only:\
\
outboxA : \[\]\
outboxB : \[\]\
inbox1 : \[A,B\]\
inbox2 : \[A,B,C\] \# C added\
inbox3 : \[A,B,C\] \# C added\
outboxC : \[\]\
inbox4 : \[C\]\
\
When a linkage is removed, the exact reverse process happens - the list
of callbacks is obtained from the soon-to-be-no-longer source, and is
then removed from the list of local callbacks. The same happens for all
downstream boxes.\
\
To facilitate this implementation, the existing \'retarget\' method that
is used to establish the linkages had to be modified slightly to enable
each postbox to know which postbox it is linked to next along the chain
of linkages (held in self.target). Previously it did not maintain this,
as all that was needed was direct references to the final destination
box, for delivering messages.\
\
threadedcomponent has also been modified to ensure it wakes up the
thread if it gets unpaused.\
\
\
**TIME COMPLEXITY**\
\
The additional time complexity of all three aspects (issuing the
notification, creating a linkage, removing a linkage) is O(n) worst
case.\
\
Issuing the notifications is, I suspect, by far the most common task. I
reckon this implementation is as cheap as it can be (simply iteration
through a list and making the call backs) without more radical changes
to Axon/Axon\'s behaviour (eg. reducing the circumstances in which
unpausing should happen)\
\
Creating and removing linkages is therefore more expensive - since it is
effectively collating and updating lists of callbacks. But my personal
feeling is that this tradeoff is acceptable. Particuarly for a first cut
implementation.\
\
\
**TEST SUITE ADDITIONS**\
\
Tests have been added to cover the bugfix, for both ordinary and
threaded components.\
\
Tests have also been added to cover setting size limits on inboxes - and
the consequent expectation that when a box becomes full, a noSpaceInBox
exception is raised. The tests again cover both ordinary and threaded
components.\
\
