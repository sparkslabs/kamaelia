#!/bin/bash

CURR_DIR=`pwd`

cd ../../Axon/
python setup.py sdist --formats=gztar -d "${CURR_DIR}/dist"
cd $CURR_DIR
