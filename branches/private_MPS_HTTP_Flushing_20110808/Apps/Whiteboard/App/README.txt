#### KAMAELIA WHITEBOARD ####

## Configuration ##
The whiteboard software will start up without the need for a configuration file, 
however you may wish to change some of the available config values to customise
its operation or enable advanced features.

The config file is saved in JSON format and features the following entries:

{"email" : 
	{"server" : "",
	 "port" : "",
	 "user" : "",
	 "pass" : "",
	 "from" : ""},
 "directories" : 
	{"scribbles" : "",
	 "decks" : ""},
 "webcam" : 
	{"device" : ""}
}

NOTE: If setting either the 'email' or 'directories' element, all entries within
that element must be completed too.

The config file must be saved as 'whiteboard.conf' in one of the following 
locations:

/etc/kamaelia/Kamaelia.Apps.Whiteboard/whiteboard.conf
/usr/local/etc/kamaelia/Kamaelia.Apps.Whiteboard/whiteboard.conf
~/.kamaelia/Kamaelia.Apps.Whiteboard/whiteboard.conf


By default, with no config files available, the whiteboard will not enable e-mail
and will use the following directories for Scribbles and Decks respectively:

~/.kamaelia/Kamaelia.Apps.Whiteboard/Scribbles/
~/Whiteboard/Decks/


## Deck E-mail Support ##
Whilst the whiteboard does support sending of decks by e-mail, it doesn't currently
support the use of this function from behind a proxy server.


## Webcams ##
Please ensure that when using a webcam with the whiteboard it is UVC compatible.
Whilst other cameras may work, some can exhibit issues of a varying nature.
To use a device other than '/dev/video0' please set it in the config file.


## Dependencies ##
- Tested with Python 2.6.5
- python-dev 2.6.6
- python-pygame 1.9.1
- python-cjson 1.0.5
- python-tk 2.6.6
- python-alsaaudio 0.5
- speex 1.0.5 (http://www.speex.org/downloads/)
- pyspeex 0.2 (http://www.freenet.org.nz/python/pySpeex/)
- pyusb 1.0.0 (only required for SMART Board experimentation) (http://pyusb.sourceforge.net/)