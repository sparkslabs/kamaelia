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

# documentation builder script
#
# 1) updates svn checkouts of source code
# 2) ...and test suite
# 3) runs test suite
# 4) builds documentation
# 5) uploads to target webserver
#
# sends email if the build fails!

# ------------------------------------------------------------------------------
# general config

BUILDROOT="/home/warrenking/AutoDocGeneration"

BUILDDOCS="$BUILDROOT/DocGen/DocExtractor.py"
RUNTESTSUITE="$BUILDROOT/DocGen/TestSuiteRun.py"

# for uploading:
WEBSERVER_LOGIN="warrenking@shell.sourceforge.net"


# ------------------------------------------------------------------------------
# configuration for axon doc build

function axon_config () {
    # where the sources are
    SOURCE="$BUILDROOT/svn-checkouts/Axon-source"
    DOC_SOURCE="$SOURCE/Axon"
    TEST_SOURCE="$BUILDROOT/svn-checkouts/Axon-tests"

    # DocExtractor.py options
    DOC_OPTIONS="--urlprefix /Docs/Axon/ --promotetitles --root Axon --notjustcomponents --indexdepth 0 --footerinclude Docs/Axon-footer.html"
    DOC_OPTIONS="$DOC_OPTIONS --dumpsymbolsto $BUILDROOT/axon.symbols"

    # where to (temporarily) place output as it is generated
    TEST_OUTPUT="$BUILDROOT/generated/Axon-tests"
    TEST_OPTIONS="--root Axon"
    DOC_OUTPUT="$BUILDROOT/generated/Axon-docs"

    # where stuff should be placed on the web server
    DOC_DIR="/tmp/persistent/kamaelia/hotdocs/Docs/Axon"
    UPLOAD_DIR="/tmp/persistent/kamaelia/uploaded-axon-pydocs"
    BACKUP_DIR="/tmp/persistent/kamaelia/backed-up-axon-pydocs"
}

# ------------------------------------------------------------------------------
# configuration for kamaelia doc build

function kamaelia_config () {
    # where the sources are
    SOURCE="$BUILDROOT/svn-checkouts/Kamaelia-source"
    DOC_SOURCE="$SOURCE/Kamaelia"
    TEST_SOURCE="$BUILDROOT/svn-checkouts/Kamaelia-tests"

    # DocExtractor.py options
    DOC_OPTIONS="--urlprefix /Components/pydoc/ --root Kamaelia --footerinclude Components/pydoc-footer.html"
    if [ -f "$BUILDROOT/axon.symbols" ]; then
        DOC_OPTIONS="$DOC_OPTIONS --linktosymbols $BUILDROOT/axon.symbols"
    fi;

    # where to (temporarily) place output as it is generated
    TEST_OUTPUT="$BUILDROOT/generated/Kamaelia-tests"
    TEST_OPTIONS="--root Kamaelia"
    DOC_OUTPUT="$BUILDROOT/generated/Kamaelia-docs"

    # where stuff should be placed on the web server
    DOC_DIR="/tmp/persistent/kamaelia/hotdocs/Components/pydoc"
    UPLOAD_DIR="/tmp/persistent/kamaelia/uploaded-kamaelia-pydocs"
    BACKUP_DIR="/tmp/persistent/kamaelia/backed-up-kamaelia-pydocs"
}


# ------------------------------------------------------------------------------
# see bottom of file for what actually executes when this is run
# ------------------------------------------------------------------------------

function cleandir () {
    local DIRNAME="$1"

    if [ -d "$DIRNAME" ]; then
        rm -rf "$DIRNAME";
    fi
    mkdir "$DIRNAME";
}



