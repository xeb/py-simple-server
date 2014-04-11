#!/bin/python

import socket
import argparse
import calendar, time
from Messages_pb2 import *
from messageparser import *

def connect(address, port):
	print "Connecting to %s:%s..." % (address, port)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((address, port))
	
	mp = MessageParser()
	mp.CreateMessage(Message.Ping, )

	ping_msg = Ping()
	ping_msg.timestamp = calendar.timegm(time.gmtime())
	client.send(ping_msg.SerializeToString.())
	print "(Press 'q' to quit')"
	while 1:
	    data = client.recv(512)
	    if ( data == 'q' or data == 'Q'):
	        client.close()
	        break;
	    else:
	        print "[received]:" , data
	        data = raw_input ( "[send command]:" )
	        if (data <> 'Q' and data <> 'q'):
	            client.send(data)
	        else:
	            client.send(data)
	            client.close()
	            break;

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--address", dest="address", default="localhost", 
		help="The address you would like to connect to")
	parser.add_argument("--port", dest="port", type=int, default=8044, 
		help="The port you would like to connect to")

	args = parser.parse_args()

	connect(args.address, args.port)