#!/bin/python

import socket
import argparse
import calendar, time
from Messages_pb2 import *
from messageparser import *

mp = MessageParser()

# A little coloring...
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def ping(client):
	ping_msg = mp.CreateMessage(Message.Ping)
	ping_msg.Value.timestamp = ping_msg.Message.correlation_id
	client.send(ping_msg.Serialize())

def pong(client):
	pong_msg = mp.CreateMessage(Message.Pong)
	pong_msg.Value.original_timestamp = pong_msg.Message.correlation_id
	val = pong_msg.Serialize()
	client.send(val)
	
def send_person(client):
	person = mp.CreateMessage(Message.Person)
	person.Value.name = "Mark"
	person.Value.id = 456
	person.Value.email = "dude@place.com"
	person.Value.address = "123 Something"
	client.send(person.Serialize())

def connect(address, port):
	print "Connecting to %s:%s..." % (address, port)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((address, port))
	
	ping(client)

	print "(Press 'q' to quit')"
	while 1:
	    data = client.recv(MessageParser.MAX_MSG_SIZE)
	    if ( data == 'q' or data == 'Q'):
	        client.close()
	        break;
	    else:
	    	op = mp.TryDeserialize(data)
	    	if op == None:
	    		if "ERROR" in data:
	    			print FAIL + ("\treceived ERROR == '%s'" % data) + ENDC 
	        	else:
	        		print WARNING + ("\treceived (unknown) == '%s'" % data) + ENDC 
	        else:
	        	# TODO: Build some kind of message handler abstraction
	        	if op.Message.type == Message.Ping:
	        		print OKBLUE + "\treceived 'Ping'" + ENDC + ", Timestamp: %s" % op.Value.timestamp
	        	elif op.Message.type == Message.Pong:
	        		print OKGREEN + "\treceived 'Pong'" + ENDC + ", Original Timestamp: %s" % op.Value.original_timestamp
	        	elif op.Message.type == Message.Person:
	        		print OKGREEN + "\treceived 'Person'" + ENDC + ", Name/ID/Email: %s %s %s" % (op.Value.name, op.Value.id, op.Value.email)
	        	

	        inputdata = raw_input ( "[send command]:" )
	        
	        if (inputdata == 'Q' or inputdata == 'q'):
	            client.close()
	            return

	        if inputdata == 'Ping':
	        	ping(client)
	        elif inputdata == 'Pong':
	        	pong(client)
	        elif inputdata == 'Person':
	        	send_person(client)
	        else:
	        	client.send(inputdata)
	        

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--address", dest="address", default="localhost", 
		help="The address you would like to connect to")
	parser.add_argument("--port", dest="port", type=int, default=8044, 
		help="The port you would like to connect to")

	args = parser.parse_args()

	connect(args.address, args.port)