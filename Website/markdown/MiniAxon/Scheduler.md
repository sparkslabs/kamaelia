---
pagename: MiniAxon/Scheduler
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[]{#Scheduler}[2. Scheduler - A means of running lots of
microprocesses]{style="font-size:14pt;font-weight:600"}

[Exercise: ]{style="font-weight:600"}Write a class called
[scheduler]{style="font-family:Courier;font-weight:600"} with the
following characteristics.

-   It should subclass microprocess.

Objects created shold have the following attributes:

-   [self.active]{style="font-family:Courier"} - this is a list.
    (initially empty)
-   [self.newqueue]{style="font-family:Courier"} - this is also a list.
    (initially empty)\
    [Hint: ]{style="font-weight:600"}Initialise these in the
    \_\_init\_\_ method!

Objects created should have the following methods:

[\_\_init\_\_(self)]{style="font-family:Courier"} - Perform any
initialisation you need here (see above)\
[Remember: ]{style="font-weight:600"}Don\'t forget to called your super
class\'s \_\_init\_\_ method!

[main(self) ]{style="font-family:Courier"}- Takes no arguments\
This should be a generator with the following logic: (Looped 100 times)

Loop through all the objects in self.active using any mechanism you
choose.

-   IMMEDIATELY YIELD CONTROL HERE WITH a \"non -1 value\"
-   Suppose you call the current object (from self.active) current
-   Call current.next()
-   If a StopIteration exception is thrown, just catch and skip on to
    the next iteration. (eg continue)
-   If the result from current.next() was NOT -1, then append current
    onto self.newqueue

Having looped through all the objects, REPLACE self.active with
self.newqueue, and replace the value of self.newqueue with a new empty
list

[activateMicroprocess(self, someprocess)]{style="font-family:Courier"}

-   someprocess is a microprocess object (or anything that conforms to
    the same interface/behaviour seen by the scheduler).
-   This method should call the object\'s main method and append the
    result to self.newqueue

**[Answer Hidden](/MiniAxon/Scheduler?template=veryplain)**

**[Show Answer](/MiniAxon/Scheduler?template=veryplain&sat=2)**

[Answer:]{style="font-weight:600"}

-   Select from the above tabs to show the answer!

[Discussion:]{style="font-weight:600"}

This class provides us with a rudimentary way of activating generators
embedded inside a class, adding them to a runqueue and then letting
something run them. So let\'s try it. The default microprocess is
relatively boring, so let\'s create some microprocesses that are little
more than an age old program that repeatedly displays a messae. To do
that we declare a class subclassing microprocess and provide a generator
called main. We\'ll also capture a provided argument:

Note that this generator doesn\'t ever exit. We can then create a couple
of these printers:

Next we can create a scheduler:

We can then ask this scheduler to activate the two microprocesses - X &
Y :

We can then run our scheduler by iterating through its main method:

If we run this we get the following output (middle of output snipped):

As you can see, the scheduler hits the 100th iteration and then halts.
