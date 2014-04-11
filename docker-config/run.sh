#!/bin/bash

# get the current host's IP
export IP=$(docker-machine ip `docker-machine active`)

# connect backends
docker run -d --name=back1 -p=8040:8040 xebxeb/pysimserv:latest --type=back --name=BACK1 --port=8040
docker run -d --name=back2 -p=8041:8041 xebxeb/pysimserv:latest --type=back --name=BACK2 --port=8041

#connect the front
sleep 1
docker run -d --name=front1 -p=8050:8050 xebxeb/pysimserv:latest --type=front --name=FRONT \
  --backends=$IP:8040,$IP:8041 --port=8050

# wait then connect
sleep 1
python ../src/client.py --address=$IP:8050

# shut it down!
# ./stop.sh
