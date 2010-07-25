#!/bin/sh
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
