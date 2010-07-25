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

LOCKFILE=/tmp/.lock_restartStreamer

WORKINGDIR=/home/warrenking/Kamaelia/Sketches/filereading
TASK=./SimpleMultiFileStreamer.py
REDIRECTS="\>\>stdout.log 2\>\>errout.log"

SECONDS_RESTART_PAUSE=1

pwd >>/tmp/stdout


stoptask()
{
    # check if lock file exists, if it does, extract the PID in it
    # if that PID is still running, kill it
    if [ -f $LOCKFILE ]
    then
        pidtokill=`cat $LOCKFILE`
        pids=`ps aux | grep "$TASK" | grep -v grep | awk '{print $2}' | grep \^$pidtokill\$`
        for p in $pids
        do
            kill -9 $p
        done
    fi
}

starttask()
{
    # check if lock file exists, if it does, extract the PID in it
    # only start task if not already running
    if [ -f $LOCKFILE ]
    then
        thepid=`cat $LOCKFILE`
        pids=`ps aux | grep "$TASK" | grep -v grep | awk '{print $2}' | grep \^$thepid\$`
    fi

    if [ -z $pids ]
    then
        # start the task
        pushd .
        cd $WORKINGDIR
        $TASK $REDIRECTS &
        popd
            
        # log process id for the task we just started
        echo $! > $LOCKFILE
    else
        echo Task not started ... it is already running.
    fi

}


case "$1" in
    start) starttask ;;
    stop)  stoptask  ;;
    restart) stoptask
             sleep $SECONDS_RESTART_PAUSE
             starttask ;;
    *) echo options:
       echo   start \| restart \| stop
       echo
       echo   start   - starts, if not already running
       echo   restart - stops if already running then starts again
       echo   stop    - stops if running
esac


