---
pagename: KamaeliaGrey
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia: Grey
==============

### What is Kamaelia: Grey ?

It\'s a greylisting SMTP proxy. It doesn\'t replace your existing mail
server, but does sit between your mail server and the outside world.

### How do I install it?

After unpacking, as root, type:

-   `python setup.py install`

Under linux you then type:

-   `chmod +x /etc/init.d/kamaeliagrey`

The code was developed under linux, but is currently acting as a
workhorse under Mac OS X. As a result a startup script for Mac OS X is
also included - take a look in the setup.py file to see what you need to
edit.

### How do I configure it?

Copy the default config file - installed to **/etc/greylist.conf.dist**
to a localised version - ie **/etc/greylist.conf**

You then edit the freshly copied config file. The config options are
documented in the config file.

### How does it work then?

Suppose your existing mailserver:

-   listens on port 25
-   runs on host 192.168.2.25

You change your mailserver to listen on some other port instead. eg 8025
You then configure Kamaelia:Grey to listen on port 25 instead, on that
host.

You also configure Kamaelia:Grey to forward to your mail server

### How do I configure that?

Edit **/etc/greylist.conf**

Change the values smtp\_ip & smtp\_port

eg change them to:

>     smtp_ip = 192.168.2.25
>
>     smtp_port = 8025

### Where can I get more information?

Information will be added to this page. (maybe) Discussion and feedback
should be sent to as issues on github.

### What on Earth is Greylisting?

Without apologies, here\'s a link to a non-techie (albeit a bit silly)
description of greylisting:

-   [Sparkslabs: Greylisting for
    non-techies](http://www.sparkslabs.com/michael/blog/2007/07/31/greylisting-for-non-techies)

More detail on how Kamaelia: Grey works: (this should get consolidated
onto this page)

-   [Sparkslabs: Greylisting using
    Kamaelia](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1190238560)

### I want to understand more?

A presentation

<iframe src="https://www.slideshare.net/slideshow/embed_code/key/xnWyAejVOZ5Hts?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="margin: auto; display: block; border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe>
<div style="margin-bottom:5px"><strong><a href="https://www.slideshare.net/kamaelian/kamaelia-grey" title="Kamaelia Grey" target="_blank">Kamaelia Grey</a></strong> from <strong><a href="https://www.slideshare.net/kamaelian" target="_blank">kamaelian</a></strong></div>


### Related

You may also wish to look at [Kamaelia: Spam
Assistant](KamaeliaSpamAssistant)

### Getting the code

**NB, this is currently out of date and so commented out for now**

<!--
    You can get the install bundle for Kamaelia Grey here: <a href="http://thwackety.com/Kamaelia-Grey.tar.gz">http://thwackety.com/Kamaelia-Grey.tar.gz</a>
    This code is Beta quality in the old fashioned meaning of the term.
    I've been using it for my mail for the past 2 1/2 months now and it's been fantastic.
    There are likely to be minor issues though. Please report them!
-->
