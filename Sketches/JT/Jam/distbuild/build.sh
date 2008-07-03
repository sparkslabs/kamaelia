#! /bin/bash
# build.sh - Build a source distribution of Kamaelia Jam from a branch, tag or
# trunk
echo "Building the Kamaelia Jam distribution"
echo "Deleting current build directory"
rm -rf ../build
echo "Creating build directory"
mkdir ../build
echo "Copying Axon"
cp -r ../../../../Code/Python/Axon/Axon ../build
echo "Copying Kamaelia"
cp -r ../../../../Code/Python/Kamaelia/Kamaelia ../build

#These should be quiet - cp complains about moving .svn files
library_dir=${1:-"../library/trunk"}
if [ -d $library_dir ]   
then
    echo "Copying $library_dir"
    cp -r $library_dir/* ../build 2>/dev/null
else
    echo "Error: $library_dir is not a directory - exitting"
    exit 1
fi

application_dir=${2:-"../application/trunk"}
if [ -d $application_dir ]
then
    echo "Copying $application_dir"
    cp -r $application_dir/* ../build 2>/dev/null
else
    echo "Error: $application_dir is not a directory - exitting"
    exit 1
fi

echo "Creating setup file"

./revomit.py setup.py.src ../../../../Code/Python/Axon/setup.py ../../../../Code/Python/Kamaelia/setup.py ../library/trunk/setup.py ../application/trunk/setup.py setup.py
echo "Copying setup file"
mv setup.py ../build/setup.py
echo "Building sdist"
cd ../build
python setup.py sdist --formats=gztar,zip


