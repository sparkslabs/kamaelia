---
pagename: Cookbook/Graphlines
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Graphlines
=====================

A Graphline provides a flexible way to link inboxes and outboxes in any
way you wish. Whereas a Pipeline constrains your components to be wired
into \... a pipeline \... with Graphline you specify each link
explicitly.

Suppose we want to build a simple slideshow application, where pygame
Button components control a Chooser component that sends filenames for
each slide to a pygame Image display component:

![](/images/graphline1_idea.gif)

We could build this by writing a new component with a whole bunch of
self.link() calls to link each outbox to the next inbox. But that is a
lot of code to write and rather tedious! \... surely there must be an
easier way?\
\
\... You need the graphline component! No need to write a whole new
component, simply use a Graphline component like this:

``` {style="margin-left: 40px;"}
from Kamaelia.Chassis.Graphline import Graphline

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Util.Chooser import Chooser

files = [ "slide1.gif", "slide2.gif", .... "slide99.gif" ]

Graphline(
     CHOOSER  = Chooser(files),
     IMAGE    = Image(size=(800,600), position=(8,48)),
     NEXT     = Button(caption="Next",     msg="NEXT", position=(72,8)  ),
     PREVIOUS = Button(caption="Previous", msg="PREV" ,position=(8,8)   ),
     FIRST    = Button(caption="First",    msg="FIRST",position=(256,8) ),
     LAST     = Button(caption="Last",     msg="LAST" ,position=(320,8) ),

     linkages = {
        ("NEXT",     "outbox") : ("CHOOSER", "inbox"),
        ("PREVIOUS", "outbox") : ("CHOOSER", "inbox"),
        ("FIRST",    "outbox") : ("CHOOSER", "inbox"),
        ("LAST",     "outbox") : ("CHOOSER", "inbox"),

        ("CHOOSER",  "outbox") : ("IMAGE",   "inbox"),
     }
).run()
```

What you see here is slightly abridged for clarity. You can find the
full version in ` Kamaelia/Examples/SimpleGraphicalApps/Slideshows `

What did we just do? Simple:

1.  Write each component as a named argument\

    ``` {style="margin-left: 40px;"}
         CHOOSER  = Chooser(files),
         IMAGE    = Image(size=(800,600), position=(8,48)),
         NEXT     = Button(caption="Next",     msg="NEXT", position=(72,8)  ),
         PREVIOUS = Button(caption="Previous", msg="PREV" ,position=(8,8)   ),
         FIRST    = Button(caption="First",    msg="FIRST",position=(256,8) ),
         LAST     = Button(caption="Last",     msg="LAST" ,position=(320,8) ),
    ```

    \

2.  \...then write the linkages you want as the \'linkages\' argument in
    a dictionary:\

    ``` {style="margin-left: 40px;"}
         linkages = {
            ("NEXT",     "outbox") : ("CHOOSER", "inbox"),
            ("PREVIOUS", "outbox") : ("CHOOSER", "inbox"),
            ("FIRST",    "outbox") : ("CHOOSER", "inbox"),
            ("LAST",     "outbox") : ("CHOOSER", "inbox"),

            ("CHOOSER",  "outbox") : ("IMAGE",   "inbox"),
         }
    ```

For each linkage we want, we write a mapping in the dictionary from a
(component, outbox) to a (component, inbox) We refer to the components
by the names we just gave them, as strings. We reference the inboxes and
outboxes by their names too.

So, for example:\

``` {style="margin-left: 40px;"}
("NEXT","outbox") : ("CHOOSER","inbox")
```

specifies that you want the \"outbox\" outbox of the \"Next\" Button to
be linked to the \"inbox\" inbox of the Chooser.\
\

### Making links to the outside world 

So the Graphline defined above wires up the Chooser, Image and 4 Button
components inside itself - like Pipeline it is a kind of container:\

::: {align="center"}
![](/images/graphline1_intention.gif)\
:::

\
If we look in more detail, the links made are actually like this:\
\

::: {style="text-align: center;"}
![A diagram showing how the components inside the example graphline are
linked up](../../../images/graphline1_inside.gif)
:::

\
Just like the Pipeline component, a Graphline has its own inboxes and
outboxes. You can specify links to and from these by using the empty
string to name the component.\
\
For example, we might want to be able to send instructions to the
Chooser from outside this graphline, in which case we would add this to
the set of linkages:\

``` {style="margin-left: 40px;"}
        ("", "inbox") : ("NEXT", "inbox"),
```

By using a name for a component that we\'ve not used (in this case
simply the empty string suffices) we\'re telling Graphline to use its
own inbox.\
\
We could do the same for outboxes too if we want. For example, we could
ask for the outbox of the Image component to be linked to the
Graphline\'s outbox:\

``` {style="margin-left: 40px;"}
        ("IMAGE", "outbox") : ("",     "outbox"),
```

In fact, if you also refer to an inbox or outbox name for the Graphline
that does not exist. Graphline will simply create it. This means you can
use a Graphline as a container, giving it whatever inboxes and outboxes
you need - not just the \'standard\' ones that most components have.\
\
Just like with Pipeline, Graphline is a fully fledged component itself,
so you can put a Graphline inside a Pipeline, or a Pipeline inside a
Graphline, or any other combination you care to choose. Again, it can be
a good way of making your system more modular, by separating off a
little group of components into a separate functional unit.\
