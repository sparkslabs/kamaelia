---
pagename: ActiveFileProcessor
last-modified-date: 2008-11-16
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Active File Processor
=====================

(Full Documentation for this will be written shortly.)\

### What is it?

It\'s designed to sit on the backend of a website that accepts images
and videos from users, and transodes them to sizes suitable for the web,
and to flash video.\
\
The code is however more general, and could in fact be used for anything
that needs to watch a bunch of directories and do interesting things
(hence the name of this page).\

### **What does it do right now?**

At present, the code does this:\

-   Has directory watchers
-   When a file is added to the source directory, the first processor
    splits it off into different directories based on file type
-   Another does image size conversion, cropping etc,
-   Another does video conversion to flash video.
-   The result is images & videos placed into a directory for
    moderation.

It\'s designed to run as a backend system that sits in the background
running continuously.\
\

Draft Installation Instructions
===============================

Install Image Magick as normal.\

### **Download and install libamr**

This is to support transcoding of video from mobile phones.\
\
Originally from
[http://www.penguin.cz/\~utx/amr](http://www.penguin.cz/%7Eutx/amr)

>     curl -O http://ftp.penguin.cz/pub/users/utx/amr/amrnb-7.0.0.2.tar.bz2
>     tar jxvf amrnb-7.0.0.2.tar.bz2
>     cd amrnb-7.0.0.2/
>     ./configure --libdir /usr/lib/
>     make  #   -- requires wget to build
>     sudo su
>     make install
>     ldconfig

### **Download and install ffmpeg**

This is used by the transcode engine to transcode videos. You can
however plug something in its place relatively easily.\

>     svn co svn://svn.mplayerhq.hu/ffmpeg/trunk ffmpeg-trunk
>     cd ffmpeg-trunk/
>     ./configure --enable-nonfree --enable-libamr-nb
>     make
>     sudo su
>     make install
>     ldconfig

### **Download, install and configure the transcode engine.**

Grab the code and install it\

>     curl -O http://www.kamaelia.org/release/Kamaelia-FileProcessor-0.1.0.tar.gz
>     tar zxvf Kamaelia-FileProcessor-0.1.0.tar.gz
>     cd Kamaelia-FileProcessor-0.1.0
>     sudo python setup.py install

**Create uploads and moderation directories for transcode/moderation
pipeline**\

>     cd /tmp # or whereever you prefer - you'll need to change a config option no matter what :-)
>     mkdir incoming
>     mkdir -p uploads/images uploads/videos
>     mkdir -p moderate/images moderate/videos

Make everything writeable by the webuser.\
\
**Configure it**\
Copy the default config to one you want to edit\

>     cp /etc/batch_converter.conf.dist /etc/batch_converter.conf

Then edit **/etc/batch\_converter.conf** such that the following
lines/config options \...\

>     # main_incoming_queue /tmp/uploads
>     # image_queue /tmp/uploads/images 
>     # video_queue /tmp/uploads/videos 
>     # image_moderation_queue /tmp/moderate/images
>     # video_moderation_queue /tmp/moderate/videos

\... get changed to:\

>     # main_incoming_queue /tmp/incoming
>     # image_queue /tmp/uploads/images 
>     # video_queue /tmp/uploads/videos 
>     # image_moderation_queue /tmp/moderate/images
>     # video_moderation_queue /tmp/moderate/video

\... or whatever you changed it to\...\
\
**Grab and install PIL (\"python imaging library\")**\
Download from\

> <http://effbot.org/downloads/Imaging-1.1.6.tar.gz>\

Unpack and install\

>     tar zxvf Imaging-1.1.6.tar.gz
>     cd Imaging-1.1.6/
>     sudo python setup.py install --force

Note: PIL requires the ability to build tcl/tk apps for odd reasons. You
may find you need to install that dependency before PIL will build.
Hence the recommendation to use am .rpm or .deb file if you can.\
\
