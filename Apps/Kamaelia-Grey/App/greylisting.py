#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import socket

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.ConnectedServer import ServerCore

from Kamaelia.Internet.TCPServer import TCPServer
from Kamaelia.Internet.TimeOutCSA import NoActivityTimeout
from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter

from Kamaelia.Apps.Grey.Support import *

from Kamaelia.Apps.Grey.MailHandler import MailHandler
from Kamaelia.Apps.Grey.ConcreteMailHandler import ConcreteMailHandler
from Kamaelia.Apps.Grey.GreyListingPolicy import GreyListingPolicy
from Kamaelia.Apps.Grey.PeriodicWakeup import PeriodicWakeup
from Kamaelia.Apps.Grey.WakeableIntrospector import LoggingWakeableIntrospector

config_files = ["/usr/local/etc/Kamaelia/greylist.conf",
                "/usr/local/etc/greylist.conf",
                "/etc/Kamaelia/greylist.conf",
                "/etc/greylist.conf",
                "greylist.conf",
                "/usr/local/etc/Kamaelia/greylist.conf.dist",
                "/usr/local/etc/greylist.conf.dist",
                "/etc/Kamaelia/greylist.conf.dist",
                "/etc/greylist.conf.dist",
                "greylist.conf.dist" ]

default_config = { 'allowed_domains': [],
                   'allowed_sender_nets': [],
                   'allowed_senders': ['127.0.0.1'],
                   'port': 25,
                   "greylist_log": "greylist.log",
                   "greylist_debuglog" : "greylist-debug.log",
                   "inactivity_timeout": 60,
                   'serverid': 'Kamaelia-SMTP 1.0',
                   'servername': 'mail.example.com',
                   'smtp_ip': '192.168.2.9',
                   'smtp_port': 8025,
                   'whitelisted_nonstandard_triples': [],
                   'whitelisted_triples': []
        }

config_used = None
for config_file in config_files:
    try:
        lines = openConfig(config_file)
    except IOError:
        pass
    else:
        config_used = config_file
        break

if config_used is not None:
    config = parseConfigFile(lines,default_config)
else:
    config = default_config
    config_used = "DEFAULT INTERNAL"

class GreylistServer(ServerCore):
    logfile = config["greylist_log"]
    debuglogfile = config["greylist_debuglog"]
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = config["port"]
    class TCPS(TCPServer):
        CSA = NoActivityTimeout(ConnectedSocketAdapter, timeout=config["inactivity_timeout"], debug=False)
        
    # 
    # What does this code do?
    # It copies specifically enumerated configuration data
    # into a dynamically created new class called protocol.
    #
    classdict = {}

    for config_attribute in ('servername', 'serverid', 'smtp_ip',
                             'smtp_port', 'allowed_senders', 'allowed_sender_nets',
                             'allowed_domains', 'whitelisted_triples', ) :
        classdict[config_attribute] = getattr(config, config_attribute)

    protocol = type("Protocol", (GreyListingPolicy,) , classdict)

    # The above code replaces the code below. The above code could be
    # generalised further and made more flexible.
    if 0:
        class protocol(GreyListingPolicy):
            servername = config["servername"]
            serverid = config["serverid"]
            smtp_ip = config["smtp_ip"]
            smtp_port = config["smtp_port"]
            allowed_senders = config["allowed_senders"]
            allowed_sender_nets = config["allowed_sender_nets"] # Yes, only class C network style
            allowed_domains = config["allowed_domains"]
            whitelisted_triples = config["whitelisted_triples"]
            whitelisted_nonstandard_triples = config["whitelisted_nonstandard_triples"]

Pipeline(
    PeriodicWakeup(),
    LoggingWakeableIntrospector(logfile=config["greylist_debuglog"]),
).activate()

MailHandler.logfile = config["greylist_log"]
MailHandler.debuglogfile = config["greylist_debuglog"]

GreylistServer().run()
