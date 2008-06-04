#!/bin/sh

scripts/Publish.notar.sh
python byte-compile.py urls.py main.py ServerConfig.py
zip kpublish.zip urls.py urls.pyc main.py main.pyc ServerConfig.py ServerConfig.pyc Kamaelia Axon WsgiApps
cat zipheader.unix kpublish.zip > kpublish
