#!/bin/bash

echo "...ok, just delete everything..."
docker rm -f $(docker ps --all | grep -v CONTAINER | awk '{print $1}')
