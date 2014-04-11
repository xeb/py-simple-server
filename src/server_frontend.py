#!/bin/python
import select, socket, argparse
import sys, os
from Messages_pb2 import *
from messageparser import *
from colorama import *

init()

# Backend Client methods
def connect_backend(address, port):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((address, port))
	return client

def connect_all_backends(addresses):
	backends = []
	for address in addresses.split(","):
		parts = address.split(":")
		try:
			backend = connect_backend(parts[0], int(parts[1]))
			backends.append(backend)
		except:
			print Fore.RED + ("\tfailed to connect to backend '%s:%s'" % (parts[0], parts[1])) + Style.RESET_ALL

	return backends

def receive_msg(mp, backend_skt):
	"""
	receive_msg is a completely blocking call
	"""
	data = backend_skt.recv(MessageParser.MAX_MSG_SIZE)
	if ( data == 'q' or data == 'Q'):
		backend_skt.close()
		return
	else:
		op = mp.TryDeserialize(data)
		if op == None:
			if "ERROR" in data:
				print Fore.RED + ("\treceived ERROR == '%s'" % data) + Style.RESET_ALL
			else:
				print Fore.YELLOW + ("\treceived (unknown) == '%s'" % data) + Style.RESET_ALL
			return None
		else:
			return op

def forward_message(mp, backend_skts, next_backend_index, op, client_skt):
	"""
	forward_message will round robin a message
	"""
	if next_backend_index >= len(backend_skts):
		print "Wrong!  next_backend_index is too large, should be less than %s" % len(backend_skts)
		return

	backend_skt = backend_skts[next_backend_index]
	next_backend_index = next_backend_index + 1
	if next_backend_index >= len(backend_skts):
		next_backend_index = 0

	result = forward_message_to_single(mp, backend_skt, op, client_skt)

	# If we could not forward, remove that backend & try again...
	if result == False:
		print Fore.MAGENTA + "Lost Connection to BACK, REMOVING!!!" + Style.RESET_ALL
		backend_skts.remove(backend_skt)

		# recurisve call to get the message over, don't wait!
		next_backend_index = next_backend_index - 1
		forward_message(mp, backend_skts, next_backend_index, op, client_skt)

	return next_backend_index

def forward_message_to_single(mp, backend_skt, op, client_skt):
	try:
		backend_skt.send(op.Message.SerializeToString())
	except Exception as inst:
		print Fore.RED + (" Exception == '%s'" % inst) + Style.RESET_ALL
		return False

	response = receive_msg(mp, backend_skt)
	# print "[Received Response from Backend] %s" % str(response.Message.correlation_id)
	msg = None
	try:
		msg = response.Message.SerializeToString()
		client_skt.send(msg)
		return True
	except:
		if msg == None:
			print "No message serialized..."
			return False

def start_server(mp, port, backends, update_backends=None):
	srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	srv.bind(('', int(port)))
	srv.listen(5)
	print Fore.MAGENTA + ("Listening on port %s" % port) + Style.RESET_ALL

	backend_skts = connect_all_backends(backends)
	orig_backend_count = len(backends.split(","))
	print Fore.MAGENTA + ("Connected all to %s" % (backends)) + Style.RESET_ALL

	read_list = [srv]
	next_backend_index = 0
	while True:

		# Update the backends address list
		orig_backends = backends
		if update_backends != None:
			backends = update_backends(backends)

		# Re-connect to BACKs if we have a new backends list (new or changed servers)
		if orig_backends != backends:
			print Fore.MAGENTA + "Reconnecting backends... " + Style.RESET_ALL
			backend_skts = connect_all_backends(backends)
			print Fore.MAGENTA + "There are now %s hosts active of the %s original configured " % (len(backend_skts), orig_backend_count) + Style.RESET_ALL
			next_backend_index = 0

		readable, writable, errored = select.select(read_list, [], [])
		for client_skt in readable:
			if client_skt is srv:
				client_socket, address = srv.accept()
				read_list.append(client_socket)
				print Fore.MAGENTA + ("Connection from %s" % address[0]) + Style.RESET_ALL
			else:
				data = client_skt.recv(MessageParser.MAX_MSG_SIZE)
				if data:
					op = mp.TryDeserialize(data)

					if op == None:
						print Fore.YELLOW + "[Unknown Message Received]" + (" %s" % data) + Style.RESET_ALL
						client_skt.close()
						read_list.remove(client_skt)
					else:
						# print "Getting backend %s with length of %s" % (next_backend_index, len(backend_skts))
						next_backend_index = forward_message(mp, backend_skts, next_backend_index, op, client_skt)

				else:
					print Fore.RED + ("Closing connection from %s" % address[0]) + Style.RESET_ALL
					client_skt.close()
					read_list.remove(client_skt)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--name", dest="name", default="FRONT", help="The service name")
	parser.add_argument("--port", dest="port", default="8050", help="The port you would like to bind to")
	parser.add_argument("--backends", dest="backends", default="localhost:8040", help="The address:port comma-separated backends you would like to use")
	args = parser.parse_args()
	mp = MessageParser(args.name)
	start_server(mp, "8050" if args.port == "" else args.port, args.backends)
