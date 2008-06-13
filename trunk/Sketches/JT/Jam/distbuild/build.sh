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
cp setup.py.src setup.py

# Get stuff from Axon and Kamaelia - this doesn't follow the naming
packages=`egrep -A 1000 START ../../../../Code/Python/Axon/setup.py|egrep -B1000 LAST`
packages="${packages}\n`egrep -A 1000 START ../../../../Code/Python/Kamaelia/setup.py|egrep -B1000 LAST`"
scripts=""
data="" 

setup_files=("../library/trunk/setup.py" "../application/trunk/setup.py")
for file in ${setup_files[@]}
do
    packages="${packages}\n`egrep -A 1000 STARTPACKAGES $file|egrep -B1000 LASTPACKAGES`"
    scripts="${scripts}\n`egrep -A 1000 STARTSCRIPTS $file|egrep -B1000 LASTSCRIPTS`"
    data="${data}\n`egrep -A 1000 STARTDATA $file|egrep -B1000 LASTDATA`"
done;

./revomit.py "$packages" "$scripts" "$data" setup.py

mv setup.py ../build/setup.py


cd ../build
python setup.py sdist --formats=gztar,zip


