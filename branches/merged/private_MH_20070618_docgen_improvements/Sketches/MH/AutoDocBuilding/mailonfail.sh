#!/bin/sh
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

if [ $# -lt "5" ]; then
    echo "Usage:"
    echo
    echo "  mailonfail <what(subject)> <from> <to> <reply> cmd args..."
    echo
    exit 0;
fi;

SUBJECT=$1
MAILFROM=$2
MAILTO=$3
MAILREPLY=$4

shift
shift
shift
shift

echo "$@"
LOG=`"$@"`
rval=$?
if [ ! $rval == 0 ]; then

    echo Failed. Sending email...
    (
        echo "This is an automated email reporting a failure."
        echo
        echo "Log of output:"
        echo "--------------"
        echo
        echo "$LOG"
    ) | mail -s "FAILED: $SUBJECT" \
             -r "$MAILFROM" \
             -R "$MAILREPLY" \
             "$MAILTO"
    echo 'mail' return code = $?
fi;
