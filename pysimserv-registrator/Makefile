.PHONY: all

all: build

build:
	docker build -t xebxeb/pysimserv-registrator .

clean:
	docker rmi -f xebxeb/pysimserv-registrator

run:
	docker run -it xebxeb/pysimserv-registrator --interface=eth0 consul://192.168.99.105:8500

shell:
	docker run -it --entrypoint=/bin/sh xebxeb/pysimserv-registrator -s

show:
	docker run --entrypoint=/bin/env xebxeb/pysimserv-registrator | grep HOSTIP

publish:
	docker push xebxeb/pysimserv-registrator
