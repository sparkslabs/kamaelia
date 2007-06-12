#!/bin/sh

/home/warrenking/AutoDocGeneration/mailonfail.sh \
    "Axon documentation automatic generation for website" \
    warrenking@users.sourceforge.net \
    kamaelia-commits@lists.sourceforge.net \
    kamaelia-commits@lists.sourceforge.net \
    /home/warrenking/AutoDocGeneration/build_and_upload.sh Axon

/home/warrenking/AutoDocGeneration/mailonfail.sh \
    "Kamaelia documentation automatic generation for website" \
    warrenking@users.sourceforge.net \
    kamaelia-commits@lists.sourceforge.net \
    kamaelia-commits@lists.sourceforge.net \
    /home/warrenking/AutoDocGeneration/build_and_upload.sh Kamaelia
