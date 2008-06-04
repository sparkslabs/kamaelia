#!/bin/bash
#This should be executed from the directory above it

scripts/Publish.notar.sh
python setup-linux.py bdist --formats=rpm
