#!/bin/bash

CURR_DIR=`pwd`

cd ../../Kamaelia/
python setup.py sdist --formats=gztar -d "${CURR_DIR}/dist"
cd $CURR_DIR
