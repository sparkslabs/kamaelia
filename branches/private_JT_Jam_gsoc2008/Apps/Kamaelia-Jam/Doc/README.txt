============
Kamaelia Jam
============

What is it?
-----------
Jam is a simple music sequencer which is designed to be used collaboratively over a network.  It has simple sound generation capabilities built in, but much of the power comes from the output of OSC and MIDI messages, allowing it to control a wide range of hardware and software.

Installation
------------
See INSTALL.txt for full installation instructions, and information on dependencies.

Usage instructions
------------------

The simplest way to run jam is simply to start it up by running::

    jam

This starts jam as the first client in a network.  If you add notes to the piano roll or step sequencer you should hear notes or drums playing.

If you wish to connect to an already running instance of jam then use the --remote-address and --remote-port options, for example::

    jam --remote-address=123.456.7.8 --remote-port=2001

Note that the default port which Jam listens for new connections on is 2001.  When you are connected as part of a network and new peers which join the network will be propagated through and also connect to you, and vice-versa.

If you are using the OSC or MIDI capabilities of Jam you may want to turn off its inbuilt sound.  This can be done by passing the --no-audio option, for example::
    jam --no-audio

For a complete guide to the options jam accepts launch it using the --help option, for example::
    jam --help
