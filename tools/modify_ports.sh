#!/bin/bash
for MACHINE in $(docker-machine ls | grep -v NAME | awk '{print $1}'); do
  echo "Opening ports on $MACHINE"

  for i in {8000..9000}; do
    VBoxManage modifyvm "$MACHINE" --natpf1 "tcp-port$i,tcp,,$i,,$i"
    VBoxManage modifyvm "$MACHINE" --natpf1 "udp-port$i,udp,,$i,,$i"
  done
done
