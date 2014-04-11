#!/bin/bash

echo "Starting BACKs"
python ../src/server_backend.py --name=BACK1 --port=10040 > /dev/null 2>1 &
python ../src/server_backend.py --name=BACK2 --port=10041 > /dev/null 2>1 &
sleep 1

echo "Starting FRONT"
python ../src/server_frontend.py --name=FRONT --port=10050 --backends=localhost:10040,localhost:10041 > /dev/null 2>1 &
sleep 1

echo "Connecting Client"
python ../src/client.py --address=localhost:10050
