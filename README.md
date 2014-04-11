<a href="https://travis-ci.org/xeb/py-simple-server">
<img src="https://api.travis-ci.org/xeb/py-simple-server.svg" />
</a>

Python Simple Server
================

A simple Python client/server that uses a basic protobuf protocol to communicate.  There is a sample of message definitions contained within the Messages.proto file.  This project has been modified to demonstrate a sample of interconnectivity using Docker containers. It also includes a service stack using Kubernetes as a PaaS-like layer.

# Execution

## A quick Docker test...
If you just want to see all this stuff work without even downloading this repo, you can pull the container & run a test like this:
```
docker run -it xebxeb/pysimserv --type=test
```
You should then see the following:
1) the BACK server started within the container
2) the FRONT server started within the container
3) the client.py started within the container & send a few messages then exit
4) all the python processes being killed off

No ports are exposed during this test -- it is completely within the container 

## Build

```
make
```
This will:
* generate the Messages_pb2.py file from Messages.proto
* build the docker container

## Run the Servers
### Run Straight-up!
```
python server_backend.py --port=8043 &
python server_frontend.py --port=8044 --backend_address=localhost --backend_port=8043
```
There are some default ports but the backend_address and backend_port are required.

### Run via the Entrypoint script

A bash script exists so that 1 docker container can host either the frontend or the backend.  To use that script from bash, do something like:
```
./docker-entrypoint.sh --type=back --port=8043
./docker-entrypoint.sh --type=front --port=8044 --backend_address=localhost --backend_port=8043
```

### Run via Docker (Interactive)

To run via Docker, make sure you've built first with *make*, looked at the notes below about setting up ports correclty, and then issue the following:

```
docker run -it -p 8043:8043 pysimserv --type=back --port=8043
docker run -it -p 8044:8044 pysimserv --type=front --port=8044 --backend_address=$(ifconfig en0 | awk '$1 == "inet" {print $2}') --backend_port=8043
```
NOTE: the -it flag for interactive mode & to forward TTY and get all the pretty colors

NOTE the backend_address.  This is the whole point of this project.  In order for containers to interconnect on the same host, they cannot use localhost.  They are isolated.  You have to use the host's IP address.  

... or better yet... service discovery!

### Run via Docker (daemonized)

To run via Docker where FRONT and BACK are daemons, just run the helpful script:
```
./run-containers.sh
```

This will create BACK then FRONT, remember the container IDs, start up a client, and then when you are done with the client, shutdown the containers & everything is clean

## Run the Client all by itself
```
python client.py
```

You will be prompted with a basic console to send commands.  Anything unknown you type will receive an echo.  Currently the three available messages are:
* Ping
* Pong (technically invalid but works)
* Person


# Testing
```
python setup.py test
```

The above will run through some assertions mainly surrounding the MessageParser class.  No integration tests

# Example

Python Simple Server has a few simple console coloring standards.  
- Yellow is a warning for Unknown messages (will be an echo)
- Red is for fatal errors
- Green is for accepted messages
- Blue is for understood messages but out of order (i.e. sending a Pong or receiving a Ping)

<img src="https://raw.githubusercontent.com/xeb/py-simple-server/master/screenshot.png" />


# Running with Docker Notes
Make sure you have your daemon running, VM-created if need be & ports forwarded.  Some helpful commands to remember:
```
docker-machine create --driver virtualbox default
docker-machine ls
eval $(docker-machine env)
VBoxManage controlvm "default" natpf1 "tcp-port8043,tcp,,8043,,8043"
VBoxManage controlvm "default" natpf1 "tcp-port8044,tcp,,8044,,8044"
```
