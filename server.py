#!/bin/python

import select
import socket
import argparse
from Messages_pb2 import *

def start_server(port):

	srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	srv.bind(('', int(port)))
	srv.listen(5)
	print "Listening on port %s" % port

	read_list = [srv]
	while True:
	    readable, writable, errored = select.select(read_list, [], [])
	    for s in readable:
	        if s is srv:
	            client_socket, address = srv.accept()
	            read_list.append(client_socket)
	            print "Connection from", address
	        else:
	            data = s.recv(1024)
	            if data:
	                s.send(data)
	                print "Received %s" % data
	            else:
	            	print "Closing connection from", address
	                s.close()
	                read_list.remove(s)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", dest="port", type=int, default=8044, help="The port you would like to bind to")
	args = parser.parse_args()
	start_server(args.port)
