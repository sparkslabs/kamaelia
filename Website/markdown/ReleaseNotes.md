---
pagename: ReleaseNotes
last-modified-date: 2008-10-19
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia 0.6.0 Release Notes 
============================

Common changes, due to Axon changes:
------------------------------------

       * Components now get default configuration via class
         attributes.
       * Allows for a more declarative approach of specialising
         entire systems without code duplication or over use of
         inheritance.  (localisation of change)

DELETED FILES
-------------

    Kamaelia/Util/passThrough.py
       - Was deprecated in 0.5.0 in favour of Kamaelia.Util.PassThrough

    Kamaelia/UI/Pygame/BasicSprite.py
       - Removed since wasn't very "kamaelia-like". A better
         experimental replacement exists in Kamaelia.Apps.Games4Kids

    Kamaelia/UI/Pygame/SpriteScheduler.py
       - Removed since wasn't very "kamaelia-like". A better
         experimental replacement exists in Kamaelia.Apps.Games4Kids

New Files:
----------

    Index: Test/Device/DVB/test_SoftDemux.py
       - tests for soft demux DVB component.
    Tools/DocGen/Nodes.py
       - support code for new documentation generation tools
    Tools/DocGen/TestSuiteRun.py
       - support for running the test suites and including output in
         docs
    Tools/DocGen/DocExtractor.py
       - A command line tool for generating Axon and Kamaelia
         documentation
    Tools/DocGen/renderHTML.py
       -  Renderer for converting docutils document trees to HTML output
          with Kamaelia website specific directives, and automatic links
          for certain text patterns.
    Tools/DocGen/README
       - Readme describing docs framework

    Tools/VideoShotChangeDetector/ShotChangeDetector.py
       - This is a simple command line tool to analyse a video file and
         output a list of (probable) locations of cuts (shot-changes)
         in the video.
    Tools/VideoShotChangeDetector/DetectedShotChanges.xsd
       - An schema for defining lists of detected cuts in a video
         sequence.
    Tools/VideoShotChangeDetector/StopSelector.py
       - StopSelector asks the Selector service to shutdown; either
         immediately, or when triggered by anything being sent to any
         of its inboxes.

    Tools/VideoReframer/VideoReframer.py
       - This is a command line tool that decodes a video clip; applies
         edit decisisions (cutting, cropping and scaling); and re-encodes
         it. The idea is to cut and crop video to make it suitable for
         playback on a small screen mobile device by zooming in onto
         just the important bit - such as the face of the interviewee.

    Tools/VideoReframer/MobileReframe.xsd
       - An schema for defining Edit Decision Lists for mobile
         reframing.
        - Adds author: +    Author     : Steve Jolly, British Broadcasting Corporation

    Tools/VideoReframer/EDL.py
        - Components supporting the VideoReframer

    Tools/VideoReframer/StopSelector.py
       - StopSelector asks the Selector service to shutdown; either
         immediately, or when triggered by anything being sent to any
         of its inboxes.

    Tools/VideoPlayer.py
       - Command line tool that plays video clips - both the sound and
         pictures.

    Kamaelia/File/MaxSpeedFileReader.py
       - MaxSpeedFileReader reads a file in bytes mode as fast as it
         can; limited only by any size limit on the inbox it is sending
         the data to.

         This component is therefore useful for building systems that
         are self rate limiting - systems that are just trying to
         process data as fast as they can and are limited by the speed
         of the slowest part of the chain.

    Kamaelia/File/UnixProcess2.py
       - UnixProcess, but with different buffer limiting semantics
         UnixProcess2 allows you to start a separate process and send
         data to it and receive data from it using the standard
         input/output/error pipes and optional additional named
         pipes.
    Kamaelia/Internet/UDP_ng.py
       - Experimental new UDP components that use the selector to 
         awaken them (ie reduce CPU usage).
       - Note, if useful, the contents of this file will replace the
         standard UDP.py file.
       - Adds UDPSender, UDPReceiver

    Kamaelia/Internet/TimeOutCSA.py
       - Designed for use with the improved TCPServer, designed for
         use to monkey patch a timeout into the basic server. Useful
         for setting inactivity timeouts onto socket connections.


    Kamaelia/Experimental/ERParsing.py
       - To support the ER Topology visualiser.
       - Parses a database model described in terms of entities and
         relations.
       - Adds components:
            - ERParser - basic parser
            - ERModel2Visualiser - converts parsed info to messages the
              visualiser understands.

    Kamaelia/Experimental/Chassis.py
       - Extended, experimental versions of Kamaelia.Chassis.Pipeline,
         Kamaelia.Chassis.Graphline and Kamaelia.Chassis.Carousel that
         add the ability to specify size limits for inboxes of
         components.

    Kamaelia/Chassis/Seq.py
       - A Seq component runs components one after the other in sequence,
         waiting until one terminates before starting the next.

    Kamaelia/XML/SimpleXMLParser.py
       - Simple/Basic parsing of XML using SAX
         XMLParser parses XML data sent to its "inbox" inbox using
         SAX, and sends out "document", "element" and "character"
         events out of its "outbox" outbox.

    Kamaelia/Support/Protocol/IRC.py
       - This provides support for Kamaelia.Protocol.IRC.*

    Kamaelia/Support/DVB/DateTime.py
       - Date and time parsing for DVB PSI tables

    Kamaelia/Support/OscarUtil.py
    Kamaelia/Support/OscarUtil2.py
       - OSCAR Support courtesy of GSOC '07, and twisted.
         - GSOC student decided to snapshot the twisted support
           and merge that.

    Kamaelia/Util/SequentialTransformer.py
        - This component applies all the functions supplied to
          incoming messages. If the output from the final function
          is None, no message is sent. (Think of it as a serialised
          version of PureTransformer)

    Kamaelia/Util/PromptedTurnstile.py
        - Buffering of data items until requested one at a time
          PromptedTurnstile buffers items received, then sends
          them out one at a time in response to requests, first-in
          first-out style.

    Kamaelia/Util/RateChunker.py
        - Breaks data into chunks matching a required chunk rate.
          Send data, such as binary strings to this component and
          it will break it down to roughly constant sized chunks,
          to match a required 'rate' of chunk emission.

    Kamaelia/Util/OneShot.py
        - One-shot sending data
          OneShot and TriggeredOneShot send a single specified
          item to their "outbox" outbox and immediately terminate.

    Kamaelia/Util/Tokenisation/Simple.py
        - Provides very simple tokenisation support

    Kamaelia/Util/TwoWaySplitter.py
        - Send stuff to two places
          Splits a data source sending it to two destinations.
          Forwards both things sent to its "inbox" inbox and
          "control" inboxes, so shutdown messages propogate
          through this splitter. Fully supports delivery to size
          limited inboxes.

    Kamaelia/Util/Max.py
        - Find the maximum of a set of values
          Send a list of values to Max and it will send out the
          maximum value in the list.

    Kamaelia/Util/FirstOnly.py
        - Pass on the first item only
          The first item sent to FirstOnly will be passed on. All
          other items are ignored.

    Kamaelia/Util/RangeFilter.py
        - Filter items out that are not in range
        - RangeFilter passes through items received on its "inbox"
          inbox where item[0] lies within one or more of a specfied
          set of ranges of value. Items that don't match this are
          discarded.

    Kamaelia/Util/TagWithSequenceNumber.py
        - Tags items with an incrementing sequence number
        - It takes in items on its "inbox" inbox and outputs
          (seqnum, item) tuples on its "outbox" outbox. 

    Kamaelia/Util/Sync.py
        - Wait for 'n' items before sending one of them on
          For every 'n' items received, one is sent out (the first
          one received in the latest batch).

    Kamaelia/Util/Collate.py
        - Collate everything received into a single message
          Buffers all data sent to it. When shut down, sends all
          data it has received as collated as a list in a single
          message.

    Kamaelia/Codec/WAV.py
        - Reading and writing simple WAV audio files
          Read and write WAV file format audio data using the
          WAVParser and WAVWriter components, respectively.

    Kamaelia/Codec/YUV4MPEG.py
        - Parsing and Creation of YUV4MPEG format files
        - YUV4MPEGToFrame parses YUV4MPEG format data sent to
          its "inbox" inbox and sends video fram data structures
          to its "outbox" outbox.
        - FrameToYUV4MPEG does the reverse - taking frame data
          structures sent to its "inbox" inbox and outputting
          YUV4MPEG format data to its "outbox" outbox."
        - The YUV4MPEG file format is supported by many tools,
          such as mjpegtools, mplayer/mencoder, and ffmpeg.

    Kamaelia/Visualisation/ER/PRelation.py
       - Particle added for visualising relations in EER diagrams

    Kamaelia/Visualisation/ER/PEntity.py
       - Particle added for visualising entities in EER diagrams

    Kamaelia/Visualisation/ER/PAttribute.py
       - Particle added for visualising attributes in EER diagrams

    Kamaelia/Visualisation/ER/PISA.py
       - Particle added for visualising ISA relationships in EER diagrams

    Kamaelia/Visualisation/ER/ERLaws.py
       - Laws governing positioning of EER particles

    Kamaelia/Visualisation/ER/ExtraWindowFurniture.py
       - "furniture" for the EER diagrams.

    Kamaelia/Visualisation/ER/ERVisualiserServer.py
       - Server/viewer for (E)ER models
       - __kamaelia_prefabs__  = ( ERVisualiserServer, ERVisualiser)

    Kamaelia/Device/DVB/Parse/ParseTimeOffsetTable.py
       - Parsing Time Offset Tables in DVB streams
         ParseTimeOffsetTable parses a reconstructed PSI table from
         a DVB MPEG Transport Stream, and outputs the current time
         and date in UTC (GMT) aswell as the current time offset,
         and when the next change will be (due to daylight saving).

    Kamaelia/Device/DVB/Parse/ParseTimeAndDateTable.py
       - Parsing Time And Date Tables in DVB streams
         ParseTimeAndDateTable parses a reconstructed PSI table
         from a DVB MPEG Transport Stream, and outputs the current
         time and date in UTC (GMT).

    Kamaelia/Protocol/HTTP/HTTPRequestHandler.py
       - Split out from Kamaelia/Protocol/HTTP/HTTPServer.py
       - Metadata fixes
       - Documentation fixes

    Kamaelia/Protocol/RecoverOrder.py
       - Recover Order of Sequence Numbered Items
         Recovers the order of data tagged with sequence numbers.
         Designed to cope with sequence numbers that have to
         eventually wrap.

    Kamaelia/Protocol/RTP/RTP.py
       - RTP Packet Framing and Deframing
         Send a dict specifying what needs to go into the RTP
         packet and RTPFramer will output it as a RTP frame.

    Kamaelia/Protocol/AIM/AIMHarness.py
       - AIM Harness
         Provides a high-level Kamaelia interface to AIM.

    Kamaelia/Protocol/AIM/ChatManager.py
       - AIM Client
         Deals with post-login messages from the AIM server, mostly
         by parsing them and sending them out to its "heard" outbox
         in a slightly more useable form. Also sends messages to
         the server based on commands coming through its "talk"
         inbox.

    Kamaelia/Protocol/AIM/LoginHandler.py
       - AIM Login
         This component logs into to AIM with the given screenname
         and password. It then sends its logged-in OSCAR connection
         out of its "signal" outbox, followed by a list of any
         non-login-related messages it has received.

    Kamaelia/Protocol/AIM/OSCARClient.py
       - Kamaelia OSCAR interface
         NOTE: These components implement the OSCAR protocol at
         the lowest level and require a fairly good knowledge of
         OSCAR to use them. For a high-level interface, see
         AIMHarness.py.

    Kamaelia/Protocol/SDP.py
       - Session Description Protocol (SDP) Support
         The SDPParser component parses Session Description
         Protocol (see `RFC 4566`_) data sent to it as individual
         lines of text (not multiline strings) and outputs a
         dictionary containing the parsed session description.

    Kamaelia/Protocol/IRC/IRCClient.py
       - Kamaelia IRC Interface
         IRC_Client provides an IRC interface for Kamaelia
         components.

    Kamaelia/Apps/Show/GraphSlides.py
    Kamaelia/Apps/Compose/GUI/TextOutputGUI.py
    Kamaelia/Apps/Compose/GUI/BuilderControlsGUI.py
    Kamaelia/Apps/Compose/GUI/ArgumentsPanel.py
    Kamaelia/Apps/Compose/PipeBuild.py
    Kamaelia/Apps/Compose/BuildViewer.py
    Kamaelia/Apps/Compose/PipelineWriter.py
    Kamaelia/Apps/Compose/CodeGen.py
    Kamaelia/Apps/Compose/GUI.py
    Kamaelia/Apps/Whiteboard/Options.py
    Kamaelia/Apps/Whiteboard/Palette.py
    Kamaelia/Apps/Whiteboard/CommandConsole.py
    Kamaelia/Apps/Whiteboard/Audio.py
    Kamaelia/Apps/Whiteboard/Painter.py
    Kamaelia/Apps/Whiteboard/CheckpointSequencer.py
    Kamaelia/Apps/Whiteboard/Routers.py
    Kamaelia/Apps/Whiteboard/Tokenisation.py
    Kamaelia/Apps/Whiteboard/Canvas.py
    Kamaelia/Apps/Whiteboard/Entuple.py
    Kamaelia/Apps/Whiteboard/UI.py
    Kamaelia/Apps/Whiteboard/TagFiltering.py
    Kamaelia/Apps/Whiteboard/SingleShot.py
    Kamaelia/Apps/Whiteboard/Router.py
    Kamaelia/Apps/Whiteboard/TwoWaySplitter.py
       - Extracted out from Tools into Kamaelia.Apps.* (allows reuse)

    Kamaelia/Apps/Games4Kids/BasicSprite.py
    Kamaelia/Apps/Games4Kids/SpriteScheduler.py
       - Extracted out from Examples (in fact) into Kamaelia.Apps.* (allows reuse)

    Kamaelia/Apps/IRCLogger/Support.py
       - Supporting Functions for IRC Logger


    Kamaelia/Apps/Games4Kids/MyGamesEventsComponent.py
       - App specific logic component at present.

    Kamaelia/Apps/Grey/PeriodicWakeup.py
       - Simple Periodic Sender Component
         Simply sends a message every X seconds.

    Kamaelia/Apps/Grey/Support.py
       - Collection of support functions from the greylister.

    Kamaelia/Apps/Grey/GreyListingPolicy.py
       - Greylisting Policy For/Subclass Of Concrete Mail Handler
         This component implements a greylisting SMTP proxy
         protocol, by subclassing ConcreteMailHandler and
         overriding the appropriate methods (primarily the
         shouldWeAcceptMail method).

    Kamaelia/Apps/Grey/MailHandler.py
       - Abstract SMTP Mailer Core
         This component effectively forms the skeleton of an SMTP
         server. It expects an SMTP client to connect and send
         various SMTP requests to it. This basic SMTP Mailer Core
         however, does not actually do anything in response to
         any of the SMTP commands it expects.

    Kamaelia/Apps/Grey/ConcreteMailHandler.py
       - Concrete Mail Core
         This code enforces the basic statemachine that SMTP
         expects, switching between the various commands and
         finally results in forwarding on the SMTP command to the
         appropriate SMTP server. By itself, this can be used as a
         simple SMTP Proxy server.

    Kamaelia/Apps/Grey/WakeableIntrospector.py
       - On Demand/Wakeable Introspector
         This component grabs a list of all running/runnable
         components whenever it receives a message on its inbox
         "inbox". This list is then sorted, and noted to a logfile.

    Kamaelia/Video/CropAndScale.py
       - Video frame cropping and scaling
         This component applies a crop and/or scaling operation
         to frames of RGB video. Requires PIL - the python
         imaging library. http://www.pythonware.com/products/pil/

    Kamaelia/Video/DetectShotChanges.py
       - Detecting cuts/shot changes in video
         DetectShotChanges takes in (framenumber, videoframe)
         tuples on its "inbox" inbox and attempts to detect where
         shot changes have probably occurred in the sequence. When
         it thinks one has ocurred, a (framenumber, confidencevalue)
         tuple is sent out of the "outbox" outbox.

    Kamaelia/Video/PixFormatConversion.py
       - Converting the pixel format of video frames
         These components convert the pixel format of video frames,
         for example, from interleaved RGB to planar YUV 420.

    Kamaelia/Video/__init__.py
       - Contains documentation/overview of the Kamaelia.Video
         components

    Kamaelia/UI/Pygame/VideoSurface.py
       - Pygame Video Surface
         Displays uncompressed RGB video data on a pygame surface
         using the Pygame Display service. Provides an alternative
         to video overlays. (also means it can be put onto an OpenGL
         texture)

    Kamaelia/UI/Pygame/Text.py
       - Pygame components for text input and display
       - TextDisplayer displays any data it receives on a Pygame
         surface. Every new piece of data is displayed on its own
         line, and lines wrap automatically.
       - Textbox displays user input while the user types, and
         sends its string buffer to its 'outbox' when it receives
         a '\n'.

    Examples/UsingChassis/WhatIsTheCarouselFor/PlayMP3s.py
       - Example showing how to use the Carousel to play several
         MP3s using a configured MP3 reader

    Examples/UsingChassis/WhatIsTheCarouselFor/PlayMP3.py
       - Example showing how to use the Carousel to play a
         configured MP3 reader

    Examples/UsingChassis/WhatIsTheCarouselFor/README
       - Simple readme for above 2 examples.

    Examples/SimpleGraphicalApps/TextBox/Textbox_ConsoleEchoer_Demo.py
    Examples/SimpleGraphicalApps/TextBox/ConsoleReader_TextDisplayer_Demo.py
    Examples/SimpleGraphicalApps/TextBox/Textbox_TextDisplayer_Demo.py
    Examples/SimpleGraphicalApps/TextBox/Source_TextDisplayer_Demo.py
       - Simple examples using Kamaelia.UI.Pygame.Text.*

    Examples/SoC2006/THF/MiniExamples/SimpleCube.py
    Examples/SoC2006/THF/MiniExamples/ProgressBar.py
    Examples/SoC2006/THF/MiniExamples/Movement.py
    Examples/SoC2006/THF/MiniExamples/Intersect.py
    Examples/SoC2006/THF/MiniExamples/SimpleTranslationInteractor.py
    Examples/SoC2006/THF/MiniExamples/SimpleRotationInteractor.py
    Examples/SoC2006/THF/MiniExamples/SkyGrassBackground.py
    Examples/SoC2006/THF/MiniExamples/OpenGLComponent.py
    Examples/SoC2006/THF/MiniExamples/LiftTranslationInteractor.py
    Examples/SoC2006/THF/MiniExamples/Button.py
    Examples/SoC2006/THF/MiniExamples/MatchedTranslationInteractor.py
    Examples/SoC2006/THF/MiniExamples/Label.py
    Examples/SoC2006/THF/MiniExamples/TexPlane.py
    Examples/SoC2006/THF/MiniExamples/Container.py
    Examples/SoC2006/THF/MiniExamples/PygameWrapper.py
    Examples/SoC2006/THF/MiniExamples/SimpleButton.py
    Examples/SoC2006/THF/MiniExamples/ArrowButton.py
       - Simple examples using Kamaelia.UI.OpenGL.*

    Examples/TCP_Systems/HTTP/ConsoleDownloader.py
        - Demo of HTTP code

    Examples/TCP_Systems/SSL/https.py
        - Shows how to hook up the TCPClient such that you can 
          use it to manually talk to an HTTPS server.

    Examples/TCP_Systems/AIM/ConsoleOneBuddyMessenger.py
        - One-buddy AIM Client
          Allows users to instant-message one of their buddies.
          A command-line program with the syntax:
          ./OneBuddyMessenger [-s screeenname password] [-b buddy]

    Examples/TCP_Systems/IRC/BasicDemo.py
        - Simple IRC demo

    Examples/Handles/simplehttpclient.py
        - How to use the Kamaelia.Protocol.HTTP.HTTPClient code in
          a non-kamaelia program - ie how to use the new "Handle"
          facility.

    Examples/Handles/simpleoggdecoder.py
        - Another example on using Handles to put Kamaelia code
          into a background thread.

    Examples/Handles/simpletcpclient.py
        - Another example on using Handles to put Kamaelia code
          into a background this time it's essentially about doing
          IRC related things in the background.

    Examples/Handles/simpleoggradioplayer.py
        - Another example on using Handles to put Kamaelia code
          into a background thread.

    Examples/Handles/LikeTicker.py
        - Another example on using Handles to put Kamaelia code
          into a background thread.

    Examples/Handles/mediumtcpclient.py
        - Another example on using Handles to put Kamaelia code
          into a background thread.

