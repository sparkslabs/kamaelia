                            Kamaelia

                         Version 0.4.0

                          14 June 2006

          Kamaelia is a general component framework for
          all programmers and maintainable development.
          Write clear and simple snap-together components
          using Unix Pipes for the 21st Century.

Introduction
============

Kamaelia is a library of networking/communications components for
innovative multimedia systems. The component architecture is designed
to simplify creation and testing of systems, protocols and large scale
media delivery systems. A subset of the system has been tested on
series 60 mobile phones.

It is optimised for simplicity, such that people can get started very
rapidly, and such that maintainers can pick up the code of others
without misunderstandings.

It is designed as a /practical/ toolkit, such that you can build
systems such as:
   * Collaborative whiteboards
   * Transcoding PVRs for timeshifting TV
   * Ogg Vorbis streaming server/client systems (via vorbissimple)
   * Create Video players & streaming systems (for dirac).
       * With subtitles.
   * Simple network aware games (via pygame)
   * Quickly build TCP & Multicast based network servers and clients
   * Presentation tools
   * A networked audio mixer matrix (think multiple audio sources over
     network connections mixed and sent on to multiple locations with
     different mixes)
   * Look at graph topologies & customise the rules of display &
     particle types.
.... Mix and match all of the above.

These are all real examples you can do today.

You can also do a lot of this *visually* using the new PipeBuilder
application in Tools.

Essentially if the system you want to build involves audio or moving
pictures, and you want to be able to make the system network aware,
then this should be quick and easy to do using Kamaelia. (If it isn't,
then a) it's a bug b) needs improving :-)

Oh, and due to things like the visual editor, the use of pygame in a
lot of examples, the use of dirac & vorbis, it's a lot of fun too :-) 

It runs on Linux, Windows, Mac OS X with a subset running on Series 60
phones. (Linux is the primary development system)


Installation
============

Quickstart Instructions for Linux:

Run the following command :

sudo python setup.py install

To get the best out of Kamaelia it makes sense to install a number of
other bindings, and libraries. You can find the details of this in
Docs/GettingStarted.html

NOTE: You are recommended to use the KamaeliaMegaBundles for
      installation and usage of Kamaelia (especially when getting
      started!). This is why this section is relatively short.


License
=======
Copyright (C) 2006 British Broadcasting Corporation and Kamaelia
Contributors(1) All Rights Reserved.

You may only modify and redistribute this under the terms of any of the
following licenses(2): Mozilla Public License, V1.1, GNU General
Public License, V2.0, GNU Lesser General Public License, V2.1

    (1) Kamaelia Contributors are listed in the AUTHORS file and at
         http://kamaelia.sourceforge.net/AUTHORS - please extend this
         file, not this notice.
    (2) Reproduced in the COPYING file, and at:
        http://kamaelia.sourceforge.net/COPYING

Please contact us via: kamaelia-list-owner@lists.sourceforge.net
to discuss alternative licensing.


Documentation
=============

The documentation of Kamaelia is available in the "Docs" subdirectory.

Your suggested route through the documentation is as follows:
   * GettingStarted.html
   * Introduction.html
   * MiniAxon.html - a tutorial on the core of Kamaelia
     (http://kamaelia.sourceforge.net/MiniAxon/ is more dynamic)
   * Cookbook.html

Once you're up and running, the following 2 documents are your jumping
off point for reference material:
   * Components.html
   * Axon.html

Additional documentation can be found online at:
     http://kamaelia.sourceforge.net/


Examples
========

There are two sets of examples included with Kamaelia.
   * "Examples" contains simple example systems implemented using
      Kamaelia. The most substantial example here is example15, which
      is a simple transcoding PVR for timeshifting digital TV.

      Please check out the README in the Examples directory for
      further description of each example.

      If you prefer browsing the examples categorised by type in a
      web browser, please point your browser at either:
         * Docs/Cookbook.html
      
      Or
         * http://kamaelia.sourceforge.net/Cookbook.html

   * "Tools" contains more substantial systems implemented using
     Kamaelia. These include tools for looking (graphically) inside
     running systems, graphically constructing Kamaelia systems, a
     collaborative whiteboard, and so on.


Bugs
====

Please report any bugs to the Kamaelia mailing list.
http://lists.sourceforge.net/lists/listinfo/kamaelia-list


Contact Details
===============

The project website is at http://kamaelia.sourceforge.net/Home
The developer and announcement mailing lists can be fount at
   * http://kamaelia.sourceforge.net/Contact.html


Last updated: Michael, June 2006
--------------
# DRL : Rough draft of README
# MPS : Modified and fleshed out
