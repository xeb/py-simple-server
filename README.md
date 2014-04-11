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

You will be prompted with 


# Testing
```python setup.py test```

The above will run through some assertions mainly surrounding the MessageParser class
