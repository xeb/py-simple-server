# (Rancher) Compose Configurations

# Notes
- 1) Create the cluster
- 2) Start it
- 3) Show the UI
- 4) Connect the client
- 5) Talk about CONSUL & links
- 6) Scale something

This directory contains two configuration files.  

- 1) a Docker Compose of the service stack, ports, images, etc.
- 2) a simple Rancher Compose specifying the scale of each container

# Running from the CLI
- 1) Install the rancher-compose CLI (```brew install rancher-compose``` or ```apt-get install rancher-compose```)
- 2) Set the appropriate env variables in ```create.sh```
- 3) Run ```./create.sh```!

# Running from the Web UI
- 1) Head over to the Stacks section of Rancher
- 2) do "Add Stack"
- 3) paste the files in the appropriate places
- 4) give it a name
- 5) click Create!  (optionally set the checkbox to start services)

# References

http://docs.rancher.com/rancher/rancher-compose/
http://docs.rancher.com/rancher/rancher-compose/commands/
