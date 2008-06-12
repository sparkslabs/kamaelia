#!/bin/bash
#This script should be executed from the directory above it

scripts/Publish.notar.sh
python setup-mac.py py2app --iconfile="Mac/cat-icon.icns"
