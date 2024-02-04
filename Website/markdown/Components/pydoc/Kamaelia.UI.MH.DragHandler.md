---
pagename: Components/pydoc/Kamaelia.UI.MH.DragHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[MH](/Components/pydoc/Kamaelia.UI.MH.html){.reference}.[DragHandler](/Components/pydoc/Kamaelia.UI.MH.DragHandler.html){.reference}
=================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Pygame \'drag\' event Handler](#355){.reference}
    -   [Example Usage](#356){.reference}
    -   [How does it work?](#357){.reference}
:::

::: {.section}
Pygame \'drag\' event Handler {#355}
=============================

A class, to implement \"click and hold\" dragging operations in pygame.
Hooks into the event dispatch mechanism provided by the PyGameApp
component.

Subclass this class to implement your required dragging functionality.

::: {.section}
[Example Usage]{#example-usage} {#356}
-------------------------------

A set of circles that can be dragged around the pygame window:

``` {.literal-block}
class Circle(object):
    def __init__(self, x, y, radius):
        self.x, self.y, self.radius = x, y, radius

    def draw(self, surface):
        pygame.draw.circle(surface, (255,128,128), (self.x, self.y), self.radius)


class CircleDragHandler(DragHandler):
    def __init__(self, event, app, theCircle):
        self.circle = theCircle
        super(CircleDragHandler,self).__init__(event, app)

    def detect(self, pos, button):
        if (pos[0] - self.circle.x)**2 + (pos[1] - self.circle.y)**2 < (self.circle.radius**2):
            return (self.circle.x, self.circle.y)
        return False

    def drag(self,newx,newy):
        self.circle.x = newx
        self.circle.y = newy

    def release(self,newx, newy):
        self.drag(newx, newy)


class DraggableCirclesApp(PyGameApp):

    def initialiseComponent(self):
        self.circles = []
        for i in range(100,200,20):
            circle = Circle(i, 2*i, 20)
            self.circles.append(circle)
            handler = lambda event, circle=circle : CircleDragHandler.handle(event, self, circle)
            self.addHandler(MOUSEBUTTONDOWN, handler)


    def mainLoop(self):
        self.screen.fill( (255,255,255) )
        for circle in self.circles:
            circle.draw(self.screen)
        return 1

DraggableCirclesApp((800,600)).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#357}
--------------------------------------

Subclass DragHandler to use it, and (re)implement the
\_\_init\_\_(\...), detect(\...), drag(\...) and release(\...) methods.

Bind the handler(\...) static method to the event (usually
MOUSEBUTTONDOWN), providing the arguments for the initializer.

The DragHandler will instantiate upon the event and the detect(\...)
method will be called to determine whether a drag operation should
begin.

The \'event\' and \'app\' attributes are set to the event that triggered
this and the PyGameApp component concerned respectively.

Implement detect(\...) so that it returns False to abort the drag
operation, or (x,y) coordinates for the start of the drag operation.
These co-ordinates don\'t have to be the same as the ones supplied -
they are your opportunity to specify the origin for the drag.

During the drag, the DragHandler object will bind to the MOUSEMOTION and
MOUSEBUTTONUP pygame events.

Whilst dragging, your drag(\...) method will be called whenever the
mouse moves and release(\...) will be called when the mouse button(s)
are finally released.

drag(\...) and release(\...) are passed updated x,y coordinates. These
are the origin coordinates (returned by detect(\...) method) plus motion
since the drag began.
:::
:::

------------------------------------------------------------------------

::: {.section}
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
