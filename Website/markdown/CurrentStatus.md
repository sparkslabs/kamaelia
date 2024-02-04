---
pagename: CurrentStatus
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
### Current Status

::: {align="right"}
***Last updated:** Nov 11, 2006, Michael Sparks*\

::: {align="left"}
Axon - Core Concurrency framework- version 1.5.1 - overview of status\

-   API Stable for generator components
-   Beta status API for Thread based components
-   Non-CPU-greedy capable (scheduler can sleep and be awoken by
    threads)
-   Production ready (\>6 months on a running system)\

Kamaelia - the toy box - version 0.5.0\

Full coverage of [core aims](/Developers/Direction.html) (introspection,
network, graphics & codec capable, graphical systems composer, large
examples)

API is subject to change (hence 0.5.0 status), but includes:\

-   Network - beta production ready (TCP/UDP/Multicast clients/servers)\

```{=html}
<!-- -->
```
-   Graphics/GUI capabilities - Pygame, OpenGL, Tkinter (stable)\

```{=html}
<!-- -->
```
-   Protocols - HTTP, BitTorrent - beta status

```{=html}
<!-- -->
```
-   Codec support - Dirac (encode/decode), Vorbis(decode),
    Speex(encode/decode), MP3 (decode - via pymedia)

```{=html}
<!-- -->
```
-   PyMedia based support for some audio codecs & audio capture\

```{=html}
<!-- -->
```
-   Devices:

```{=html}
<!-- -->
```
-   Alsa, DVB (digital TV broadcast)

```{=html}
<!-- -->
```
-   Unix Shell outs

```{=html}
<!-- -->
```
-   eg to call transcoding tools

Larger scale systems in the distribution\

-   Kamaelia Macro (timeshift & transcode what\'s broadcast for viewing
    at a more convenient time)
-   P2P Whiteboard (supporting multiple pages, linked whiteboards, audio
    mixing and retransmission, etc)

```{=html}
<!-- -->
```
-   Compose - a graphical composition tool for creating pipelines
-   Axon Shell - a specialised command line allowing the launch of
    components as well as programs
-   Axon Visualiser - a pygame based system for visualising what\'s
    going on inside a Kamaelia system (uses a physics model (based on a
    lava lamp(!) )for layout that we\'ve had repeated comments looks
    fun/attractive :)\
-   Show - a presentation tool\

[Examples](/Cookbook.html) for many major subsystems

Extensive [Documentation](/Components.html) (at minimum detailed module
level docs - ala pydoc)\
:::
:::

Ongoing [Projects](/Developers/Projects.html)\
[Developer Console](/Developers/\
