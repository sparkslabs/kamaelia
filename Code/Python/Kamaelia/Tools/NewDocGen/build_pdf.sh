#!/bin/bash

./kamaelia-docs.py Kamaelia > Kamaelia_docs.rst
pandoc Kamaelia_docs.rst  -o Kamaelia_docs.pdf

./kamaelia-docs.py Axon > Axon_docs.rst
pandoc Axon_docs.rst  -o Axon_docs.pdf

cat Axon_docs.rst Kamaelia_docs.rst > AxonKamaelia_docs.rst
pandoc AxonKamaelia_docs.rst  -o AxonKamaelia_docs.pdf

echo "Docs built, to check:"
echo "okular kamaelia_docs.pdf"

