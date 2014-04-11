#!/bin/sh

import argparse
import time
from subprocess import call
from Messages_pb2 import *
from messageparser import MessageParser

class Tests():

	def test_deserialize(self):
		mp = MessageParser()
		ping_msg = mp.Deserialize("08011017520608ecf49d9a05".decode("hex"))
		
		self.assert_msg(lambda: ping_msg.Message.correlation_id == 23, "Expected correlation_id to be 23")

	def test_serialize(self):
		mp = MessageParser()
		pong = mp.CreateMessage(Message.Pong, correlation_id=666)
		pong.Value.original_timestamp = 1397195273
		strval = pong.Message.SerializeToString().encode("hex")

		self.assert_msg(lambda: strval == "0802109a055a060889849e9a05", "Expected %s" % strval)

	def test_correlation_id(self):
		mp = MessageParser()
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




	