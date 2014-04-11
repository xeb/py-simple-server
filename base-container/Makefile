.PHONY: all

all: build

build:
	docker build -t xebxeb/pybase .

clean:
	docker rmi -f xebxeb/pybase

run:
	docker run -it xebxeb/pybase bash

echo:
	docker run xebxeb/pybase env | grep IS_SECURE

publish:
	docker push xebxeb/pybase
