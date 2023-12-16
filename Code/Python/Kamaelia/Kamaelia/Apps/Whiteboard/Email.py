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
#

import smtplib
#from email.MIMEText import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import socket
import os
import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess

class Email(threadedcomponent):
    # Sends e-mails from a specific mail account - could be modified to relay via servers, but that doesn't tend to work due to restrictions
    Inboxes = {
        "inbox" : "Receives a list containing details to send out e-mails with",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Sends status messages relating to sending e-mail",
        "signal" : "",
    }

    def __init__(self, server, port, fromaddr, username, password):
        super(Email, self).__init__()
        self.server = server
        self.port = port
        self.fromaddr = fromaddr
        self.username = username
        self.password = password

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        while self.shutdown():
            if self.dataReady("inbox"):
                # Input format: ['to address','subject','message body',['attachment filenames']]
                emaildata = self.recv("inbox")
                msg = MIMEMultipart()
                for filename in emaildata[3]:
                    file = open(filename)
                    data = file.read()
                    file.close()
                    diff = MIMEBase('application','zip')
                    diff.set_payload(data)
                    encode_base64(diff)
                    filelink = filename.split("/")
                    filelink = filelink[len(filelink) - 1]
                    diff.add_header('Content-Disposition','attachment',filename=filelink)
                    msg.attach(diff)
                msg['Subject'] = emaildata[1]
                msg['From'] = "Whiteboard Server"
                msg['To'] = emaildata[0]
                text = MIMEText(emaildata[2],'plain')
                msg.attach(text)
                try:
                    s = smtplib.SMTP(self.server,self.port)
                    s.ehlo()
                    s.starttls()
                    s.ehlo()
                    s.login(self.username,self.password)
                    s.sendmail(self.fromaddr,emaildata[0],msg.as_string())
                    self.send("sent","outbox")
                    s.quit()
                except smtplib.SMTPRecipientsRefused:
                    self.send("Recipient refused","outbox")
                except smtplib.SMTPHeloError:
                    self.send("Remote server responded incorrectly","outbox")
                except smtplib.SMTPSenderRefused:
                    self.send("From address rejected by server","outbox")
                except smtplib.SMTPDataError:
                    self.send("An unknown data error occurred","outbox")
                except smtplib.SMTPAuthenticationError:
                    self.send("The mail server login details specified are incorrect","outbox")
                except smtplib.SMTPException:
                    self.send("Server does not support STARTTLS","outbox")
                except RuntimeError:
                    self.send("SSL/TLS support not found","outbox")
                except socket.error:
                    e = sys.exc_info()[1]
                    self.send("Socket error: " + str(e), "outbox")
            time.sleep(0.5)
