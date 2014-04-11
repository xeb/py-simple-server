#!/bin/python
import select, socket, argparse
import sys, os
from Messages_pb2 import *
from messageparser import *
from colorama import *

init()

mp = None

def handle_person(msg, s):
	print Fore.GREEN + "[Received Person]" + Style.RESET_ALL + (", Name,ID,Email = %s %s %s" % (msg.Value.name, msg.Value.id, msg.Value.email))
	person = mp.CreateMessage(Message.Person)
	person.Value.name = msg.Value.name
	person.Value.id = msg.Value.id + 1
	person.Value.email = msg.Value.email
	person.Value.address = msg.Value.address
	s.send(person.Serialize())

def handle_ping(msg, s):
	print Fore.GREEN + ("[Received Ping]") + Style.RESET_ALL + (", Timestamp = %s" % msg.Value.timestamp)
	pong = mp.CreateMessage(Message.Pong)
	pong.Value.original_timestamp = msg.Value.timestamp
	s.send(pong.Serialize())

def handle_pong(msg, s):
	print Fore.BLUE + Style.BRIGHT + ("[Received Pong]") + Style.RESET_ALL + (", Timestamp = %s" % msg.Value.original_timestamp)
	ping = mp.CreateMessage(Message.Ping)
	ping.Value.timestamp = msg.Value.original_timestamp
	s.send(ping.Serialize())

def start_server(port):
	srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	srv.bind(('', int(port)))
	srv.listen(5)
	print Fore.MAGENTA + ("Listening on port %s" % port) + Style.RESET_ALL

	read_list = [srv]
	while True:
	    readable, writable, errored = select.select(read_list, [], [])
	    for s in readable:
	        if s is srv:
	            client_socket, address = srv.accept()
	            read_list.append(client_socket)
	            print Fore.MAGENTA + ("Connection from %s" % address[0]) + Style.RESET_ALL
	        else:
	            data = s.recv(MessageParser.MAX_MSG_SIZE)
	            if data:
		            msg = mp.TryDeserialize(data)

		            #TODO: Abstract message handlers
		            if msg == None:
		                print Fore.YELLOW + "[Unknown Message Received]" + (" %s" % data)
		                print "Sending Ping..." + Style.RESET_ALL
		                handle_ping(msg, s)
		            elif msg.Message.type == Message.Ping:
		            	handle_ping(msg, s)
		            elif msg.Message.type == Message.Pong:
		            	handle_pong(msg, s)
		            elif msg.Message.type == Message.Person:
		            	handle_person(msg, s)
		            else:
		            	print Fore.RED + "[No Handler Mapped]" + Style.RESET_ALL + (", %s" % msg.Message.type)
		            	s.send("ERROR=1")

	            else:
	            	print Fore.RED + ("Closing connection from %s" % address[0]) + Style.RESET_ALL
	                s.close()
	                read_list.remove(s)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--name", dest="name", default="BACK", help="The service name")
	parser.add_argument("--port", dest="port", type=int, default=8040, help="The port you would like to bind to")
	args = parser.parse_args()
	mp = MessageParser(args.name)
	start_server(args.port)
