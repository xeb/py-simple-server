#!/bin/python

import select
import socket
import argparse
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

def start_server(port):

	srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	srv.bind(('', int(port)))
	srv.listen(5)
	print HEADER + ("Listening on port %s" % port) + ENDC

	read_list = [srv]
	while True:
	    readable, writable, errored = select.select(read_list, [], [])
	    for s in readable:
	        if s is srv:
	            client_socket, address = srv.accept()
	            read_list.append(client_socket)
	            print HEADER + ("Connection from %s" % address[0]) + ENDC
	        else:
	            data = s.recv(MessageParser.MAX_MSG_SIZE)
	            if data:
		            msg = mp.TryDeserialize(data)

		            #TODO: Abstract message handlers
		            if msg == None:
		                s.send(data)
		                print WARNING + "[Unknown Message Received]" + (" %s" % data) + ENDC
		            elif msg.Message.type == Message.Ping:
		            	print OKGREEN + ("[Received Ping]") + ENDC + (", Timestamp = %s" % msg.Value.timestamp)
		            	pong = mp.CreateMessage(Message.Pong)
		            	pong.Value.original_timestamp = msg.Value.timestamp
		            	s.send(pong.Serialize())

		            elif msg.Message.type == Message.Pong:
		            	print OKBLUE + ("[Received Pong]") + ENDC + (", Timestamp = %s" % msg.Value.original_timestamp)
		            	ping = mp.CreateMessage(Message.Ping)
		            	ping.Value.timestamp = msg.Value.original_timestamp
		            	s.send(ping.Serialize())

		            elif msg.Message.type == Message.Person:
		            	print OKGREEN + "[Received Person]" + ENDC + (", Name,ID,Email = %s %s %s" % (msg.Value.name, msg.Value.id, msg.Value.email))
		            	person = mp.CreateMessage(Message.Person)
		            	person.Value.name = msg.Value.name
		            	person.Value.id = msg.Value.id + 1
		            	person.Value.email = msg.Value.email
		            	person.Value.address = msg.Value.address
		            	s.send(person.Serialize())

		            else:
		            	print FAIL + "[No Handler Mapped]" + ENDC + (", %s" % msg.Message.type)
		            	s.send("ERROR=1")

	            else:
	            	print FAIL + ("Closing connection from %s" % address[0]) + ENDC
	                s.close()
	                read_list.remove(s)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", dest="port", type=int, default=8044, help="The port you would like to bind to")
	args = parser.parse_args()
	start_server(args.port)
