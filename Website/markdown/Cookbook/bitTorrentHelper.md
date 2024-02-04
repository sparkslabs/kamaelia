---
pagename: Cookbook/bitTorrentHelper
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook/bitTorrentHelper
=========================

This cookbook recipe stems from my needing a tool to manage BitTorrent
clients for other applications. I required that the utility have the
following properties:\
\

1.  Control I/O through pipes (via stdin/stdout)
2.  If given a torrent filename it should start seeding/downloading the
    file
3.  \
