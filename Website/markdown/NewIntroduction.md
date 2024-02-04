---
pagename: NewIntroduction
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia: A quick overview[ ](http://trac.defuze.org/wiki/KamaeliaQuickWord#AquickwordaboutAxonandKamaelia "Link to this section"){.anchor} {#AquickwordaboutAxonandKamaelia}
===========================================================================================================================================

::: {.wikipage}
::: {#searchable}
[[Kamaelia]{.icon}](http://kamaelia.sourceforge.net/){.ext-link} is a
Python library by [[BBC
Research]{.icon}](http://www.bbc.co.uk/opensource/projects/kamaelia/){.ext-link}
for concurrent programming using a simple pattern of components that
send and receive data from each other. The following is an example of a
system made by piping the output of one component into another:\

>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>
>     Pipeline(
>              ConsoleReader(),
>              ConsoleEchoer(),
>     ).run()

Or maybe you want to build a presentation tool? (imports & setup
excluded here - [full
example](../../../Examples/SimplestPresentationTool))\

>     Graphline(
>          CHOOSER = Chooser(items = files),
>          IMAGE = Image(size=(800,600), position=(8,48)),
>          NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
>          PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
>          FIRST = Button(caption="First", msg="FIRST",position=(256,8)),
>          LAST = Button(caption="Last", msg="LAST",position=(320,8)),
>          linkages = {
>             ("NEXT","outbox") : ("CHOOSER","inbox"),
>             ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
>             ("FIRST","outbox") : ("CHOOSER","inbox"),
>             ("LAST","outbox") : ("CHOOSER","inbox"),
>             ("CHOOSER","outbox") : ("IMAGE","inbox"),
>          }
>     ).run()

That\'s all well and good, but how is a component written? What\'s
inside it?\

> ::: {.code}
>     from Axon.Component import component
>     from Axon.Ipc import shutdownMicroprocess, producerFinished
>
>     class MyComponent(component):    
>         Inboxes = {"inbox"        : "some data in",
>                    "control"      : "stops the component"}
>         Outboxes = {"outbox"      : "some data out",
>                     "signal"      : "Shutdown signal"}
>
>         def __init__(self, **argd):
>             super(MyComponent, self).__init__(**argd)
>
>         def main(self):
>             while not self.doShutdown():
>                 if self.dataReady("inbox"):
>                     data = self.recv("inbox")
>                     # let's echo what we received...
>                     self.send(data, 'outbox')
>                         
>                 if not self.anyReady():
>                     self.pause()
>       
>                 yield 1
>
>         def doShutdown(self):
>             if self.dataReady("control"):
>                 mes = self.recv("control")                
>                 if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
>                     self.send(producerFinished(), "signal")
>                     return True
>             return False
> :::

This is the simplest form a component can take. A component:

-   is a class that inherits from `Axon.Component.component`
-   has inboxes and outboxes

By inheriting from `Axon.Component.component` you make your class usable
by the
[[Axon]{.icon}](http://kamaelia.sourceforge.net/MiniAxon/){.ext-link}
library which is at the core of the Kamaelia library. It allows for your
class to be used with other components.

Inboxes and outboxes allow your component to be linked to and from by
other components.

Then your class defines a main method that simple loop until a specific
kind of message is put into the \"control\" inbox of the component.
During the looping it checks for any inboxes and process data read from
them. Eventually it yields to the Axon scheduler that goes to the next
available component. By using a generator we allow the shceduler to come
back to the component\'s loop eventually.

Note that inboxes and outboxes are pure Python dictionary hence they
allow for any Python objects and are not limited to strings. The
component described above is simple, complex components have many
inboxes and outboxes to link to and from.

Kamaelia[ ](http://trac.defuze.org/wiki/KamaeliaQuickWord#Kamaelia "Link to this section"){.anchor} {#Kamaelia}
---------------------------------------------------------------------------------------------------

Kamaelia is a library of complex components for [[all kind of tasks and
topics]{.icon}](http://kamaelia.sourceforge.net/Components){.ext-link}:

For example taking the previous example we could write:

> ::: {.code}
>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>
>     Pipeline(
>              ConsoleReader(),
>              MyComponent(),
>              ConsoleEchoer(),
>     ).run()
> :::

[[Pipeline]{.icon}](http://kamaelia.sourceforge.net/Components/pydoc/Kamaelia.Experimental.Chassis.Pipeline.html){.ext-link}
is component that automatically links outboxes to inboxes of each
provided component. The console components allow for reading and writing
data from and to the command line. Because `Pipeline` is also a
component itself it could in turns be used in another component.

Note that calling the `run()` method on a component blocks the process
until it is killed. You can also simply activate a component which will
then be in an active state but will run only when eventually `run` is
called on another component. In other words, the previous snippet could
also be written like that:

> ::: {.code}
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>
>     reader = ConsoleReader()
>     reader.activate()
>
>     mycomp = MyComponent()
>     mycomp.link((reader, 'outbox'), (mycomp, 'inbox'))
>     mycomp.activate()
>
>     writer = ConsoleEchoer()
>     mycomp.link((mycomp, 'outbox'), (writer, 'inbox'))
>
>     writer.run()
> :::

Now that you have the basics of Kamaelia you should dive into its
[[documentation]{.icon}](http://kamaelia.sourceforge.net/Cookbook.html){.ext-link}
and have fun with its fantastic library.
:::
:::
