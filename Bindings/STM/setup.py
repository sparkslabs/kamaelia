#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------

from distutils.core import setup    

setup(name = "Axon.STM",
      version = "1.0.1",
      description = "Axon: Software Transactional Memory",
      
      author = "Kamaelia Contributors.",
      author_email = "sparks.m@gmail.com",
      url = "http://www.kamaelia.org/STM.html",
      license ="Apache Software License",
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
