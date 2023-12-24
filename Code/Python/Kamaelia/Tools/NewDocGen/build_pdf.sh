#!/bin/bash

./kamaelia-docs.py > kamaelia_docs.rst
pandoc kamaelia_docs.rst  -o kamaelia_docs.pdf

echo "Docs built, to check:"
echo "okular kamaelia_docs.pdf"

