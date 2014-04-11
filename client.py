#!/bin/python

import socket
import argparse
import calendar, time
from Messages_pb2 import *

def send_hello(address, port):
	print "Connecting..."
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((address, port))
	ping_msg = Ping()
	ping_msg.timestamp = calendar.timegm(time.gmtime())
	client.send(ping_msg.SerializeToString.())

	while 1:
	    data = client.recv(512)
	    if ( data == 'q' or data == 'Q'):
	        client.close()
	        break;
	    else:
	        print "RECIEVED:" , data
	        data = raw_input ( "SEND( TYPE q or Q to Quit; 'Ping' for Ping Message ):" )
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

	send_hello(args.address, args.port)