#!/bin/sh

import argparse
import time
from subprocess import call
from Messages_pb2 import *
from messageparser import MessageParser
from tests import Tests

def run_tests():
	tests = Tests()
	tests.test_correlation_id()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("action", choices=("test", "build"))
	args = parser.parse_args()

	# This doesn't work because there is a dependency on Messages_pb2
	# if args.action == "build":
	# 	call(["protoc", "--python_out=.", "Messages.proto"])

	if args.action == "test":
		run_tests()
