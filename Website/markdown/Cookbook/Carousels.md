---
pagename: Cookbook/Carousels
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
> \

Cookbook : Carousels
====================

So you\'ve built your components and wired them up using
[Pipelines](/Cookbook/Pipelines%20) and
[Graphlines](/Cookbook/Graphlines%20) . But what do you do if you want
to create or initialise a component at runtime?

Perhaps you can\'t know the value of some arguments until you start
reading that input file. Or maybe you want to process several streams of
data in sequence, but the component you want to use isn\'t designed to
process several streams back to back. This is where a component like the
*Carousel* comes in.

The Carousel gives us a way to create a component on-the-fly in response
to being sent a message.\

### For example\...

Suppose we want to play an MP3 file \... we could use a simple pipeline
like this:\

>     from Kamaelia.File.Reading import RateControlledFileReader
>     from Kamaelia.Audio.Codec.PyMedia.Decoder import Decoder
>     from Kamaelia.Audio.PyMedia.Output import Output
>     from Kamaelia.Chassis.Pipeline import Pipeline
>
>     import sys
>     mp3filename=sys.argv[1]
>
>     Pipeline( RateControlledFileReader( mp3filename, readmode="bytes", rate=256000/8),
>               Decoder("mp3"),
>               Output(sample_rate=44100, channels=2, format="S16_LE"),
>             ).run()

\
That is all very nice; but what if we get the sample rate, number of
channels or format wrong? We can\'t get this information until we start
decoding it. If we get it wrong then the audio may be corrupted or
played at the wrong speed!\
\
It would be great if, at runtime, we could create the audio playback
(Output) component in response to receiving a message from the MP3
decoder containing the audio format:\
\

::: {align="center"}
![](/images/carousel1_idea.gif)\
:::

\
The PyMedia MP3 Decoder component we are using helpfully sends out a
message containing the information we need, so we can use the Carousel
component to do it like this:\

>     from Kamaelia.Chassis.Graphline import Graphline
>     from Kamaelia.Chassis.Carousel import Carousel
>
>     def makeAudioOutput(metadata):
>         return Output( metadata["sample_rate"],
>                        metadata["channels"],
>                        metadata["format"]
>                      )
>
>     Graphline( READ = RateControlledFileReader( mp3filename, readmode="bytes", rate=256000/8),
>                DECODE = Decoder("mp3"),
>                OUTPUT = Carousel( makeAudioOutput ),
>                linkages = {
>                    ("READ",   "outbox") : ("DECODE", "inbox"),
>                    ("DECODE", "outbox") : ("OUTPUT", "inbox"),
>                    ("DECODE", "format") : ("OUTPUT", "next"),
>
>                    ("READ",   "signal") : ("DECODE", "control"),
>                    ("DECODE", "signal") : ("OUTPUT", "control"),
>                }
>              ).run()

This example is wired up using a Graphline component - find out more
about Graphlines [here](/Cookbook/Graphlines%20) .\

### So what does this do?

### 

The MP3 Decoder component we are using helpfully sends out the format of
the decoded audio out of its \"format\" outbox, so we link this to the
Carousel\'s \"next\" inbox to control it. A message from the decoder wil
look like this:\

>     { "sample_rate" : 44100, "channels":2, "format":"S16_LE" }

We\'ve also written a function makeAudioOutput(). When called with the
message as its argument; it returns a new Output component set up with
the right sample rate, number of channels, and format.

We give this function to the Carousel. Note that we don\'t call it - we
just give it the function. The Carousel calls it when it receives a
message on its \"next\" inbox and therefore needs to create the
component:

\

::: {align="center"}
![](/images/carousel_anim.gif)
:::

\

1.  The Carousel receives a message on its \"next\" inbox, containing
    the format of the audio\
2.  The Carousel calls our *makeAudioOutput* function, passing it this
    message as its parameter\
3.  Our function returns a new Output component, ready to be used.\
4.  Carousel links the new Output component up to use its own inboxes
    and outboxes

So when the raw audio samples start to arrive at its inbox, there will
be a new Output component already linked in to receive them.\
Note that it does not link the \"signal\" outbox - this is so that when
the component finishes and sends its own shutdown message, this doesn\'t
get passed on - after all, you might want to reuse the Carousel with
another component.\

### So why is it called a \"Carousel\" then?

### 

If you send another message to the \"next\" inbox, then the component
gets replaced. Any existing component is told to shutdown and is thrown
away as soon as possible, and a new one is created, by calling our
function with the new message as the parameter.\
\
This kind of behaviour is a little like the carousel on an old slide
projector - when you want to move on, the old item is swapped for the
next one. Alternatively think of a fairground merry-go-round carousel -
where one horse comes by after another.\
\
For example, suppose we want to improve our MP3 player by making it play
multiple files back to back. We could put everything in a Carousel, then
when it has finished, it could send us a message. We could then respond
by sending it the next filename to play, and letting it start again.
Something like this:\

::: {align="center"}
![](/images/carousel_anim2.gif)\

::: {align="left"}
We can do this by using a Chooser component for the playlist and putting
our existing player inside a Carousel. When all the player components
finish, our Carousel will send out a \"next\" message from its
\"requestNext\" outbox, which we can use to cause our Chooser to send
back the next filename:

![](/images/carousel3.gif)

Notice that we can also wire up the \"signal\" and \"control\" boxes, so
that when the Chooser has no more names in its playlist, it can tell our
player Carousel to shut down.\

So now lets build this! First, lets make a function that we will give to
the Carousel for it to use to create our player:\

>     def makePlayer(mp3filename):
>         return Graphline(
>             READ = RateControlledFileReader( mp3filename, readmode="bytes", rate=256000/8),
>             DECODE = Decoder("mp3"),
>             OUTPUT = Carousel( makeAudioOutput ),
>             linkages = {
>                 ("READ",   "outbox") : ("DECODE", "inbox"),
>                 ("DECODE", "outbox") : ("OUTPUT", "inbox"),
>                 ("DECODE", "format") : ("OUTPUT", "next"),
>
>                 ("",      "control") : ("READ",   "control"),
>                 ("READ",   "signal") : ("DECODE", "control"),
>                 ("DECODE", "signal") : ("OUTPUT", "control"),
>                 ("OUTPUT", "signal") : ("",       "signal"),
>             }
>           )
:::
:::

This is almost identical to our player from before. Notice we\'ve added
extra links to make sure shutdown messages can get into and out of the
Graphline. This is important, as Carousel will be listening for our
Graphline sending the shutdown message.\
\
Now lets wire it all up! We will use a *ForwardIteratingChooser* because
it will send a shutdown message once all the filenames have been
iterated over:\

>     from Kamaelia.Util.Chooser import ForwardIteratingChooser
>
>     filenames = argv[1:]
>
>     Graphline( PLAYLIST = ForwardIteratingChooser(filenames),
>                PLAYER   = Carousel( makePlayer, make1stRequest=True ),
>                linkages = {
>                    ("PLAYER",   "requestNext") : ("PLAYLIST", "inbox"),
>                    ("PLAYLIST", "outbox")      : ("PLAYER",   "next"),
>
>                    ("PLAYLIST", "signal") : ("PLAYER", "control"),
>                }
>              ).run()

Notice that we have asked the Carousel to make the 1st request. What
this means is that as soon as it starts it will send out its request for
the next item - instead of just waiting. This gets things going.\
\
So there we have it, a simple mp3 playlist system, built entirely in
Kamaelia, using Carousels to create components with the right settings
when we need them.\

\-- 19 Dec 2006 - Matt Hammond\
