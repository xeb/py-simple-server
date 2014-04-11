
from Messages_pb2 import *

class MessageParser:
	def __init__():
		self.extension_map = { 
			Message.Ping: Ping.message, 
			Message.Pong: Pong.message,
			Message.Person: Person.message
		}

	def Deserialize(full_message):
		msg = Message()
		msg.ParseFromString(val)
		val = msg.Extensions[extension_map[msg.type]]
		return [ msg, val ]