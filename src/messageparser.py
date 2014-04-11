
from Messages_pb2 import *
from colorama import *
import calendar, time
import socket
import sys, os

class MessageResult: #TODO: get rid of this, multiple returns
	def __init__(self, message, value):
		self.Message = message
		self.Value = value

	def Serialize(self):
		return self.Message.SerializeToString()

	def LogHost(self, service_name):
		data = str.join(" ", sys.argv)
		secure = "UNKNOWN"
		if "IS_SECURE" in os.environ:
			secure = os.environ["IS_SECURE"]

		# data = data + "\n[%s] (%s)" % (socket.gethostname(), str.join("/", [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]))
		data = "(%s : " % (service_name) + Fore.RED + ("[%s]" % socket.gethostname()) + Fore.YELLOW + ") " + data
		self.Message.log = "%s\n%s" % (data, self.Message.log)

class MessageParser:

	MAX_MSG_SIZE = 1024
	service_name = "N/A"

	def __init__(self, name):
		self.service_name = name
		self.extension_map = {
			Message.Ping: Ping.message,
			Message.Pong: Pong.message,
			Message.Person: Person.message
		}

	def Deserialize(self, full_message):
		msg = Message()
		msg.ParseFromString(full_message)
		val = msg.Extensions[self.extension_map[msg.type]]
		result = MessageResult(msg, val)
		return result

	def TryDeserialize(self, full_message):
		try:
			msg = self.Deserialize(full_message)
			msg.LogHost(self.service_name)
			return msg
		except:
			return None


	def CreateMessage(self, type, correlation_id=0):

		# default correlation_id to timestamp
		if correlation_id == 0:
			correlation_id = calendar.timegm(time.gmtime())

		msg = Message()
		msg.type = type
		msg.correlation_id = correlation_id
		val = msg.Extensions[self.extension_map[msg.type]]

		result = MessageResult(msg, val)
		result.LogHost(self.service_name)
		return result
