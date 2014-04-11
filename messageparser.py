
from Messages_pb2 import *
import calendar, time

class MessageResult:
	def __init__(self, message, value):
		self.Message = message
		self.Value = value

class MessageParser:
	def __init__(self):
		self.extension_map = { 
			Message.Ping: Ping.message, 
			Message.Pong: Pong.message,
			Message.Person: Person.message
		}

	def Deserialize(self, full_message):
		msg = Message()
		msg.ParseFromString(full_message)
		val = msg.Extensions[self.extension_map[msg.type]]
		return MessageResult(msg, val)

	def CreateMessage(self, type, correlation_id=0):
		
		# default correlation_id to timestamp
		if correlation_id == 0:
			correlation_id = calendar.timegm(time.gmtime())

		msg = Message()
		msg.type = type
		msg.correlation_id = correlation_id
		val = msg.Extensions[self.extension_map[msg.type]]

		return MessageResult(msg, val)