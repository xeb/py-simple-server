#!/bin/python

import socket
import argparse
import calendar, time
from Messages_pb2 import *
from messageparser import *
from colorama import *

init()

mp = MessageParser("CLIENT")

def ping(client):
    ping_msg = mp.CreateMessage(Message.Ping)
    ping_msg.Value.timestamp = ping_msg.Message.correlation_id
    client.send(ping_msg.Serialize())

def pong(client):
    pong_msg = mp.CreateMessage(Message.Pong)
    pong_msg.Value.original_timestamp = pong_msg.Message.correlation_id
    val = pong_msg.Serialize()
    client.send(val)

def send_person(client):
    person = mp.CreateMessage(Message.Person)
    person.Value.name = "Mark"
    person.Value.id = 456
    person.Value.email = "dude@place.com"
    person.Value.address = "123 Something"
    client.send(person.Serialize())

def connect(address, port, sendall):
    print "Connecting to %s:%s..." % (address, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, port))

    ping(client)

    cmds = []
    if sendall:
        cmds.extend(['Ping','Person']) # TODO make dynamic
    else:
        print "(Press 'q' to quit')"

    while 1:
        data = client.recv(MessageParser.MAX_MSG_SIZE)
        if ( data == 'q' or data == 'Q'):
            client.close()
            break;
        else:
            op = mp.TryDeserialize(data)
            if op == None:
                if "ERROR" in data:
                    print Fore.RED + ("\treceived ERROR == '%s'" % data) + Style.RESET_ALL
                else:
                    print Fore.YELLOW + ("\treceived (unknown) == '%s'" % data) + Style.RESET_ALL
            else:
                # TODO: Build some kind of message handler abstraction
                if op.Message.type == Message.Ping:
                    print Fore.BLUE + Style.BRIGHT + "\treceived 'Ping'" + Style.RESET_ALL + ", Timestamp: %s" % op.Value.timestamp + \
                        Fore.YELLOW + "\nLog:\n%s" % op.Message.log + Style.RESET_ALL
                elif op.Message.type == Message.Pong:
                    print Fore.GREEN + "\treceived 'Pong'" + Style.RESET_ALL + ", Original Timestamp: %s" % op.Value.original_timestamp + \
                        Fore.YELLOW + "\nLog:\n%s" % op.Message.log + Style.RESET_ALL
                elif op.Message.type == Message.Person:
                    print Fore.GREEN + "\treceived 'Person'" + Style.RESET_ALL + ", Name/ID/Email: %s %s %s" % (op.Value.name, op.Value.id, op.Value.email) + \
                        Fore.YELLOW + "\nLog:\n%s" % op.Message.log + Style.RESET_ALL

            if sendall and len(cmds) > 0:
                inputdata = cmds[0]
                print inputdata
                cmds.pop(0)
            elif sendall and len(cmds) == 0:
                print Fore.GREEN + "\nAll done!\n\n" + Style.RESET_ALL
                return
            else:
                inputdata = raw_input ( "pysimserv$ " )

                if (inputdata == 'Q' or inputdata == 'q'):
                    client.close()
                    return

            if inputdata == 'Ping':
                ping(client)
            elif inputdata == 'Pong':
                pong(client)
            elif inputdata == 'Person':
                send_person(client)
            else:
                ping(client)
                print Fore.YELLOW + "\tSend 'Ping' or 'Pong' or 'Person'\nSince you don't know what you are doing, I'm sending a Ping..." + Style.RESET_ALL


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sendall',dest='sendall',action='store_true',
        help="Don't start a console.  Instead send all Message types")
    parser.add_argument("--address", dest="address", default="localhost:8044",
        help="The address you would like to connect to")

    args = parser.parse_args()
    parts = args.address.split(":")
    connect(parts[0], int(parts[1]), args.sendall)
