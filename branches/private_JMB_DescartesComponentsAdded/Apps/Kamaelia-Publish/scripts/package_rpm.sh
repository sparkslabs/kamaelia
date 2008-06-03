#!/bin/bash
#This should be executed from the directory above it

scripts/Publish.no-tar.sh
python setup-linux.py bdist --formats=rpm
