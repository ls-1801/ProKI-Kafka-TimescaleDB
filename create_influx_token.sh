#!/bin/bash
INFLUX_HOST="http://influxdb:8086"
INFLUX_TOKEN=$1 #operator-token
INFLUX_ORG_NAME=$2 #proki
BUCKET_NAME=$3 #chair1.bigmachine

# running the following command will create the bucket and the write token
# docker run -it -v $(pwd):/scripts --net=proki_default influxdb:latest /scripts/create_influx_token.sh \
# OPERATOR_TOKEN ORG_NAME BUCKET_NAME

ORG_ID=$(influx org find --host ${INFLUX_HOST} --token ${INFLUX_TOKEN} | grep ${INFLUX_ORG_NAME} | cut -f1)

BUCKET_ID=$(influx bucket create --org-id ${ORG_ID} --host ${INFLUX_HOST} --token ${INFLUX_TOKEN} --name ${BUCKET_NAME} | grep ${BUCKET_NAME} | cut -f1)

influx auth create --org-id ${ORG_ID} --host ${INFLUX_HOST} --token ${INFLUX_TOKEN} \
  --write-bucket ${BUCKET_ID} --json

