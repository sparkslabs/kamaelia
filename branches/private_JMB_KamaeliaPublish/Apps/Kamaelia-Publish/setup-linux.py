#!/usr/bin/env python
"""
setup.py - script for installing Kamaelia Publish
"""

from distutils.core import setup

setup(
    name = 'Publish',
    version = '0.0.1',
    description='Kamaelia Publish - A Kamaelia WSGI web server',
    author='Jason Baker, Michael Sparks, BBC, and contributors',
    author_email='jason.baker@ttu.edu',
    url='http://wsgi.coderspalace.com/kcwiki',
    license='Copyright(c) 2008 BBC & Kamaelia Contributors.  All Rights Reserved Use allowed under MPL 1.1, GPL 2.0, LGPL 2.1',
    packages= [ 'Axon',
                'Kamaelia',
                'Kamaelia.Automata',
                'Kamaelia.Audio',
                'Kamaelia.Audio.PyMedia',
                'Kamaelia.Audio.Codec',
                'Kamaelia.Audio.Codec.PyMedia',
                'Kamaelia.Chassis',
                'Kamaelia.Codec',
                'Kamaelia.Device',
                'Kamaelia.Device.DVB',
                'Kamaelia.Experimental',
                'Kamaelia.Experimental.Wsgi',
                'Kamaelia.File',
                'Kamaelia.Internet',
                'Kamaelia.Internet.Simulate',
                'Kamaelia.Protocol',
                'Kamaelia.Protocol.HTTP',
                'Kamaelia.Protocol.HTTP.Handlers',
                'Kamaelia.Protocol.RTP',
                'Kamaelia.Protocol.Torrent',
                'Kamaelia.Support',
                'Kamaelia.Support.Data',
                'Kamaelia.Support.DVB',
                'Kamaelia.Support.Particles',
                'Kamaelia.Support.PyMedia',
                'Kamaelia.Support.Tk',
                'Kamaelia.UI',
                'Kamaelia.UI.Tk',
                'Kamaelia.UI.MH',
                'Kamaelia.UI.Pygame',
                'Kamaelia.UI.OpenGL',
                'Kamaelia.Util',
                #'Kamaelia.Uti.Tokenisation',
                'Kamaelia.Video',
                'Kamaelia.Visualisation',
                'Kamaelia.Visualisation.Axon',
                'Kamaelia.Visualisation.PhysicsGraph',
                'Kamaelia.XML',
                'WsgiApps.Apps'
                "",],
    scripts = ['Linux/App/kamaelia-publish.py',
               'Linux/App/ServerConfig.py',],
    long_description="""
    Kamaelia Publish lets you publish yourself on your own terms.
    """,
)