Changed
-------

    Test/test_Selector.py
       - to handle component name change
    Test/Util/test_Marshalling.py
       - namespace changes
    Tools/Show.py
       - namespace changes:
            Kamaelia.Chassis
            Kamaelia.Apps

    Tools/Whiteboard/Whiteboard.py
        import os
       - namespace changes:
            Kamaelia.Chassis
            Kamaelia.Apps
       - Will now work even if certain parts of audio don't
           - eg non-availability of pymedia, speex.
       - now supports the concept of notepads as a command line argument
          - defaults still to "Scribbles"
       - General code clean up and better componentisation
         into Kamaelia.Apps

    Tools/Whiteboard/WhiteboardRecorder.py
    Tools/Whiteboard/WhiteboardPlayer.py
    Tools/Whiteboard/MP3Player.py
       - namespace changes:
            Kamaelia.Apps
            (Enables reuse of Whiteboard code in other apps potentially
             within limits)


    Tools/Compose.py
       - Largely disabled by changes since 0.5.0, but with good reason.
          - lots of code cleanup, and uses a new introspection method
            regarding the repository based on parsing the component
            definitions rather than imports.

    Kamaelia/File/Reading.py
        - Documentation and introspection fixes

    Kamaelia/File/BetterReading.py
       - namespace change:
           Kamaelia.KamaeliaIPC -> Kamaelia.IPC
       - bugfix


    Kamaelia/Internet/SingleServer.py
        - Better shutdown support via .stop() (from scheduler)
        - Better passon/shutdown support

    Kamaelia/Internet/UDP.py
        - Documentation & examples added
        - SimplePeer implementation simplified
        - TargettedPeer output form is now (data,(host, port))
        - PostboxPeer now expects data of form: (host,port,data)

    Kamaelia/Internet/ConnectedSocketAdapter.py
        - Changes to support removeReader, removeWriter
        - Now supports SSL connections, via SSLSocket
        - ConnectedSocketAdapter:
           new inbox: "makessl": "Notify this CSA that the socket
             should be wrapped into SSL",
           new outbox: "sslready": "Notifies components that
             the socket is now wrapped into SSL",
        - Various internal improvements
        - Much improved shutdown handling
        - self.scheduler.stop() can now shutdown a server cleanly,
          including attempting to close all open sockets, and pass
          shutdown info to protocol handlers etc
        - Data send queue no longer has an internal buffer unless
          absolutely necessary.
        - Adds author sylvain hellagouache

    Kamaelia/Internet/TCPServer.py
        - Changes primarily to improve shutdown handling.
           - See cookbook for examples.
        - Change to use (self.CSA) (for example) rather than use
          ConnectedSocketAdapter directly - allowing for override of
          the specific CSA by users of this class.

    Kamaelia/Internet/Selector.py
       - Improved shutdown handling. (No sockets being managed for
         5 seconds == shutdown)

       - select timeout changed from 5 seconds to 0.05 seconds. This
         makes the system more responsive to shutdown requests

    Kamaelia/Internet/TCPClient.py
       - Changed to support the SSL support in the CSA
       - Better shutdown handling.
       - New inbox: makessl : Notifications to the
         ConnectedSocketAdapter that we want to negotiate SSL
       - New outbox: sslready : SSL negotiated successfully
       - More correct support for errors on windows

    Kamaelia/BaseIPC.py

       - Documentation improvements. NOTE: Many components do not
         use this, and it's use is limited to the HTTP code primarily.
         It may or may not be useful to you.

    Kamaelia/Experimental/Services.py
       - Metadata added

    Kamaelia/Chassis/ConnectedServer.py
       - Documentation changes
       - Shutdown improvements
       - Change from just SimpleServer to ServerCore and SimpleServer
       - ServerCore protocols gets 4 named arguments by default:
             peer, peerport, localip, localport
       - New inbox: _socketactivity : Messages about new and closing
         connections here
       - ServerCore configuration changed to allow TCPServer to be
         easily overridden by a user.

    Kamaelia/Chassis/Carousel.py
    Kamaelia/Chassis/Prefab.py
    Kamaelia/Chassis/Pipeline.py
    Kamaelia/Exceptions.py
    Kamaelia/Support/Deprecate.py
       - Documentation improvements

    Kamaelia/Support/Data/Repository.py
       - Documentation improvement & complete overhaul of approach

    Kamaelia/Support/DVB/Descriptors.py
       - Documentation fixes
       - Extended to include content type genres - level 1, level 2
       - Better error handling in the absence of missing bindings
       - descriptor parses extended to allow parser_sets
       - parser_content_Descriptor & results extended
       - Better support for ETSI TS 102 323 defined descriptors
       - lookup tables for descriptors to something understandable.

    Kamaelia/Util/ConsoleEcho.py
       - deprecated in favour of Kamaelia/Util/Console.py

    Kamaelia/Chassis/Carousel.py
    Kamaelia/Util/PureTransformer.py
    Kamaelia/Support/Data/Experimental.py
    Kamaelia/Support/DVB/CRC.py
    Kamaelia/Util/Chooser.py
    Kamaelia/Util/Filter.py
       - Minor bugfixes

    Kamaelia/Util/MarshallComponent.py
    Kamaelia/Util/Backplane.py
    Kamaelia/Codec/Speex.py
    Kamaelia/Visualisation/Axon/AxonVisualiserServer.py
       - Metadata fixes

    Kamaelia/Internet/Selector.py
    Kamaelia/Util/PureTransformer.py
    Kamaelia/Util/Chooser.py
    Kamaelia/File/UnixProcess.py
    Kamaelia/File/ReadFileAdaptor.py
    Kamaelia/Community/__init__.py
    Kamaelia/Chassis/Graphline.py
    Kamaelia/Support/Particles/SpatialIndexer.py
    Kamaelia/Support/Data/bitfieldrec.py
    Kamaelia/Util/DataSource.py
    Kamaelia/Util/Fanout.py
    Kamaelia/Util/Console.py
    Kamaelia/Util/Splitter.py
    Kamaelia/Util/Comparator.py
    Kamaelia/Util/Chunkifier.py
    Kamaelia/Util/ChunkNamer.py
    Kamaelia/Util/Introspector.py
    Kamaelia/Util/UnseenOnly.py
    Kamaelia/Util/NullSink.py
    Kamaelia/Util/Marshalling.py
    Kamaelia/Util/RateFilter.py
    Kamaelia/Util/Stringify.py
    Kamaelia/Codec/RawYUVFramer.py
    Kamaelia/Visualisation/PhysicsGraph/lines_to_tokenlists.py
    Kamaelia/Visualisation/PhysicsGraph/GridRenderer.py
    Kamaelia/Visualisation/PhysicsGraph/ParticleDragger.py
    Kamaelia/Visualisation/PhysicsGraph/TopologyViewerServer.py
    Kamaelia/Visualisation/PhysicsGraph/chunks_to_lines.py
    Kamaelia/Visualisation/Axon/ExtraWindowFurniture.py
       - Documentation fixes

    Kamaelia/Util/PassThrough.py
    Kamaelia/Util/Clock.py
    Kamaelia/Util/Backplane.py
    Kamaelia/Visualisation/PhysicsGraph/TopologyViewer.py
       - Documentation improvement

    Kamaelia/Util/RateFilter.py
    Kamaelia/Util/Backplane.py
    Kamaelia/Visualisation/Axon/ExtraWindowFurniture.py
    Kamaelia/Device/DVB/EIT.py
       - Minor bugfixes

    Kamaelia/Codec/Dirac.py
       - Doc fixes
       - Better support for Dirac 0.6.0 vs 0.5.4
       - better support of more encoding parameters

    Kamaelia/Visualisation/Axon/PComponent.py
       - Support for abbreviating node names
       - collection of default colours - colours selected and
         mixed based on the letters in the node name.
       - Switch from circles to hexagons

    Kamaelia/Device/DVB/Core.py
       - Documentation improvements
       - Use fixed DVB bindings
       - Locking of DVB device handled correctly now
       - Metadata fixes

    Kamaelia/Device/DVB/DemuxerService.py
       - Documentation improvements
       - Metadata fixes

    Kamaelia/Device/DVB/Tuner.py
       - Documentation improvements
       - Metadata fixes
       - Use fixed DVB bindings
       - Locking of DVB device handled correctly now

    Kamaelia/Device/DVB/SoftDemux.py
       - Minor bugfixes

    Kamaelia/Device/DVB/__init__.py
       - Documentation improvements

    Kamaelia/Device/DVB/NowNext.py
       - Documentation improvements

    Kamaelia/Device/DVB/Parse/ParseProgramMapTable.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings

    Kamaelia/Device/DVB/Parse/ReassemblePSITables.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings

    Kamaelia/Device/DVB/Parse/ParseEventInformationTable.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings

    Kamaelia/Device/DVB/Parse/__init__.py
       - Documentation improvements

    Kamaelia/Device/DVB/Parse/PrettifyTables.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings
       - Metadata fixes

    Kamaelia/Device/DVB/Parse/ParseNetworkInformationTable.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings
       - Metadata fixes

    Kamaelia/Device/DVB/Parse/ParseServiceDescriptionTable.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings
       - Metadata fixes

    Kamaelia/Device/DVB/Parse/ParseProgramAssociationTable.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings
       - Metadata fixes

    Kamaelia/Device/DVB/Receiver.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings
       - Metadata fixes

    Kamaelia/Device/DVB/PSITables.py
       - Documentation improvements
       - Minor bugfixes
       - Use fixed DVB bindings
       - Metadata fixes

    Kamaelia/Protocol/HTTP/ErrorPages.py
       - return bundles: "type" -> "content-type"

    Kamaelia/Protocol/HTTP/Handlers/SessionExample.py
       - return bundles: "type" -> "content-type"

    Kamaelia/Protocol/HTTP/Handlers/UploadTorrents.py
       - return bundles: "type" -> "content-type"

    Kamaelia/Protocol/HTTP/Handlers/Minimal.py
       - return bundles: "type" -> "content-type"
       - Documentation fixes
       - added debug info

    Kamaelia/Protocol/HTTP/IcecastClient.py
       - Documentation improvements

    Kamaelia/Protocol/HTTP/HTTPParser.py
       - Documentation improvements
       - Logic changed to use WaitComplete to improve clarity
       - Now supports the extended form of protocol creation - ie
         supports peer, peerport, localip, localport
       - Minor improvements
       - Much better shutdown support
       - Better support for alternate HTTP methods (eg PUT)
       - Code refactored for clarity/improved maintainability
       - Code made more robust
       - Buffer handling made more accurate
       - More explicit about half close issues
       - Errors in the state machine clearer regarding 100
         continue messages

    Kamaelia/Protocol/HTTP/HTTPClient.py
       - Documentation improvements
       - better support for alternate HTTP methods and extra
         headers (ie changed initialiser)
       - partial code cleanup
       - Metadata fixes

    Kamaelia/Protocol/HTTP/HTTPHelpers.py
       - Metadata fixes

    Kamaelia/Protocol/HTTP/HTTPServer.py
       - Split out code from here into HTTPRequestHandler
       - Added HTTPShutdownLogicHandling component - assists with
         shutting down the various parts.
       - HTTPServer is a prefab, configuring the various parts,
         specifically including. PARSER
          - Likely to be renamed HTTP_ServerSide
       - Metadata fixes

    Kamaelia/Protocol/FortuneCookieProtocol.py
       - Documentation improvements
       - Likely candidate for disappearance at some point (largely
         a demo protocol)

    Kamaelia/Protocol/EchoProtocol.py
       - Documentation improvements

    Kamaelia/Protocol/Torrent/TorrentClient.py
       - Documentation improvements
       - Metadata fixes

    Kamaelia/Protocol/Torrent/TorrentMaker.py
       - Metadata fixes

    Kamaelia/Protocol/Torrent/TorrentPatron.py
    Kamaelia/Protocol/Torrent/TorrentService.py
    Kamaelia/Protocol/RTP/NullPayloadRTP.py
       - Documentation improvements

    Kamaelia/Protocol/RTP/RtpPacker.py
       - Documentation fixes

    Kamaelia/Protocol/RTP/__init__.py
       - Documentation improvements

    Kamaelia/Protocol/RTP/RTCPHeader.py
       - Documentation fixes

    Kamaelia/Protocol/SimpleReliableMulticast.py
       - Documentation fixes
       - Metadata fixes

    Kamaelia/Audio/RawAudioMixer.py
       - Documentation improvements
       - Metadata fixes

    Kamaelia/Audio/PyMedia/Resample.py
       - Documentation improvements
       - Requires PyMedia
       - Metadata fixes

    Kamaelia/Audio/PyMedia/Input.py
       - Documentation improvements
       - Requires PyMedia
       - Metadata fixes

    Kamaelia/Audio/PyMedia/Output.py
       - Documentation improvements
       - Requires PyMedia
       - Metadata fixes

    Kamaelia/Audio/Filtering.py
       - Metadata fixes

    Kamaelia/Audio/Codec/PyMedia/Encoder.py
       - Documentation improvements
       - Requires PyMedia
       - Metadata fixes

    Kamaelia/Audio/Codec/PyMedia/Decoder.py
       - Documentation improvements
       - Requires PyMedia
       - Metadata fixes

    Index: Kamaelia/IPC.py
       - Added serverShutdown message.
       - newCSA message also supports passing through the socket now.

    Kamaelia/UI/Pygame/VideoOverlay.py
       - Minor documentation fixes


    Kamaelia/UI/Pygame/KeyEvent.py
       - Minor documentation fixes
       - Support for keyup events as well as key down. Key down
         is still the default. (backwards compatible)

    Kamaelia/UI/Pygame/Button.py
       - Minor documentation fixes

    Kamaelia/UI/Pygame/Multiclick.py
       - Minor bugfix (fix does not affect user of component aside
         from making this component work better)

    Kamaelia/UI/Pygame/Ticker.py
       - Minor bugfix (fix does not affect user of component aside
         from making this component work better)

    Kamaelia/UI/Pygame/Image.py
       - Now able to accept image data (eg in a string read from
         a file or via the network, and able to display that
         directly, via the magic of StringIO) Described as
         "file_strings"

    Kamaelia/UI/Pygame/Display.py
       - Documentation improvements
       - Better windows support due to change to _PygameEventSource
         (use pygame.event.peek not pygame.event.get)
       - Support for passing events to the surface ONLY if the
         mouse is inside the surface, rather than outside.
       - Added support for an "fullscreen" message to toggle
         fullscreen cleanly
       - better handle of events in general 
       - now defaults to always closing the mixer before trying
         to set the display mode.
       - Ensures that the pipewidth between the event source and
         display is only wide enough for a single message - to
         avoid memory explosion.

    Kamaelia/UI/OpenGL/Movement.py
    Kamaelia/UI/OpenGL/SimpleTranslationInteractor.py
       - Metadata fixes

    Kamaelia/UI/OpenGL/OpenGLComponent.py
       - Minor bugfix

    Kamaelia/UI/OpenGL/Button.py
       - Documentation improvements
       - Metadata fixes

    Kamaelia/UI/GraphicDisplay.py

    setup.py
       - Lots of packages added.
       - version bumped

    Examples/Introspection/IntrospectingSimpleStreamingSystem.py
    Examples/Multicast/SimpleReliableMulticast/MulticastStreamingSystem_SRM.py
    Examples/Multicast/BasicSystems/MulticastStreamingSystem.py
    Examples/Multicast/BasicSystems/MulticastStreamingServer.py
    Examples/VideoCodecs/Dirac/SimpleDiracPlayer.py
    Examples/TCP_Systems/SimpleStreamingPieces/SimpleStreamer.py
       - Examples changed to used media files we can share

    Examples/DVB_Systems/PersonalVideoRecorder.py
    Examples/DVB_Systems/RecordNamedChannel.py
    Examples/DVB_Systems/TransportStreamCapture.py
    Examples/DVB_Systems/SingleChannelTransportStreamCapture.py
       - To match changes to the DVB bindings
       - Minor bugfixes

    Examples/SimpleGraphicalApps/BouncingCatGame/Sprites/BasicSprite.py
    Examples/SimpleGraphicalApps/BouncingCatGame/Simplegame.py
       - minor bugfixes

    Examples/SoC2006/RJL/
       - Minor fixes (avoid using deprecated code)










    Axon Release Notes: 1.6.0New Files & Functionality


    Index: Axon/Handle.py

    Rewritten replacement for LikeFile. Intended to be used with
    Axon.background. Handle and code using it is experimental at
    present. See Examples/Handle for how to use this.

    Handle is specifically designed to allow you to use Kamaelia components
    and subsystem in non-kamaelia systems. It does this by providing you
    with a "Axon.Handle" which is conceptually similar to a "file handle".
    The interface allows you to start components in the background, and
    read from it's outboxes, and write to it's inboxes in a non-blocking
    fashion.

    The fact that it's non-blocking does mean that exceptions can be thrown
    if the component isn't ready for some reason, but this is intentionally
    similar to talking a non-blocking file handle.

    Note: whilst Handle is conceptually similar to a file handle, since you
    have multiple data sources and data sinks inside a component, the interface
    is not the same as the file interface since it wouldn't be appropriate.
    However, given the usage style is similar, that's why the name of this
    facility is "Handle".

    Limitations:
     * It currently will only allow access to components with the
       default/standard inboxes of inbox/control/signal/outbox.
     * This is a known limitation, but covers a wide class of situations.

    Please look at the examples for details.

    Index: Axon/background.py
        * This provides facilities for running the Axon scheduler in a
          background thread. This is useful for integrating Kamaelia code
          with non-Kamaelia based systems - especially those that MUST own
          the primary thread (eg various windowing systems).
        * Expected to be used with Axon.background.
        * Please see Examples/Handle for examples of usage.
        * Simplest usage:
              from Axon.background import background
              from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle
              import time

              background = background().start()

              MagnaDoodle().activate()
              while 1:
                  time.sleep(1)
                  print "."

    Index: Axon/STM.py
       * Support for basic in-process software transactional memory.

       * Software Transactional Memory (STM) is a technique for allowing
         multiple threads to share data in such a way that they know when
         something has gone wrong. It's been used in databases (just called
         transactions there really) for some time and is also very similar
         to version control. Indeed, you can think of STM as being like
         variable level version control. (If you ignore history and are
         just after version numbers(!))

       * This is provided for those times when you really DO need to share
         values between threads/component.

    Index: Axon/experimental/_pprocess_support.py
       * The internals of this are strictly private from an API perspective.
         It's actually based on an older version of Axon.Handle which works
         sufficiently well for Axon.experiment.Process, but not for general
         support. (essentially it's the old Axon.LikeFile code, which was
         experimented with between Axon 1.5 and 1.6)

    Index: Axon/experimental/Process.py
       * Provides the core for multiprocess support in Kamaelia.
         Specifically provides ProcessPipeline and ProcessGraphline. At
         present thse are limited in the inboxes/outboxes you can use for
         linkages to just inbox/outbox/control/signal. This is a
         limitation, but sufficient in many contexts.

    Index: Examples/STM/Philosophers.py
       * An example of how to implement dining philosophers with pure
         python threads and Axon's STM code.

    Index: Examples/STM/Axon.Philosophers.py
       * An example of how to implement dining philosophers with
         Axon ThreadedComponents and Axon's STM code.

    Index: Examples/SystemShutdown.py
        * Example of how to use the new self.scheduler.stop() facility in
          Axon, both in terms of shutting down the system and also in terms
          of shutting down components that don't actually support shutting
          down directly.

    Index: Examples/Handles/TestHandle.py
        * An acceptance test for using Axon.Handle to act as a manual
          intermediary between 2 Kamaelia components in a non-Kamaelia
          system.

          Ie read from this one, pass onto that one - core of the code for
          that is this:
               while 1:
                   time.sleep(1)
                   try:
                      data = TB.get("outbox")
                      print data
                      message = data
                   except Queue.Empty:
                      pass
                   TD.put(message, "inbox")

    Index: Examples/Handles/reverser.py
       * And example of how to use Handle with a trivial component that
         reverses lines of data passed to it. (The aim is not to demo the
         component, but how to use the component in a non-Kamaelia system)
         After all, the component could be accessing a remote web service
         instead.

