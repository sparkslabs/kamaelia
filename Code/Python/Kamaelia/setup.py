#!/usr/bin/env python
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

from distutils.core import setup

setup(name = "kamaelia",
      version = "1.14.32", # Semver update
      description = "Kamaelia - Multimedia & Server Development Kit",

      author = "Michael Sparks (sparkslabs)",
      author_email = "sparks.m@gmail.com",
      url = "http://www.kamaelia.org/",
      license ="Apache Software License",
      packages = [\
                  "Kamaelia", # START
                  "Kamaelia.Apps",
                  "Kamaelia.Apps.CL",
                  "Kamaelia.Apps.CL.CollabViewer",
                  "Kamaelia.Apps.CL.FOAFViewer",
                  "Kamaelia.Apps.Compose",
                  "Kamaelia.Apps.Compose.GUI",
                  "Kamaelia.Apps.Europython09",
                  "Kamaelia.Apps.Europython09.BB",
                  "Kamaelia.Apps.Games4Kids",
                  "Kamaelia.Apps.Grey",
                  "Kamaelia.Apps.GSOCPaint",
                  "Kamaelia.Apps.IRCLogger",
                  "Kamaelia.Apps.JsonRPC",
                  "Kamaelia.Apps.JMB",
                  "Kamaelia.Apps.JMB.Common",
                  "Kamaelia.Apps.JMB.WSGI",
                  "Kamaelia.Apps.JMB.WSGI.Apps",
                  "Kamaelia.Apps.JPB",
                  "Kamaelia.Apps.MH",
                  "Kamaelia.Apps.MPS",
                  "Kamaelia.Apps.SA",
                  "Kamaelia.Apps.Show",
                  "Kamaelia.Apps.SocialBookmarks",
                  "Kamaelia.Apps.SpeakNWrite",
                  "Kamaelia.Apps.SpeakNWrite.Gestures",
                  "Kamaelia.Apps.Whiteboard",
                  "Kamaelia.Automata",
                  "Kamaelia.Audio",
                  "Kamaelia.Audio.PyMedia",
                  "Kamaelia.Audio.Codec",
                  "Kamaelia.Audio.Codec.PyMedia",
                  "Kamaelia.Chassis",
                  "Kamaelia.Codec",
                  "Kamaelia.Device",
                  "Kamaelia.Device.DVB",
                  "Kamaelia.Device.DVB.Parse",
                  "Kamaelia.Experimental",
                  "Kamaelia.File",
                  "Kamaelia.Internet",
                  "Kamaelia.Internet.Simulate",
                  "Kamaelia.Protocol",
                  "Kamaelia.Protocol.AIM",
                  "Kamaelia.Protocol.HTTP",
                  "Kamaelia.Protocol.HTTP.Handlers",
                  "Kamaelia.Protocol.IRC",
                  "Kamaelia.Protocol.RTP",
                  "Kamaelia.Protocol.Torrent",
                  "Kamaelia.Support",
                  "Kamaelia.Support.Data",
                  "Kamaelia.Support.DVB",
                  "Kamaelia.Support.Particles",
                  "Kamaelia.Support.Protocol",
                  "Kamaelia.Support.PyMedia",
                  "Kamaelia.Support.Tk",
                  "Kamaelia.UI",
                  "Kamaelia.UI.Tk",
                  "Kamaelia.UI.MH",
                  "Kamaelia.UI.Pygame",  
                  "Kamaelia.UI.OpenGL",
                  "Kamaelia.Util",
                  "Kamaelia.Util.Tokenisation",
                  "Kamaelia.Video",
                  "Kamaelia.Visualisation",
                  "Kamaelia.Visualisation.Axon",
                  "Kamaelia.Visualisation.ER",
                  "Kamaelia.Visualisation.PhysicsGraph",
                  "Kamaelia.Visualisation.PhysicsGraph3D",
                  "Kamaelia.XML", # LAST
                  ],
#      scripts = ['Tools/KamaeliaPresent.py'],
      long_description = """
Kamaelia, A fast overview
=========================

`Kamaelia <https://www.kamaelia.org/Home.html>`__ is a Python library by
`BBC Research <http://www.bbc.co.uk/opensource/projects/kamaelia/>`__
for concurrent programming using a simple pattern of components that
send and receive data from each other.

Note: this is the first alpha release of the Kamaelia 'refresh' project to
bring Kamaelia up to date with the modern python ecosystem.

A quick overview
================

| The following is an example of a system made by piping the output of
  one component into another:

   ::

      from Kamaelia.Chassis.Pipeline import Pipeline
      from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

      Pipeline(
               ConsoleReader(),
               ConsoleEchoer(),
      ).run()

Or maybe you want to build a presentation tool? (imports & setup
excluded here)

   ::

      Graphline(
           CHOOSER = Chooser(items = files),
           IMAGE = Image(size=(800,600), position=(8,48)),
           NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
           PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
           FIRST = Button(caption="First", msg="FIRST",position=(256,8)),
           LAST = Button(caption="Last", msg="LAST",position=(320,8)),
           linkages = {
              ("NEXT","outbox") : ("CHOOSER","inbox"),
              ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
              ("FIRST","outbox") : ("CHOOSER","inbox"),
              ("LAST","outbox") : ("CHOOSER","inbox"),
              ("CHOOSER","outbox") : ("IMAGE","inbox"),
           }
      ).run()

| That's all well and good, but how is a component written? What's
  inside it?

   ::

      from Axon.Component import component
      from Axon.Ipc import shutdownMicroprocess, producerFinished

      class MyComponent(component):    
          Inboxes = {"inbox"        : "some data in",
                     "control"      : "stops the component"}
          Outboxes = {"outbox"      : "some data out",
                      "signal"      : "Shutdown signal"}

          def __init__(self, **argd):
              super(MyComponent, self).__init__(**argd)

          def main(self):
              while not self.doShutdown():
                  if self.dataReady("inbox"):
                      data = self.recv("inbox")
                      # let's echo what we received...
                      self.send(data, 'outbox')

                  if not self.anyReady():
                      self.pause()

                  yield 1

          def doShutdown(self):
              if self.dataReady("control"):
                  mes = self.recv("control")
                  if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                      self.send(producerFinished(), "signal")
                      return True
              return False

This is the simplest form a component can take. A component:

-  is a class that inherits from ``Axon.Component.component``
-  has inboxes and outboxes

By inheriting from ``Axon.Component.component`` you make your class
usable by the Axon library which is at the core of the
Kamaelia library. It allows for your class to be used with other
components.

Inboxes and outboxes allow your component to be linked to and from by
other components.

Then your class defines a main method that simple loop until a specific
kind of message is put into the "control" inbox of the component. During
the looping it checks for any inboxes and process data read from them.
Eventually it yields to the Axon scheduler that goes to the next
available component. By using a generator we allow the shceduler to come
back to the component's loop eventually.

Note that inboxes and outboxes are pure Python dictionary hence they
allow for any Python objects and are not limited to strings. The
component described above is simple, complex components have many
inboxes and outboxes to link to and from.

Kamaelia
--------

Kamaelia is a library of components for `all kind of tasks and
topics <https://kamaelia.org/Components.html>`__:

For example taking the previous example we could write:

   ::

      from Kamaelia.Chassis.Pipeline import Pipeline
      from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

      Pipeline(
               ConsoleReader(),
               MyComponent(),
               ConsoleEchoer(),
      ).run()

`Pipeline <https://kamaelia.org/Components/pydoc/Kamaelia.Chassis.Pipeline.html>`__
is component that automatically links outboxes to inboxes of each
provided component. The console components allow for reading and writing
data from and to the command line. Because ``Pipeline`` is also a
component itself it could in turns be used in another component.

Note that calling the ``run()`` method on a component blocks the process
until it is killed. You can also simply activate a component which will
then be in an active state but will run only when eventually ``run`` is
called on another component.
"""
      )
