#!/bin/sh
#make-unix.sh
#usage:  ./make-unix.sh [clean] [include-files]
#This script will first run scripts/publish.prepare.sh to assemble all of the relevant
#files into the assembly directory and strip the .svns from them.  It will then remove
#every pyc from the assembly directory.  Once this is finished, it will zip all the
#source files, byte compiled modules, and optimized modules as well as any other
#files that were named in include-files at the command line.  After this, the script
#will concatenate this zip file with zipheader.unix creating the executable (which
#will be moved to the zip directory).
#
#If clean was specified at the command line, the script will remove the assembly directory
#once it is finished.  It is recommended that you remove the assembly directory prior to
#running this script again.

./prepare.sh #assemble everything we need in the assembly directory
#python byte-compile.py urls.py main.py ServerConfig.py

if [ "$1" = "clean" ]
then
    CLEANUP=$1
    shift 1
else
    CLEANUP="empty"
fi



(
cd assembly
echo ">Removing any previously compiled modules"
rm -rfv assembly/*.pyc
echo ">Creating executable"
find . -name "*.py"|zip -@ kpublish.zip
find . -name "*.cfg"|zip -@g9 kpublish.zip
find . -name "*.ini"|zip -@g9 kpublish.zip
zip kpublish.zip data/.kp
#find . -name "*.pyc"|zip -@g kpublish.zip
#find . -name "*.pyo"|zip -@g kpublish.zip
cat zipheader.unix kpublish.zip > kpublish

if [ ! -d ../dist ]
then
    mkdir ../dist
fi

mv kpublish ../dist
chmod a+x ../dist/kpublish
)

if [ "$CLEANUP" = "clean" ]
then
    echo ">Cleaning up!"
    rm -rf assembly
fi
