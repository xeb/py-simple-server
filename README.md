<a href="https://travis-ci.org/xeb/py-simple-server">
<img src="https://api.travis-ci.org/xeb/py-simple-server.svg" />
</a>

Python Simple Server
================

A simple Python client/server that uses a basic **protobuf** protocol to communicate.  There is a sample of message definitions contained within the Messages.proto file

# Execution
## Build
```python setup.py build``` 

Will generate the Messages_pb2.py file from Messages.proto

## Run the Server
```python server.py```

You can optionally specify a port number if you desire, the default is *8044*

## Run the Client
```python client.py``` 

You will be prompted with a basic console to send commands.  Anything unknown you type will receive an echo.  Currently the three available messages are:
* Ping
* Pong (technically invalid but works)
* Person


# Testing
```python setup.py test```

The above will run through some assertions mainly surrounding the MessageParser class

# Example

Python Simple Server has a few simple console coloring standards.  
- Yellow is a warning for Unknown messages (will be an echo)
- Red is for fatal errors
- Green is for accepted messages
- Blue is for understood messages but out of order (i.e. sending a Pong or receiving a Ping)

<img src="https://raw.githubusercontent.com/xeb/py-simple-server/master/screenshot.png" />