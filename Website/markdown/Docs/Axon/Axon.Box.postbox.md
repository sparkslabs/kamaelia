---
pagename: Docs/Axon/Axon.Box.postbox
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[postbox](/Docs/Axon/Axon.Box.postbox.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Box.html){.reference}

------------------------------------------------------------------------

::: {.section}
class postbox(object) {#symbol-postbox}
---------------------

::: {.section}
postbox(storage\[,notify\]) -\> new postbox object.

Creates a postbox, using the specified storage as default storage.
Storage should have the interface of list objects.

Also takes optional notify callback, that will be called whenever an
item is taken out of a postbox further down the chain.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, storage\[, notify\])]{#symbol-postbox.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [\_\_len\_\_(self)]{#symbol-postbox.__len__}

Returns number of items in the postbox
:::

::: {.section}
#### [\_\_repr\_\_(self)]{#symbol-postbox.__repr__}
:::

::: {.section}
#### [\_addnotifys(self, newnotifys)]{#symbol-postbox._addnotifys}

Updates the local storage\'s list of notification callbacks for when
messages are taken out of inboxes. Then recurses this info to this
postbox\'s target, so it can update too.
:::

::: {.section}
#### [\_removenotifys(self, oldnotifys)]{#symbol-postbox._removenotifys}

Updates the local storage\'s list of notification callbacks for when
messages are taken out of inboxes. Then recurses this info to this
postbox\'s target, so it can update too.
:::

::: {.section}
#### [\_retarget(self\[, newtarget\])]{#symbol-postbox._retarget}

retarget(\[newtarget\]) aims requests at to this postbox at a different
target.

If newtarget is unspecified or None, target is default local storage.
:::

::: {.section}
#### [addsource(self, newsource)]{#symbol-postbox.addsource}

addsource(newsource) registers newsource as a source and tells it to
\'retarget\' at this postbox.

Also finds out from the new source who wants to be notified when
messages are taken out of postboxes, and updates records accordingly,
and passes this info further down the chain of linkages.

Raises
[Axon.AxonExceptions.BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
if the newsource is already targetted at a destination. This is because
Axon does not support one-to-many arrangements.
:::

::: {.section}
#### [getSize(self)]{#symbol-postbox.getSize}

Gets current box size limit
:::

::: {.section}
#### [getnotifys(self)]{#symbol-postbox.getnotifys}

Returns list of all callbacks that should be made when messages are
collected from a postbox using this one as a source.

The list returned is effectively all callbacks this postbox would have
to make *plus* the callback for the owner of this box (if there is one)
:::

::: {.section}
#### [isFull(self)]{#symbol-postbox.isFull}

Returns True if the destination box is full (and has a size limit)
:::

::: {.section}
#### [removesource(self, oldsource)]{#symbol-postbox.removesource}

removesource(oldsource) deregisters oldsource as a source and tells it
to \'retarget\' at None (nothing).

Also finds out from the old source who was being notified when messages
are taken out of postboxes, and updates records accordingly, and passes
this info further down the chain of linkages.
:::

::: {.section}
#### [setShowTransit(self\[, showtransit\]\[, tag\])]{#symbol-postbox.setShowTransit}

Set showTransit to True to cause debugging output whenever a message is
delivered to this postbox. The tag can be anything you want to identify
this occurrence.
:::

::: {.section}
#### [setSize(self, size)]{#symbol-postbox.setSize}

Set box size limit (use None for no limit)

Behaviour is undefined (and not recommended!) if this call is made
whilst there may be items in the postbox!
:::
:::

::: {.section}
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
