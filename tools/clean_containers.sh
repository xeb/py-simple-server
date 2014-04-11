#!/bin/bash

for MACHINE in $(docker-machine ls | grep -v NAME | awk '{print $1}'); do
  echo "Purging exited containers from $MACHINE"
  eval $(docker-machine env $MACHINE)
  export CONTAINERS=$(docker ps -a | grep Exited | awk '{print $1}')
  if [ -n "$CONTAINERS" ]; then
    docker rm -f $CONTAINERS
  fi
done
