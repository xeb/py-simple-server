#!/bin/sh

import argparse
import time
from subprocess import call
from Messages_pb2 import *
from messageparser import MessageParser

class Tests():

	def test_correlation_id(self):
		mp = MessageParser("test")
		pong = mp.CreateMessage(Message.Pong)
		pong.Value.original_timestamp = 1;
		strval1 = pong.Message.SerializeToString().encode("hex")

		time.sleep(1)

		pong = mp.CreateMessage(Message.Pong)
		pong.Value.original_timestamp = 1;
		strval2 = pong.Message.SerializeToString().encode("hex")

		self.assert_msg(lambda: strval1 != strval2, "Expected strval1 != strval2, both are %s" % strval1)


	def assert_msg(self, condition, msg):
		try:
			assert condition()
		except AssertionError as e:
			e.args += ('Message', msg)
			raise
