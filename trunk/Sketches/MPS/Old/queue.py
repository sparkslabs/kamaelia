class Queue(list):
	def shift(self):
		if self == []:
		   return None
		result = self[0]
		del self[0]
		return result
	def push(self, value):
		self.append(value)

class MessageQueue(Queue):
	def read(Queue):
		raise NotImplementedError
	def write(Queue):
		raise NotImplementedError

class InboundQueue(MessageQueue):
	def read(Queue):
		"Should be defined in this class"
class OutboundQueue(MessageQueue):
	def write(Queue, *Messages):
		"Should be defined in this class"

