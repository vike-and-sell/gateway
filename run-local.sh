#!/bin/sh

docker build --tag "flask-gateway" .
docker run --detach -p 8080:8080 flask-gateway
