#! /usr/bin/env python
from distutils.core import setup
setup(name = "Kamaelia Jam Application",
      version = "0.1a1",
      scripts = [
                 "jam", #STARTSCRIPTS LASTSCRIPTS
                ],
      data_files = [("share/kamaelia/jam/pd", ["PD/PureJam.pd"]), #STARTDATA
                    ("share/kamaelia/jam/samples",
                     ["Samples/12910_sweet_trip_mm_clap_mid.wav",
                      "Samples/12911_sweet_trip_mm_hat_cl.wav",
                      "Samples/12912_sweet_trip_mm_hat_op.wav",
                      "Samples/12914_sweet_trip_mm_kick_lo.wav",
                      "Samples/__details_and_attribution.txt"
                     ]) #LASTDATA
                    ]
      )
