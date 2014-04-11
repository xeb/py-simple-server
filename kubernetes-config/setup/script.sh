#!/bin/bash
sudo sh -c 'docker daemon -H unix:///var/run/docker-bootstrap.sock -p /var/run/docker-bootstrap.pid --iptables=false --ip-masq=false --bridge=none --graph=/var/lib/docker-bootstrap 2> /var/log/docker-bootstrap.log 1> /dev/null &'
sudo docker -H unix:///var/run/docker-bootstrap.sock run -d     --net=host     gcr.io/google_containers/etcd-amd64:2.2.1     /usr/local/bin/etcd         --listen-client-urls=http://127.0.0.1:4001,http://192.168.99.114:4001         --advertise-client-urls=http://192.168.99.114:4001         --data-dir=/var/etcd/data
sudo docker -H unix:///var/run/docker-bootstrap.sock run             --net=host             gcr.io/google_containers/etcd-amd64:2.2.1             etcdctl set /coreos.com/network/config '{ "Network": "10.1.0.0/16" }'
