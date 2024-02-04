---
pagename: Docs/Axon/Axon.STM
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}
------------------------------------------------------------------------------------
:::
:::

::: {.section}
STM
===

::: {.container}
-   **class
    [BusyRetry](/Docs/Axon/Axon.STM.BusyRetry.html){.reference}**
-   **class
    [Collection](/Docs/Axon/Axon.STM.Collection.html){.reference}**
-   **class
    [ConcurrentUpdate](/Docs/Axon/Axon.STM.ConcurrentUpdate.html){.reference}**
-   **class [Store](/Docs/Axon/Axon.STM.Store.html){.reference}**
-   **class [Value](/Docs/Axon/Axon.STM.Value.html){.reference}**
:::

-   [What IS it?](#52){.reference}
-   [Why is it useful?](#53){.reference}
-   [Using It](#54){.reference}
    -   [Accessing/Updating a single shared value in the
        store](#55){.reference}
    -   [Accessing/Updating a collection of shared values in the
        store](#56){.reference}
-   [What can (possibly) go wrong?](#57){.reference}
:::

::: {.section}
Support for basic in-process software transactional memory.

::: {.section}
[What IS it?]{#what-is-it} {#52}
--------------------------

Software Transactional Memory (STM) is a technique for allowing multiple
threads to share data in such a way that they know when something has
gone wrong. It\'s been used in databases (just called transactions there
really) for some time and is also very similar to version control.
Indeed, you can think of STM as being like variable level version
control.
:::

::: {.section}
[Why is it useful?]{#why-is-it-useful} {#53}
--------------------------------------

Why do you need it? Well, in normal code, Global variables are generally
shunned because it can make your code a pain to work with and a pain to
be certain if it works properly. Even with linear code, you can have 2
bits of code manipulating a structure in surprising ways - but the
results are repeatable. Not-properly-managed-shared-data is to threaded
systems as not-properly-managed-globals are to normal code. (This code
is one way of helping manage shared data)

Well, with code where you have multiple threads active, having shared
data is like an even nastier version of globals. Why? Well, when you
have 2 (or more) running in parallel, the results of breakage can become
hard to repeat as two pieces of code \"race\" to update values.

With STM you make it explicit what the values are you want to update,
and only once you\'re happy with the updates do you publish them back to
the shared storage. The neat thing is, if someone else changed things
since you last looked, you get told (your commit fails), and you have to
redo the work. This may sound like extra work (you have to be prepared
to redo the work), but it\'s nicer than your code breaking :-)

The way you get that message is the .commit raises a ConcurrentUpdate
exception.

Also, it\'s designed to work happily in code that requires non-blocking
usage - which means you may also get a BusyRetry exception under load.
If you do, you should as the exception suggests retry the action that
you just tried. (With or without restarting the transaction)

Apologies if that sounds too noddy :)
:::

::: {.section}
[Using It]{#using-it} {#54}
---------------------

::: {.section}
### [Accessing/Updating a single shared value in the store]{#accessing-updating-a-single-shared-value-in-the-store} {#55}

You can have many single vars in a store of course\... If they\'re
related though or updated as a group, see the next section:

``` {.literal-block}
from Axon.STM import Store

S = Store()
greeting = S.usevar("hello")
print repr(greeting.value)
greeting.set("Hello World")
greeting.commit()
```
:::

::: {.section}
### [Accessing/Updating a collection of shared values in the store]{#accessing-updating-a-collection-of-shared-values-in-the-store} {#56}

Likewise you can use as many collections of values from the store as you
like:

``` {.literal-block}
from Axon.STM import Store

S = Store()
D = S.using("account_one", "account_two", "myaccount")
D["account_one"].set(50)
D["account_two"].set(100)
D.commit()
S.dump()

D = S.using("account_one", "account_two", "myaccount")
D["myaccount"].set(D["account_one"].value+D["account_two"].value)
D["account_one"].set(0)
D["account_two"].set(0)
D.commit()
S.dump()
```
:::
:::

::: {.section}
[What can (possibly) go wrong?]{#what-can-possibly-go-wrong} {#57}
------------------------------------------------------------

You can have 2 people trying to update the same values at once. An
example of this would be - suppose you have the following commands being
executed by 2 threads with this mix of commands:

``` {.literal-block}
S = Store()
D = S.using("account_one", "account_two", "myaccount")
D["myaccount"].set(0)
D["account_one"].set(50)
D["account_two"].set(100)
D.commit() # 1
S.dump()

D = S.using("account_one", "account_two", "myaccount")
D["myaccount"].set(D["account_one"].value+D["account_two"].value)
E = S.using("account_one", "myaccount")
E["myaccount"].set(E["myaccount"].value-100)
E["account_one"].set(100)
E.commit() # 2
D["account_one"].set(0)
D["account_two"].set(0)
D.commit() # 3 - should fail
S.dump()
```

You do actually want this to fail because you have concurrent updates.
This will fail on the third commit, and fail by throwing a
ConcurrentUpdate exception. If you get this, you should redo the
transaction.

The other is where there\'s lots of updates happening at once. Rather
than the code waiting until it acquires a lock, it is possible for
either the .using, .usevar or .commit methods to fail with a BusyRetry
exception. This means exactly what it says on the tin - the system was
busy & you need to retry. In this case you do not have to redo the
transaction. This is hard to replicate except under load. The reason we
do this however is because most Kamaelia components are implemented as
generators, which makes blocking operation ( as a .acquire() rather than
.acquire(0) would be) an expensive operation.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[BusyRetry](/Docs/Axon/Axon.STM.BusyRetry.html){.reference}
================================================================================================================================================

::: {.section}
class BusyRetry(Exception) {#symbol-BusyRetry}
--------------------------

::: {.section}
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[Collection](/Docs/Axon/Axon.STM.Collection.html){.reference}
==================================================================================================================================================

::: {.section}
class Collection(dict) {#symbol-Collection}
----------------------

::: {.section}
Collection() -\> new Collection dict

A dictionary which belongs to a thread-safe store

Again, you do not instantiate these yourself
:::

::: {.section}
### Methods defined here

::: {.section}
#### [commit(self)]{#symbol-Collection.commit}

Commit new versions of the collection\'s items to the store
:::

::: {.section}
#### [set\_store(self, store)]{#symbol-Collection.set_store}

Set the store to associate the collection with
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[ConcurrentUpdate](/Docs/Axon/Axon.STM.ConcurrentUpdate.html){.reference}
==============================================================================================================================================================

::: {.section}
class ConcurrentUpdate(Exception) {#symbol-ConcurrentUpdate}
---------------------------------

::: {.section}
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[Store](/Docs/Axon/Axon.STM.Store.html){.reference}
========================================================================================================================================

::: {.section}
class Store(object) {#symbol-Store}
-------------------

::: {.section}
Store() -\> new Store object

A thread-safe versioning store for key-value pairs

You instantiate this as per the documentation for this module
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_can\_update(self, key, value)]{#symbol-Store.__can_update}

Returns true if a value can be safely updated. Potentially not
thread-safe
:::

::: {.section}
#### [\_\_do\_update(self, key, value)]{#symbol-Store.__do_update}

Update a key-value pair and increment the version. Not thread-safe
:::

::: {.section}
#### [\_\_get(self, key)]{#symbol-Store.__get}

Retreive a value. Returns a clone of the Value. Not thread-safe.
:::

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-Store.__init__}
:::

::: {.section}
#### [\_\_make(self, key)]{#symbol-Store.__make}

Create a new key-value pair. Not thread-safe
:::

::: {.section}
#### [dump(self)]{#symbol-Store.dump}
:::

::: {.section}
#### [set(self, key, value)]{#symbol-Store.set}

Tries to update a value in the store. If the store is already in use a
BusyRetry error is raised. If the value has been updated by another
thread a ConcurrentUpdate error is raised
:::

::: {.section}
#### [set\_values(self, D)]{#symbol-Store.set_values}

Tries to update a selection of values in the store. If the store is
already in use a BusyRetry error is raised. If one of the values has
been updated by another thread a ConcurrentUpdate error is raised.
:::

::: {.section}
#### [usevar(self, key\[, islocked\])]{#symbol-Store.usevar}

Tries to get an item from the store. Returns the requested Value object.
If the store is already in use a BusyRetry error is raised.
:::

::: {.section}
#### [using(self, \*keys)]{#symbol-Store.using}

Tries to get a selection of items from the store. Returns a Collection
dictionary containing the requested values. If the store is already in
use a BusyRetry error is raised.
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[Value](/Docs/Axon/Axon.STM.Value.html){.reference}
========================================================================================================================================

::: {.section}
class Value(object) {#symbol-Value}
-------------------

::: {.section}
Value(version, value, store, key) -\> new Value object

A simple versioned key-value pair which belongs to a thread-safe store

Arguments:

-   version \-- the initial version of the value
-   value \-- the object\'s initial value
-   store \-- a Store object to hold the value and it\'s history
-   key \-- a key to refer to the value

Note: You do not instantiate these - the Store does that
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, version, value, store, key)]{#symbol-Value.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_\_repr\_\_(self)]{#symbol-Value.__repr__}
:::

::: {.section}
#### [clone(self)]{#symbol-Value.clone}

Returns a clone of the value
:::

::: {.section}
#### [commit(self)]{#symbol-Value.commit}

Commit a new version of the value to the store
:::

::: {.section}
#### [set(self, value)]{#symbol-Value.set}

Set the value without storing
:::
:::

::: {.section}
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
