#!/bin/bash

# running the docker command will output the operator token required for the other scritps
# docker run -e USERNAME=USERNAME -e PASSWORD=PASSWORD -v $(pwd):/scripts --net=proki_default influxdb:latest bash

influx setup --host http://influxdb:8086 --username $USERNAME --password $PASSWORD --org proki --bucket proki --force > /dev/null

influx auth create \
  --org proki\
  --operator \
  --json
