#!/bin/bash
export MASTER_NAME="kube-master"
docker-machine create -d virtualbox $MASTER_NAME
docker-machine create -d virtualbox kube-node1
docker-machine create -d virtualbox kube-node2

echo "Clearing all Docker processes from $MASTER_NAME"
docker-machine ssh $MASTER_NAME docker rm -f $(docker-machine ssh $MASTER_NAME docker ps --all | grep -v CONTAINER | awk '{print $1}')

export MASTER_IP=`docker-machine ip $MASTER_NAME`
# export NODE_1_IP=`docker-machine ip kube-node1`
# export NODE_2_IP=`docker-machine ip kube-node2`


export K8S_VERSION=1.2.1
export ETCD_VERSION=2.2.1
export FLANNEL_VERSION=0.5.5
# export FLANNEL_IFACE=eth0
# export FLANNEL_IPMASQ=<flannel_ipmasq_flag (defaults to true)>

echo "Creating startup script..."
cat << EOF > script.sh
#!/bin/bash
sudo sh -c 'docker daemon -H unix:///var/run/docker-bootstrap.sock -p /var/run/docker-bootstrap.pid --iptables=false --ip-masq=false --bridge=none --graph=/var/lib/docker-bootstrap 2> /var/log/docker-bootstrap.log 1> /dev/null &'
sudo docker -H unix:///var/run/docker-bootstrap.sock run -d \
    --net=host \
    gcr.io/google_containers/etcd-amd64:${ETCD_VERSION} \
    /usr/local/bin/etcd \
        --listen-client-urls=http://127.0.0.1:4001,http://${MASTER_IP}:4001 \
        --advertise-client-urls=http://${MASTER_IP}:4001 \
        --data-dir=/var/etcd/data
sudo docker -H unix:///var/run/docker-bootstrap.sock run \
            --net=host \
            gcr.io/google_containers/etcd-amd64:${ETCD_VERSION} \
            etcdctl set /coreos.com/network/config '{ "Network": "10.1.0.0/16" }'
EOF
echo "Done!"

echo "Copying script to $MASTER_NAME"
docker-machine scp script.sh $MASTER_NAME:~/setup.sh
