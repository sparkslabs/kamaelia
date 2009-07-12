#!/usr/bin/python

import socket

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Seq import Seq

from Kamaelia.Apps.Europython09.BB.Support import readUsers
from Kamaelia.Apps.Europython09.BB.LineOrientedInputBuffer import LineOrientedInputBuffer
from Kamaelia.Apps.Europython09.BB.Authenticator import Authenticator
from Kamaelia.Apps.Europython09.BB.UserStatePersistence import UserRetriever, StateSaverLogout
from Kamaelia.Apps.Europython09.BB.MessageBoardUI import MessageBoardUI

def CompositeBulletinBoardProtocol(**argd):
    ConnectionInfo = {}
    ConnectionInfo.update(argd)
    return Pipeline(
              LineOrientedInputBuffer(),
              Seq(
                  Authenticator(State = ConnectionInfo, users = users),
                  UserRetriever(State = ConnectionInfo),
                  MessageBoardUI(State = ConnectionInfo),
                  StateSaverLogout(State = ConnectionInfo),
              )
           )

users = readUsers()

ServerCore(protocol=CompositeBulletinBoardProtocol,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=1600).run()


