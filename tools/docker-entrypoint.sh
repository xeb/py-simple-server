#!/bin/bash
while test $# -gt 0; do
        case "$1" in
                --port*) # port to host
                        export PORT=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --address*) # client address to connect to
                        export ADDRESS=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --type*) # types are: back,front,client
                        export TYPE=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --name*) # for logging of messages
                        export NAME=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --backends*) # list of backs to connect to
                        export BACKENDS=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --consul*) # consul cluster to query
                        export CONSUL=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --dnshosts*) # dns entry to resolve
                        export DNSHOSTS=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --dnsport*) # consul cluster to query
                        export DNSPORT=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --pattern*) # consul cluster to query
                        export PATTERN=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                *)
                        break
                        ;;
        esac
done
if [ "${TYPE}" == "front" ];
then
  if [ "${BACKENDS}" == "dynamic" ]; # dynamically get the backends
  then
  echo "Starting FRONT (dynamic) on port $PORT connecting to (DNS $DNSHOSTS : $DNSPORT or Consul $CONSUL ) ..."
    python ../src/server_frontend_dynamic.py --name=${NAME} --dns=${DNSHOSTS} --dns_port=${DNSPORT} --consul=${CONSUL} --port=${PORT} --pattern=${PATTERN}
    exit 0
  fi
  echo "Starting FRONT on port $PORT connecting to $BACKENDS ..."
  python ../src/server_frontend.py --name=${NAME} --port=${PORT} --backends=${BACKENDS}
fi
if [ "${TYPE}" == "back" ];
then
	echo "Starting BACK on port $PORT..."
  python ../src/server_backend.py --name=${NAME} --port=${PORT}
fi
if [ "${TYPE}" == "client" ];
then
	echo "Attempting Client connection to FRONT on port $ADDRESS : $PORT..."
  python ../src/client.py --address=${ADDRESS}
fi
if [ "${TYPE}" == "test" ];
then
	echo "Running a test within the container..."
  python ../src/server_backend.py --name=BACK --port=8043 &
  sleep 1
  python ../src/server_frontend.py --name=FRONT --port=8044 --backends=localhost:8043 &
  sleep 1
  python ../src/client.py --address=localhost:8044 --sendall
  kill -9 $(ps aux | grep "python" | awk '{print $2}')
fi
