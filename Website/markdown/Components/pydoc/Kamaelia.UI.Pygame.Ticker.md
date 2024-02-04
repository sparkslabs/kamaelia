---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Ticker
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.html){.reference}
===================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.Ticker.html){.reference}**
:::

-   [Pygame text \'Ticker\'](#389){.reference}
    -   [Example Usage](#390){.reference}
    -   [How does it work?](#391){.reference}
:::

::: {.section}
Pygame text \'Ticker\' {#389}
======================

Displays text in pygame a word at a time as a \'ticker\'.

NOTE: This component is very much a work in progress. Its capabilities
and API is likely to change substantially in the near future.

::: {.section}
[Example Usage]{#example-usage} {#390}
-------------------------------

Ticker displaying text from a file:

``` {.literal-block}
Pipeline( RateControlledFileReader("textfile","lines",rate=1000),
          Ticker(position=(100,100))
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#391}
--------------------------------------

The component requests a display surface from the Pygame Display service
component. This is used as the ticker.

Send strings containing *lines of text* to the Ticker component. Do not
send strings with words split between one string and the next. It
displays the words as a \'ticker\' one word at a time. Text is
automatically wrapped from one line to the next. Once the bottom of the
ticker is reached, the text automatically jump-scrolls up a line to make
more room.

The text is normalised by the ticker. Multiple spaces between words are
collapsed to a single space. Linefeeds are ignored.

NOTE: 2 consecutive linefeeds currently results in a special message
being sent out of the \"\_displaysignal\" outbox. This is
work-in-progress aimed at new features. It is only documented here for
completeness and should not be relied upon.

You can set the text size, colour and line spacing. You can also set the
background colour, outline (border) colour and width. You can also
specify the size and position of the ticker

NOTE: Specifying the outline width currently does not work for any value
other than 1.

NOTE: Specify the size of the ticker with the render\_right and
render\_bottom arguments. Specifying render\_left and render\_top
arguments with values other than 1 results in parts of the ticker being
obscured.

The ticker displays words at a constant rate - it self regulates its
display speed.

Whilst it is running, sending any message to the \"pausebox\" inbox will
pause the Ticker. It will continue to buffer incoming text. Any message
sent to the \"unpausebox\" inbox will cause the Ticker to resume.

Whilst running, you can change the transparency of the ticker by sending
a value to the \"alphacontrol\" inbox between 0 (fully transparent) and
255 (fully opaque) inclusive.

If a producerFinished message is received on the \"control\" inbox, this
component will send its own producerFinished message to the \"signal\"
outbox and will terminate.

However, if the ticker is paused (message sent to \"pausebox\" inbox)
then the component will ignore messages on its \"control\" inbox until
it is unpaused by sending a message to its \"unpausebox\" inbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.html){.reference}.[Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.Ticker.html){.reference}
=================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Ticker([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Ticker}
----------------------------------------------------------------------------------------------

Ticker(\...) -\> new Ticker component.

A pygame based component that displays incoming text as a ticker.

Keyword arguments (all optional):

-   text\_height \-- Font size in points (default=39)
-   line\_spacing \-- (default=text\_height/7)
-   background\_colour \-- (r,g,b) background colour of the ticker
    (default=(128,48,128))
-   text\_colour \-- (r,g,b) colour of text (default=(232,232,48))
-   outline\_colour \-- (r,g,b) colour of the outline border
    (default=background\_colour)
-   outline\_width \-- pixels width of the border (default=1)
-   position \-- (x,y) pixels location of the top left corner
-   render\_left \-- pixels distance of left of text from left edge
    (default=1)
-   render\_top \-- pixels distance of top of text from top edge
    (default=1)
-   render\_right \-- pixels width of ticker (default=399)
-   render\_bottom \-- pixels height of ticker (default=299)

NOTE: render\_left and render\_top currently behave incorrectly if not
set to 1

::: {.section}
### [Inboxes]{#symbol-Ticker.Inboxes}

-   **control** : NOT USED (yet)
-   **\_displaycontrol** : Shutdown messages & feedback from Pygame
    Display service
-   **unpausebox** : Any message unpauses the ticker
-   **pausebox** : Any message pauses the ticker
-   **inbox** : Specify (new) filename
-   **alphacontrol** : Transparency of the ticker (0=fully transparent,
    255=fully opaque)
:::

::: {.section}
### [Outboxes]{#symbol-Ticker.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED (yet)
-   **\_displaysignal** : Shutdown signalling & sending requests to
    Pygame Display service
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Ticker.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [clearDisplay(self)]{#symbol-Ticker.clearDisplay}

Clears the ticker of any existing text.
:::

::: {.section}
#### [handleAlpha(self)]{#symbol-Ticker.handleAlpha}
:::

::: {.section}
#### [main(self)]{#symbol-Ticker.main}

Main loop.
:::

::: {.section}
#### [renderBorder(self, display)]{#symbol-Ticker.renderBorder}

Draws a rectangle to form the \'border\' of the ticker
:::

::: {.section}
#### [requestDisplay(self, \*\*argd)]{#symbol-Ticker.requestDisplay}

Generator. Gets a display surface from the Pygame Display service.

Makes the request, then yields 1 until a display surface is returned.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-Ticker.waitBox}

Generator. yields 1 until data ready on the named inbox.
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

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
