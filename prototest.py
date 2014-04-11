#!/bin/python

from subprocess import call
from messageparser import MessageParser
import calendar, time
import google.protobuf


def serialize_person():
	print "Generating classes from protos..."
	call(["protoc", "--python_out=.", "Messages.proto"])
	
	messages_module = __import__("Messages_pb2", fromlist=[])
	p = messages_module.Person()
	p.id = 123
	p.name = "John"
	p.address = "Someplace"

	print "Instantiated Person class"

	val = p.SerializeToString()

	print "Serialized version is '%s'" % val.encode("hex")


def deserialize_person():
	val = "0a044d61726b107b2a0932322057696e746572".decode("hex")
	messages_module = __import__("Messages_pb2", fromlist=[])
	p =messages_module.Person()
	p.ParseFromString(val)
	print "Deserialized proto, Person is: %s" % p


def serialize_msg():
	messages_module = __import__("Messages_pb2", fromlist=[])
	msg = messages_module.Message()
	msg.type = messages_module.Message.Ping
	msg.correlation_id = 77144

	ping = msg.Extensions[messages_module.Ping.message]
	ping.timestamp = calendar.timegm(time.gmtime())

	msg_bytes = msg.SerializeToString()
	print "Serialized message is '%s'" % msg_bytes.encode("hex")

	ping.timestamp = 0

	msg_bytes = msg.SerializeToString() # double serialize!?!?

	print "Serialized message is '%s'" % msg_bytes.encode("hex")


def deserialize_msg():
	val = "080110d8da04520608e2f89d9a05".decode("hex")
	messages_module = __import__("Messages_pb2", fromlist=[])
	
	extension_map = { 
		messages_module.Message.Ping: messages_module.Ping.message, 
		messages_module.Message.Pong: messages_module.Pong.message 
	}

	msg = messages_module.Message()
	msg.ParseFromString(val)
	print "Deserialized message of type %s and correlation_id of %s " % (msg.type, msg.correlation_id)
	ping = msg.Extensions[extension_map[msg.type]]
	print "\t Ping timestamp is %s" % ping.timestamp


def msgparser_test():
	mp = MessageParser("08011017520608ecf49d9a05".decode("hex"))
	ping_msg = mp.Deserialize()
	print ping_msg[0].correlation_id

if __name__ == "__main__":
	serialize_person()
	deserialize_person()

	serialize_msg()
	deserialize_msg()

