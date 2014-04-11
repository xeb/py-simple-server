#!/bin/python
import select, socket, argparse, time
import sys, os
from Messages_pb2 import *
from messageparser import *
from colorama import *
import dns.resolver
import server_frontend # use the old frontend
import get_backends

service = "pysimserv"

def update_backends(dns, dns_port, consul, pattern, backends):
	"""
	update_backends needs to return a list of backends to use, but is given the original list
	we don't want to query consul every tick, so we do modulus every 5 seconds to see what's active
	"""
	if round(time.time(), 0) % 5 == 0:
		backends = get_backends.discover(dns, dns_port, consul, service, pattern)
	return backends

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--name", dest="name", default="FRONT", help="The service name")
	parser.add_argument("--port", dest="port", default="8050", help="The port you would like to bind to")
	parser.add_argument("--dns", dest="dns", default="", help="The name to resolve over DNS")
	parser.add_argument("--dns_port", dest="dns_port", default="8040", help="The port to use for DNS")
	parser.add_argument("--consul", dest="consul", default="localhost:8040", help="The consul agent used to query")
	parser.add_argument("--pattern", dest="pattern", default="back", help="The pattern to look for in Concul entries")
	args = parser.parse_args()
	mp = MessageParser(args.name)

	print "DNS is %s : %s" % (args.dns, args.dns_port)
	
	backends = get_backends.discover(args.dns, args.dns_port, args.consul, service, args.pattern)
	print "backends are %s " % backends

	port = "8050" if args.port == "" else args.port
	print "using port %s" % port

	server_frontend.start_server(mp, port, backends, lambda b: update_backends(args.dns, args.dns_port, args.consul, args.pattern, b))
