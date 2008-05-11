#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

from distutils.core import setup    

setup(name = "Axon.STM",
      version = "1.0.1",
      description = "Axon: Software Transactional Memory",
      author = "Michael",
      author_email = "ms_@users.sourceforge.net",
      url = "http://kamaelia.sourceforge.net/",
      license = "Copyright (c)2007 Kamaelia Contributors, All Rights Reserved. Use allowed under MPL 1.1, GPL 2.0, LGPL 2.1",
      py_modules = ["Axon.STM",
                   ],
      long_description = """
Axon is a software component system. In Axon, components are active and
reactive, independent processing nodes responding to a CSP-like environment.
Systems are composed by creating communications channels (linkages) between
components. This package is a submodule of the Axon package providing *just*
the software transactional memory support via Axon.STM


Multivalue usage:
    from Axon.STM import Store

    S = Store()
    D = S.using("account_one", "account_two", "myaccount")
    D["account_one"].set(50)
    D["account_two"].set(100)
    D.commit()
    S.dump()

    D = S.using("account_one", "account_two", "myaccount")
    D["myaccount"].set(D["account_one"].value+D["account_two"].value)
    D["account_one"].set(0)
    D["account_two"].set(0)
    D.commit()
    S.dump()

Single valued usage:
    from Axon.STM import Store

    S = Store()
    greeting = S.usevar("hello")
    print repr(greeting.value)
    greeting.set("Hello World")
    greeting.commit()
    # ------------------------------------------------------
    print greeting
    S.dump()

"""
      )
