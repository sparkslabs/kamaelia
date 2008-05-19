About BitTorrent:
=================

BitTorrent is a tool for distributing files. It's extremely easy to
use - downloads are started by clicking on hyperlinks.  Whenever more
than one person is downloading at once they send pieces of the file(s)
to each other, thus relieving the central server's bandwidth
burden. Even with many simultaneous downloads, the upload burden on
the central server remains quite small, since each new downloader
introduces new upload capacity.


Instructions for users:
=======================

Once you install BitTorrent, you should be able to download .torrent
files.  If you have any questions, please read the FAQ:

http://www.bittorrent.com/FAQ.html

If you find a bug, check the FAQ for your bug.  If your bug is not in
the FAQ, please send email to:

bugs at bittorrent.com


Instructions for publishers:
============================

Instructions for trackerless operation are in TRACKERLESS.txt.

To start hosting -

1) start running a tracker

First, you need a tracker. If you're on a dynamic IP or otherwise 
unreliable connection, you should find someone else's tracker and 
use that. Otherwise, follow the rest of this step.

Trackers refer downloaders to each other. The load on the tracker 
is very small, so you only need one for all your files.

To run a tracker, execute the command bittorrent-tracker.py Here is an
example -

./bittorrent-tracker.py --port 6969 --dfile dstate

--dfile is where persistent information is kept on the tracker across 
invocations. It makes everything start working again immediately if 
you restart the tracker. A new one will be created if it doesn't exist 
already.

The tracker must be on a net-addressable box, and you must know the 
ip number or dns name of it.

The tracker outputs web logs to standard out. You can get information 
about the files it's currently serving by getting its index page. 

2) create a torrent file using maketorrent.py (GUI) or
maketorrent-console.py. The GUI version, maketorrent.py is preferred.

To generate a torrent file using maketorrent-console.py and give it the file
you want a torrent for and the url of the tracker

./maketorrent-console.py myfile.ext http://my.tracker:6969/announce

This will generate a file called myfile.ext.torrent

Make sure to include the port number in the tracker url if it isn't 80.

(You may also use maketorrent.py to create trackerless torrents. See
the file TRACKERLESS.txt for information about trackerless operation.)

This command may take a while to scan over the whole file hashing it.

The /announce path is special and hard-coded into the tracker. 
Make sure to give the domain or ip your tracker is on instead of 
my.tracker.

You can use either a dns name or an IP address in the tracker url.

3) associate .torrent with application/x-bittorrent on your web server

The way you do this is dependent on the particular web server you're using.

You must have a web server which can serve ordinary static files and is 
addressable from the internet at large.

4) put the newly made .torrent file on your web server

Note that the file name you choose on the server must end in .torrent, so 
it gets associated with the right mimetype.

5) put up a static page which links to the location you uploaded to in step 4

The file you uploaded in step 4 is linked to using an ordinary url.

6) start a downloader as a resume on the complete file

You have to run a downloader which already has the complete file, 
so new downloaders have a place to get it from. Here's an example -

./bittorrent-console.py --url http://my.server/myfile.torrent --saveas myfile.ext

Make sure the saveas argument points to the already complete file.

If you're running the complete downloader on the same machine or LAN as 
the tracker, give a --ip parameter to the complete downloader. The --ip 
parameter can be either an IP address or DNS name.

BitTorrent defaults to port 6881. If it can't use 6881, (probably because 
another download is happening) it tries 6882, then 6883, etc. It gives up 
after 6889.

7) you're done!

Now you just have to get people downloading! Refer them to the page you 
created in step 5.

BitTorrent can also publish whole directories - simply point
btmaketorrent.py at the directory with files in it, they'll be
published as one unit. All files in subdirectories will be included,
although files and directories named 'CVS', 'core', 'Thumbs.db',
'desktop.ini' and beginning with a dot ('.') are ignored.


Instructions for installation:
==============================

Instructions for Unix installation are in INSTALL.unix.txt

Instructions for Windows installation and creating Windows installers
are in BUILD.windows.txt
