#!/bin/bash
echo "Building again just in case..."
make
echo "Starting BACK detached..."
export BACK_CONTAINER_ID=`docker run -d -p 8043:8043 pysimserv --type=back --port=8043`

echo "Starting FRONT detached..."
export FRONT_CONTAINER_ID=`docker run -d -p 8044:8044 pysimserv --type=front --port=8044 --backend_address=$(ifconfig en0 | awk '$1 == "inet" {print $2}') --backend_port=8043`

echo "Starting up a client for you..."
python client.py --port=8044

echo "Shutting down the containers..."
docker stop $BACK_CONTAINER_ID
docker stop $FRONT_CONTAINER_ID
