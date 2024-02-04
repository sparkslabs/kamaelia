---
pagename: MiniAxon/Component
last-modified-date: 2008-10-28
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[4[]{#Component} Simple Component - Microprocesses with standard
external interfaces]{style="font-size: 14pt; font-weight: 600;"}

[Exercise: ]{style="font-weight: 600;"} Write a class called
[component]{style="font-family: Courier; font-weight: 600;"} that
subclasses [microprocess]{style="font-family: Courier;"} with the
following\...

Attributes:

[self.boxes]{style="font-family: Courier;"} - this should be a
dictionary of the following form:

<div>

Clearly this allows for more inboxes and outboxes, but at this stage
we\'ll keep things simple.

</div>

Behaviour: (methods)

As before an [\_\_init\_\_]{style="font-family: Courier;"} for anything
you need (eg attributes above :)\

[send(self, value, boxname)]{style="font-family: Courier;"}

This method takes the value and appends it to the end of the list
associated with the boxname.

That is if I do:

::: {dir="ltr"}
:::

::: {dir="ltr"}
Then given the suggested implementation of boxes above the following
should be true afterwards:
:::

::: {dir="ltr"}
:::

::: {dir="ltr"}
ie the last value in the list associated with the boxname is the value
we sent to that outbox. More explicitly, if the value of self.boxes was
this beforehand:
:::

::: {dir="ltr"}
:::

::: {dir="ltr"}
And the following call had been made:
:::

::: {dir="ltr"}
:::

::: {dir="ltr"}
The self.boxes would look like this afterwards:
:::

<div>

</div>

[recv(self, boxname)]{style="font-family: Courier;"}

This is the logical opposite of sending. Rather than appending a value
at the end of the send queue, we take the first value in the queue.

Behaviourally, given a starting value of self.boxes:

::: {dir="ltr"}
Then I would expect the following behaviour code\....
:::

::: {dir="ltr"}
\... to display the following sort of behaviour:
:::

::: {dir="ltr"}
:::

::: {dir="ltr"}
The value of self.boxes should also change as follows after each call:
:::

::: {dir="ltr"}
:::

[dataReady(self, boxname)]{style="font-family: Courier;"}

This should return the length of the list associated with the boxname.\
\
For example, given:

<div>

</div>

<div>

The following behaviour is expected:

</div>

**[Answer Hidden](/MiniAxon/Component?template=veryplain)**

**[Show Answer](/MiniAxon/Component?template=veryplain&cat=2)**

[Answer:]{style="font-weight:600"}

-   Select from the above tabs to show the answer!

[Discussion:]{style="font-weight: 600;"}

Ok that\'s a fairly long description, but a fairly simple
implementation. So what\'s this done? It\'s enabled us to send data to a
running generator and receive data back. We\'re not worried what the
generator is doing at any point in time, and so the communications
between us and the generator (or between generators) is asynchronous.

An extension to the suggested \_\_init\_\_ is to do the following:

This small extension means that classes subclassing
[component]{style="font-family: Courier;"} can have a different set of
inboxes and outboxes. For example:

That said, components by themselves are relatively boring. Unless we
have some way of moving the data between generators we haven\'t gained
anything (really) beyond the printer example above. So we need
someone/something that can move data/messages from outboxes and deliver
to inboxes\...
