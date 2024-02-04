---
pagename: STM
last-modified-date: 2008-10-19
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Axon: STM
=========

### Software Transactional Memory {#software-transactional-memory align="right"}

Support for basic in-process software transactional memory has been
added to Axon - Kamaelia\'s core. The API chosen is the simplest that
that seems minimally sufficient. As well as being added to mainline Axon
(for enhancing the CAT later), it is also packaged up a standalone
package since it\'s likely to be useful in its own right.\

Getting it
----------

You can download the release version here:\

> <http://thwackety.com/Axon.STM-1.0.1.tar.gz>

Previewing it
-------------

You can look at the sourcecode online here:\

> <https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private_MPS_Scratch/Bindings/STM/Axon/STM.py>\

Installing it
-------------

>     ~ > tar zxf Axon.STM-1.0.1.tar.gz
>     ~ > cd Axon.STM-1.0.1/
>     ~ > sudo python setup.py install

What IS it?
-----------

Software Transactional Memory (STM) is a technique for allowing multiple
threads to share data in such a way that they know when something has
gone wrong. It\'s been used in databases (just called transactions there
really) for some time and is also very similar to version control.
Indeed, you can think of STM as being like variable level version
control.

Note: Because this is NOT intended to be persistent, this is not an ACID
store because it doesn\'t support the D - durability across a crash.
(after all, we don\'t save the state to disk) (The other aspects
atomicity, consistency & isolation are supported though)

I\'ve written this to allow a part of Kamaelia to share & manage a
dictionary of atomic values simply, and as a result this code is also
going into mainline Kamaelia. (Specifically into Axon Kamaelia\'s core)

However STM is something that should hopefully be of use to others doing
concurrent *things* whether or not they\'re using kamaelia, hence this
stand alone release.

This stand alone release should \*not\* be used alongside mainline Axon
yet. (Well you can, as long as you reinstall your Axon over the top, but
that\'s icky :-)

Why is it useful?
-----------------

> *please skip this (or correct me :) if you understand concurrency
> already :-)*\

Why do you need it? Well, in normal code, Global variables are generally
shunned because it can make your code a pain to work with and a pain to
be certain if it works properly. Even with linear code, you can have 2
bits of code manipulating a structure in surprising ways - but the
results are repeatable. Not-properly-managed-shared-data is to threaded
systems as not-properly-managed-globals are to normal code. (This code
is one way of helping manage shared data)\
\
Well, with code where you have multiple threads active, having shared
data is like an even nastier version of globals. Why? Well, when you
have 2 (or more) running in parallel, the results of breakage can become
hard to repeat as two pieces of code \"race\" to update values.\
\
With STM you make it explicit what the values are you want to update,
and only once you\'re happy with the updates do you publish them back to
the shared storage. The neat thing is, if someone else changed things
since you last looked, you get told (your commit fails), and you have to
redo the work. This may sound like extra work (you have to be prepared
to redo the work), but it\'s nicer than your code breaking :-)\
\
The way you get that message is the .commit raises a
**ConcurrentUpdate** exception.\
\
Also, it\'s designed to work happily in code that requires non-blocking
usage - which means you may also get a **BusyRetry** exception under
load. If you do, you should as the exception suggests retry the action
that you just tried. (With or without restarting the transaction)\
\
Apologies if that sounds too noddy :)\

Using It
--------

### Accessing/Updating a single shared value in the store

You can have many single vars in a store of course\... If they\'re
related though or updated as a group, see the next section.\

>     from Axon.STM import Store
>
>     S = Store()
>     greeting = S.usevar("hello")
>     print repr(greeting.value)
>     greeting.set("Hello World")
>     greeting.commit()

### Accessing/Updating a collection of shared values in the store

Likewise you can use as many collections of values from the store as you
like.\

>     from Axon.STM import Store
>
>     S = Store()
>     D = S.using("account_one", "account_two", "myaccount")
>     D["account_one"].set(50)
>     D["account_two"].set(100)
>     D.commit()
>     S.dump()
>
>     D = S.using("account_one", "account_two", "myaccount")
>     D["myaccount"].set(D["account_one"].value+D["account_two"].value)
>     D["account_one"].set(0)
>     D["account_two"].set(0)
>     D.commit()
>     S.dump()

What can (possibly) go wrong?
-----------------------------

You can have 2 people trying to update the same values at once. An
example of this would be - suppose you have the following commands being
executed by 2 threads with this mix of commands:\

>     S = Store()
>     D = S.using("account_one", "account_two", "myaccount")
>     D["myaccount"].set(0)
>     D["account_one"].set(50)
>     D["account_two"].set(100)
>     D.commit() # 1
>     S.dump()
>
>     D = S.using("account_one", "account_two", "myaccount")
>     D["myaccount"].set(D["account_one"].value+D["account_two"].value)
>     E = S.using("account_one", "myaccount")
>     E["myaccount"].set(E["myaccount"].value-100)
>     E["account_one"].set(100)
>     E.commit() # 2
>     D["account_one"].set(0)
>     D["account_two"].set(0)
>     D.commit() # 3 - should fail
>     S.dump()

You do actually want this to fail because you have concurrent updates.
This will fail on the third commit, and fail by throwing a
**ConcurrentUpdate** exception. If you get this, you should redo the
transaction.\
\
The other is where there\'s lots of updates happening at once. Rather
than the code waiting until it acquires a lock, it is possible for
either the .using, .usevar or .commit methods to fail with a
**BusyRetry** exception. This means exactly what it says on the tin -
the system was busy & you need to retry. In this case you do **not**
have to redo the transaction. This is hard to replicate except under
load. The reason we do this however is because most Kamaelia components
are implemented as generators, which makes blocking operation ( as a
.acquire() rather than .acquire(0) would be) an expensive operation.\

Possible Extensions
-------------------

It\'d be fun to use this in pypy (say) to extend python such that the
latter example could become something like this:\

>     atomically using account_one, account_two:
>        account_one = 50
>        account_two = 100
>
>
>     atomically using account_one, account_two, myaccount:
>         myaccount = account_one + account_two
>         account_one = 0
>         account_two = 0

However that\'s out of scope really for this module here at present. (or
at least me with the amount of time I have right now!) This module could
be used to implement the above semantics though. *(Oh, note: I\'m not
even vaguely suggesting this as a modification to core python - it\'s
just the sort of thing that strikes me as a fun thing to do :-)*\

Feedback
--------

Feedback is very welcome, preferably via email to
<kamaelia-list@lists.sourceforge.net>\
\
Michael Sparks\
\

::: {#__ss_599591 style="width:425px;text-align:left"}
[Sharing Data and Services Safely in Concurrent Systems using
Kamaelia](http://www.slideshare.net/kamaelian/sharing-data-and-services-safely-in-concurrent-systems-using-kamaelia-presentation?type=powerpoint "Sharing Data and Services Safely in Concurrent Systems using Kamaelia")

::: {style="font-size:11px;font-family:tahoma,arial;height:26px;padding-top:2px;"}
View SlideShare
[presentation](http://www.slideshare.net/kamaelian/sharing-data-and-services-safely-in-concurrent-systems-using-kamaelia-presentation?type=powerpoint "View Sharing Data and Services Safely in Concurrent Systems using Kamaelia on SlideShare")
or [Upload](http://www.slideshare.net/upload?type=powerpoint) your own.
(tags: [pyconuk](http://slideshare.net/tag/pyconuk)
[kamaelia](http://slideshare.net/tag/kamaelia))
:::
:::
