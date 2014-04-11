.PHONY: all

all: build container run

clean:
	rm -rf src/*.pyc
	rm -f src/Messages_pb2.py
	docker rmi -f xebxeb/pysimserv

run:
	docker run xebxeb/pysimserv --type=test

build:
	protoc --python_out=src Messages.proto

container:
	docker build -t xebxeb/pysimserv .

publish:
	docker push xebxeb/pysimserv

kill:
	./tools/stop_all_py.sh

test:
	python src/server_backend.py --name=BACK-one --port=6041 &
	sleep 1
	python src/server_backend.py --name=BACK-two --port=6042 &
	sleep 1
	python src/server_frontend.py --name=ROUTER-backs --backends=localhost:6041,localhost:6042 --port=6043 &
	sleep 1
	python src/server_frontend.py --name=ROUTER-router-b2 --backends=localhost:6043,localhost:6042 --port=6044 &
	sleep 1
	# The FRONT connects to: both ROUTERs (which are just FRONTs) and both BACKs
	python src/server_frontend.py --name=FRONT-all --backends=localhost:6044,localhost:6043,localhost:6042,localhost:6041 --port=6045 &
	sleep 1
	python src/client.py --address=localhost:6045
	# python client.py --address=localhost:6045 --sendall
	./tools/stop_all_py.sh
