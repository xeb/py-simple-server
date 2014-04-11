#!/bin/bash
# export RANCHER_URL=http://localhost:8080/
# export RANCHER_ACCESS_KEY={access}
# export RANCHER_SECRET_KEY={secret}
rancher-compose -p pysimserv create
rancher-compose -p pysimserv start # or 'down'?
