# Local Config

This folder contains scripts to running a PySimServ stack on a single host.  No docker, or anything fancy.

# Usage
```
./run.sh
```

This will create 2 backends (back1 & back2), and then 1 frontend (front1).  
It will statically link them togethers.

In order to shut everything down, you can run:
```
./stop.sh
```
*WARNING* this will purge all containers on the host that contain "xebxeb"
