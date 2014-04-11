#!/bin/bash

for MACHINE in $(docker-machine ls | grep -v NAME | awk '{print $1}'); do
  echo "Restarting $MACHINE"
  docker-machine stop $MACHINE
  # docker-machine start $MACHINE
done
