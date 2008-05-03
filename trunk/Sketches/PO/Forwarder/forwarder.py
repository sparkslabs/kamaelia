#!/usr/bin/python

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# This code right here is quite dirty. The problem is that TCPServer does
# not handle the address of the clients which are being connected to it, and
# thus it seems to be impossible to get this information from a SimpleServer.
# 
# What I'm doing here is basically replacing the line where the address
# is being forgotten, and save it in a local variable. As I say, it's a 
# quick & really really really dirty fix for the demo :-(
# 
import Kamaelia.Internet.TCPServer as TCPServer
from Kamaelia.IPC import newReader

class FakeTCPServer(TCPServer.TCPServer):
	def __init__(self, *args, **kargs):
		super(FakeTCPServer,self).__init__(*args, **kargs)
	"""
	This is exactly the same code found in the original
	TCPServer, but saving "addr" as self.lastAddr.

	It should be worked around more cleanly, but not on
	Saturday for a quick demo! :-D
	"""
	def createConnectedSocket(self, sock):
		"""\
		Accepts the connection request on the specified socket and returns a
		ConnectedSocketAdapter component for it.
		"""
		tries = 0
		maxretries = 10
		gotsock=False
		newsock, addr = sock.accept()  # <===== THIS IS THE PROBLEM
		self.lastAddr = addr[0]
		self.send(newReader(self, ((self, "newconnection"), self.listener)), "_selectorSignal")

		gotsock = True
		newsock.setblocking(0)
		###      
		CSA = (self.CSA)(newsock,self.selectorService)
		return newsock, CSA

import Kamaelia.Chassis.ConnectedServer as ConnectedServer
ConnectedServer.TCPServer = FakeTCPServer # }:-D
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Now, the "normal code"
import re
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Axon.Ipc import producerFinished
from Axon.Component import component

class _ProtocolForwarder(component):
	Inboxes = {
			"inbox"    : "Information coming from the socket",
			"tosocket" : "Information coming from the user code",
			"control"  : "From component..."
	}
	Outboxes = {
			"outbox"     : "Information being sent to the socket",
			"fromsocket" : "Information sent to the user code",
			"signal"     : "From component..."
	}

	def _shutdown(self):
		if self.dataReady("control"):
			msg = self.recv("control")
			print msg
			self.send(msg, "signal")
			return isinstance(msg, producerFinished)

	def mainBody(self):
		if self._shutdown():
			return 0
		
		if self.dataReady("inbox"):
			data = self.recv("inbox")
			self.send(data, "fromsocket")
			return 1

		if self.dataReady("tosocket"):
			data = self.recv("tosocket")
			self.send(data, "outbox")
		return 1

class _NotAuthorizedProtocol(component):
	Inboxes = {
			"inbox"    : "Information coming from the socket",
			"control"  : "From component..."
	}
	Outboxes = {
			"outbox"     : "Information being sent to the socket",
			"signal"     : "From component..."
	}

	def mainBody(self):
		self.send("Not authorized!\n", "outbox")
		self.send(producerFinished(self), "signal")
		self.pause()
		return 0

class Forwarder(component):
	def __init__(self, public_port, control_port, remote_server, remote_port, *default_addresses):
		super(Forwarder, self).__init__()

		self.public_port       = public_port
		self.control_port      = control_port

		self.remote_server     = remote_server
		self.remote_port       = remote_port

		self.servers_activated = False

		self.allowed_addresses = list(default_addresses)

		self.publicServer      = ConnectedServer.SimpleServer(
			protocol       = self._buildPublicProtocol,
			port           = self.public_port
		)

		self.controlServer     = ConnectedServer.SimpleServer(
			protocol       = self._buildControlProtocol,
			port           = self.control_port
		)

		print "Listening on ports: %s and %s" % (
					self.public_port,
					self.control_port
				)

	def _buildPublicProtocol(self):
		addr = getattr(self.publicServer.server,'lastAddr','127.0.0.1')
		if addr in self.allowed_addresses:
			print "Accepted public petition from: %s" % addr
			client = TCPClient(
					self.remote_server, 
					port=self.remote_port
				)
			protocol = _ProtocolForwarder()
			self.link((protocol, "fromsocket"), (client,   "inbox"))
			self.link((client,   "outbox"),     (protocol, "tosocket"))
			self.link((client,   "signal"),     (protocol, "control"))

			client.activate()
			return protocol
		else:
			print "Rejected public petition from: %s" % addr
			return _NotAuthorizedProtocol()

	def _buildControlProtocol(self):
		addr = getattr(self.publicServer.server,'lastAddr','127.0.0.1')
		if addr == '127.0.0.1':
			print "Accepted control petition from: %s" % addr
			protocol = _ProtocolForwarder()
			self.link((protocol, "fromsocket"), (self, "inbox"))
			return protocol
		else:
			print "Rejected control petition from: %s" % addr
			return _NotAuthorizedProtocol()
		

	def _shutdown(self):
		if self.dataReady("control"):
			msg = self.recv("control")
			self.send(msg, "signal")
			return isinstance(msg, producerFinished)

	def mainBody(self):
		if self._shutdown():
			return 0

		if not self.servers_activated:
			self.publicServer.activate()
			self.controlServer.activate()
			self.servers_activated = True
			return 1

		if self.dataReady("inbox"):
			msg = self.recv("inbox")
			msg = msg.strip()
			self.parse_msg(msg)
		return 1

	def parse_msg(self, msg):
		# Only "accept ${IPv4 address}" are accepted
		digit_0_to_ff = r'(([0-1]?[0-9]{1,2})|2[0-4][0-9]|25[0-5])'
		regex         = r'^accept ((%(DIGIT)s\.){3}%(DIGIT)s)$' % {'DIGIT':digit_0_to_ff}
		matchobj      = re.match(regex,msg)
		if matchobj is not None:
			address = matchobj.groups()[0]
			if address in self.allowed_addresses:
				print "Already added address. Current addresses: %s" % self.allowed_addresses
			else:
				self.allowed_addresses.append(address)
				print "Accepted request. Current addresses: %s" % self.allowed_addresses
		else:
			print "Unaccepted request: %s" % msg

__kamaelia_components__  = ( Forwarder, )

if __name__ == '__main__':
	publicPort  = 1500
	controlPort = publicPort + 5

	Pipeline(
		ConsoleReader('>>> '),
		Forwarder(publicPort, controlPort, 'localhost', 80)
	).run()

