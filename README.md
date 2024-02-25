# ProKI-Kafka-Influxdb

Setup is based on docker-compose

to launch:
> docker compose up


## Initial launch

Kafka topic is created by the docker-compose kafka-init service.

Influxdb needs to be setup, either manually using the web interface at localhost:8086 or using the setup influxdb scripts

> docker run -e USERNAME=USERNAME -e PASSWORD=PASSWORD -v $(pwd):/scripts --net=proki_default influxdb:latest /scripts/influx_setup.sh | jq .token

Make sure to copy the token. The org will be called proki.

Vector expects the example bucket to exist. to create the example bucket you can either use the web interface or use the script. You need to provide the operator-token and the org name and choose a bucket name.

> docker run -it -v $(pwd):/scripts --net=proki_default influxdb:latest /scripts/create_influx_token.sh \
>   OPERATOR_TOKEN ORG_NAME BUCKET_NAME

Make sure to copy the bucket-write token and the organisation id.
> "write:orgs/ORG_ID/buckets/BUCKET_ID"

Lastly you need to update the vector.toml with the bucket-write token (not the operator-token) and the organisation id.







