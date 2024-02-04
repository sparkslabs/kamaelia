---
pagename: Cookbook/DVB/SingleChannelTransportStreamCapture
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Recording a channel from a DVB broadcast
===================================================

*Find the code for this here:\
*[/Code/Python/Kamaelia/Examples/DVB\_Systems/SingleChannelTransportStreamCapture.py](http://svn.sourceforge.net/viewvc/kamaelia/trunk/Code/Python/Kamaelia/Examples/DVB_Systems/SingleChannelTransportStreamCapture.py?view=markup)

This simple example shows how to record a channel broadcast in a DVB
multiplex at a frequency of 754MHz, where the channel\'s audio and video
data are carried in packets with packet IDs 640 and 641:\

>     from Kamaelia.Device.DVB.Core import DVB_Multiplex
>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.File.Writing import SimpleFileWriter
>
>     Pipeline(
>        DVB_Multiplex(754, [640, 641]),
>        SimpleFileWriter("BBC_NEWS_24.ts")
>     ).run()

The DVB\_Multiplex component is the simplest and easiest to use combined
tuner and demultiplexer component - you simply specify the frequency, a
list of packet IDs to demultiplex, and an optional dictionary of tuner
control parameters.\

\-- 04 Jan 2007, Matt\

\