function builddocs () {
    local IDENTITY="Build of '$1' documentation"
    local SOURCE="$2"
    local DOC_SOURCE="$3"
    local TEST_SOURCE="$4"
    local DOC_OUTPUT="$5"
    local TEST_OUTPUT="$6"
    local DOC_OPTIONS="$7"
    local WEBSERVER_UPLOAD_DIR="$8"
    local WEBSERVER_BACKUP_DIR="$9"
    local WEBSERVER_DOC_DIR="${10}"
    local TEST_OPTIONS="${11}"

    local rval

    echo -------------------------------------------------------------------------------
    echo "Building: $IDENTITY"
    echo -------------------------------------------------------------------------------

    # 1) update svn checkout
    echo 
    echo Updating source code svn checkout...
        svn update $SOURCE;
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    # 2) update test suite checkout
    echo 
    echo Updating test suite svn checkout...
        svn update $TEST_SOURCE;
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    # 3) generate test suite output
    echo 
    echo Cleaning test suite output destination dir...
        cleandir "$TEST_OUTPUT"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;

    echo 
    echo Running test suite...
        $RUNTESTSUITE $TEST_OPTIONS --outdir "$TEST_OUTPUT" --codebase "$SOURCE" "$TEST_SOURCE"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    # 4) rebuild docs
    
    echo 
    echo Building docs...
        cleandir "$DOC_OUTPUT"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
        
        $BUILDDOCS $DOC_OPTIONS --outdir "$DOC_OUTPUT" --includetestoutput "$TEST_OUTPUT" "$DOC_SOURCE"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    # 5) upload docs
    
    echo
    echo Cleaning upload destination...
        ssh "$WEBSERVER_LOGIN" "if [ -d \"$WEBSERVER_UPLOAD_DIR\" ]; then rm -rf \"$WEBSERVER_UPLOAD_DIR\"; fi;"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    echo
    echo Uploading...
        scp -rC "$DOC_OUTPUT" "$WEBSERVER_LOGIN:$WEBSERVER_UPLOAD_DIR"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;

    echo
    echo Removing previous backup...
        ssh "$WEBSERVER_LOGIN" "if [ -d \"$WEBSERVER_BACKUP_DIR\" ]; then rm -rf \"$WEBSERVER_BACKUP_DIR\"; fi;"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    echo
    echo Backing up data...
        ssh "$WEBSERVER_LOGIN" "if [ -d \"$WEBSERVER_DOC_DIR\" ]; then mv \"$WEBSERVER_DOC_DIR\" \"$WEBSERVER_BACKUP_DIR\"; fi;"
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    echo
    echo Making upload live...
        ssh "$WEBSERVER_LOGIN" "mv \"$WEBSERVER_UPLOAD_DIR\" \"$WEBSERVER_DOC_DIR\""
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
    echo
    echo Setting permissions on uploaded data...
        ssh "$WEBSERVER_LOGIN" "chmod -R a+rwx \"$WEBSERVER_DOC_DIR\"; "
        rval=$?; if [ ! $rval == 0 ]; then return $rval; fi;
    
}


# ------------------------------------------------------------------------------


if [ $# -lt 1 ]
then
    help=1;
    echo "Usage:"
    echo ""
    echo "$0 [Axon] [Kamaelia]"
    echo ""
    echo "    Axon     - build and upload Axon docs"
    echo "    Kamaelia - build and upload Kamaelia docs"
    echo ""
    exit 0;    
fi

failures=0
for buildset in "$@" 
do
    case $buildset in
        "Axon" )
              axon_config;
              builddocs "Axon" \
                  "$SOURCE" "$DOC_SOURCE" "$TEST_SOURCE" "$DOC_OUTPUT" "$TEST_OUTPUT" \
                  "$DOC_OPTIONS" "$UPLOAD_DIR" "$BACKUP_DIR" "$DOC_DIR" "$TEST_OPTIONS";
              if [ ! $? == 0 ]; then let failures++; fi;;
        "Kamaelia" )
              kamaelia_config;
              builddocs "Kamaelia" \
                  "$SOURCE" "$DOC_SOURCE" "$TEST_SOURCE" "$DOC_OUTPUT" "$TEST_OUTPUT" \
                  "$DOC_OPTIONS" "$UPLOAD_DIR" "$BACKUP_DIR" "$DOC_DIR" "$TEST_OPTIONS";
              if [ ! $? == 0 ]; then let failures++; fi;;
    esac
done

exit $failures