Axon Files Changed and Changes in this release 
----------------------------------------------

    Index: Axon/Component.py
        * Copyright notice change
        * Documentation changed to REST format
        * Extensive Documentation improvements
        * change to support this:
        * +      self.__dict__.update(argd)
           -- Major change/improvement despite appearances
        * Components can now be awoken when a component
          *leaves* an outbox again.
        * New method:
               def setInboxSize(self, boxname, size):
                    "boxname - some boxname, must be an inbox ;
                     size - maximum number of items we're happy
                     with"
        * Extra debugging assistance in some unusual situations,
          specifically designed to catch where someone uses the
          class where they should be using an instance when
          creating sub components.
        * New method:
        +   def Inbox(self, boxname="inbox"):
        +       while self.dataReady(boxname):
        +           yield self.recv(boxname)

    Index: Axon/Box.py
       * Copyright notice
       * Module documentation added - REST format
         * nullsink Class documentation added
            * Method documentation added
         * realsink Class documentation added
            * Method documentation added

         * postbox Class documentation clarified
            * Init gains notify method
            * Ahhh, "wake on object taken from outbox implemented",
              this is implemented using notify and following down
              the chain of linkages.
            * Notify on pop added
               * Variety of knockons in lots of places.
               - Cause of many of the changes to this module.
            * Method documentation added

    Index: Axon/Introspector.py
        * Documentation changed to REST format
        * Documentation improvements
        * Added documentation of internals

    Index: Axon/__init__.py
        * Documentation changed to REST format
        * Documentation added, matching new autodocs system
        * Code tidying

    Index: Axon/Postoffice.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Adds in BoxAlreadyLinkedToDestination error
           - thrown if the user tries to link an outbox to a
             destination, when it is already linked to a
             destination.

    Index: Axon/ThreadedComponent.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Minor bugfix ( _threadrunning flag)
        * stuffWaiting = True commented out
        * Fixes regarding waking a thread back up when a message is
          taken from it's outbox. (ie improvements to unpausing
          when message taken from outbox)
          (hence removal of stuffWaiting flag)
        * Unpauses on recv from inbox.
        * Unpauses on send to outbox
        * Minor changes to improve responsiveness when pausing

    Index: Axon/debugConfigDefaults.py
        * Documentation changed to REST format
        * Major documentation improvements.

    Index: Axon/Axon.py
        * Documentation changed to REST format
        * Removed the metaclass created __super() method
          convenience function - it's been deprecated for
          a long time since there's boundary issues where
          it would go wrong.

    Index: Axon/AxonExceptions.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * New exception: BoxAlreadyLinkedToDestination
          The inbox/outbox already has a linkage going *from* it
          to a destination.

          Possible causes:
              - Are you trying to make a linkage going from an
                inbox/outbox to more than one destination?
              - perhaps another component has already made a
                linkage from that inbox/outbox?

    Index: Axon/Microprocess.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Added extra argument to microprocess, specifically tag=
          this allows the name of the microprocess to be tagged.
          This is useful in conjunction with WaitComplete and The
          Introspector and pausing to understand why a piece of
          code is staying in a particular WaitComplete loop/state.
        * When .stop() is called the microprocess, it's scheduler
          is set to a null scheduler.
        * Extra error messages when you call WaitComplete with a
          function rather than a generator. (you should only pass
          a generator object into WaitComplete, rather than a
          function).

    Index: Axon/Linkage.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Extra debugging provided in the case of trying to make a
          link from an outbox that doesn't exist. This is possible
          to do accidentally by having a trailing comma in the
          linkage description. (So this possible causes is
          described in the error message)

    Index: Axon/Ipc.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Signature of WaitComplete changed from:
           def __init__(self, *args):
           to 
           def __init__(self, *args,**argd):
           Copies of args/argd copied in as attributes. 

    Index: Axon/debugConfigFile.py
        * Documentation changed to REST format
        * Major documentation improvements.

    Index: Axon/util.py
        * Documentation changed to REST format
        * Documentation improvements.

    Index: Axon/Scheduler.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * import os
        * Signature changed to include **argd rather than no args.
        * Added "wait_for_one" attribute
           - Means the scheduler can be started without any
             components/microprocesses being ready to run.
        * Added in a stopRequests queue (for safely recieving
          method calls from users of the system)
        * The wait_for_one class flag causes an internal flag to
          note that we have to wait for at least one microprocess
          to start before the scheduler exits.
        * New method waitForOne to allow the same flag to be set
        * This flag is cleared when a new microprocess is started.
        * listAllThreads method now switches on local debugging as
           well.
        * Handling of WaitComplete extended to allow passing
          through any tag provided by the user. Otherwise a default
          tag is created based on the parent's microprocess name.
        * Support for .stop() requests changes the logic in the
          main loop for the scheduler to allow clean shutdown and
          exit of loops. After exitting the main loop, the
          scheduler calls the .stop() method of all
          microprocesses & components in the run queue.
          One key use case for this is to allow clean close and
          shutdown of TCP sockets when someone calls
          self.scheduler.stop()
        * The self.stop() method however doesn't directly
          maniplate this flag, but in fact updates a threadsafe
          queue. The reason for that is to allow threaded
          components as well as generator components to cleanly
          call this method.

    Index: Axon/AdaptiveCommsComponent.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Change to _AdaptiveCommsable.__init__ signature to
          support class based system configuration.
        * addOutbox defaults to also ensuring that the
          self.unpause callback gets added as the notification
          callback when a message is removed from an outbox.
        * Change to AdaptiveCommsableComponent.__init__ signature
          to support class based system configuration.

    Index: Axon/CoordinatingAssistantTracker.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * New .zap() method to clear the services and information
          logged by the co-ordinating assistant tracker. This was
          added to assist with multiple process support.

    Index: Axon/debug.py
        * Documentation changed to REST format
        * Documentation improvements.

    Index: Axon/idGen.py
        * Documentation changed to REST format
        * Documentation improvements.

    Index: setup.py
        * Annotated slightly to assist building targetted
          application tar balls.

    Index: CHANGELOG
    +
    +   * Added support for *basic* software transactional memory
    +    * Software transactional memory is a fancy phrase for something
    +      that boils down to something similar to version control for
    +      variables. You can checkout the current state, make modifications
    +      and try to commit them back. If the commit succeeds, you
    +      successfully updated it. If it doesn't, you didn't.
    +
    +      This implements it, and provides a mechanism for making the CAT
    +      safe for threads to use as well as standard components.
    +
    +    Added in LikeFile --> renamed to Handle
    +    Added in support for monkey patching the internals of a component
    +    system.

    +1.5.1 -> 1.x.x
    +    An exception is now raised if you try to create a linkage going
    +    from an inbox/outbox that already has a linkage going from it.
    +
    +    Waking up of producer components re-introduced (bugfix)
    +
    +    * When a component collects a message from an inbox; all producer
    +      components with outboxes linked to that inbox will be woken.
    +
    +    Additions to the Axon Test Suite providing test coverage of this
    +    facility.

\
 \

\
