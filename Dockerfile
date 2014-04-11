FROM python:2.7.11-slim

WORKDIR /
RUN pip install protobuf==3.0.0b2 colorama dnspython
COPY src/*.py /src/
COPY tools/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]
