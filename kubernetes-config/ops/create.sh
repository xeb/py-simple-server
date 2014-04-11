#!/bin/bash
kubectl config use-context pss
kubectl create ns pysimserv
kubectl create -f ..
