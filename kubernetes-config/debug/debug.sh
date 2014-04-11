#!/bin/bash
kubectl create -f busybox.yaml
sleep 1
kubectl exec -it busybox /bin/sh 
