# PySimServ Registrator

This is a container to be used in Rancher that essentially just gets the IP address
for a given interface and then passes that to GliderLab's Registrator container.

# Usage
```
make build # which is: docker build -t xebxeb/pysimserv-registrator .
docker run xebxeb/pysimserv-registrator --interface=en0
```

# Rancher Usage
See the compose-config file in the <a href="../compose-config/">compose-config</a> directory.
