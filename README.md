# ProKI-Kafka-TimescaleDb

The setup is based on docker-compose

To launch:
> docker compose up

The Kafka UI is available via port 8080. Grafana via port 3000.

The `producer.py` produces tuples matching the prototype schema (which has a timestamp and xyz coordinates).
It requires the following Python packages to be installed:
```
confluent_kafka
confluent_avro
avro
numpy
```

## Initial launch

Kafka topic is created by the docker-compose kafka-init service. `kafka-init/chair1.bigmachine.sh` creates a Kafka topic with a schema and creates a Kafka-connector, which moves data from Kafka into timescaleDB. The number of topic partitions and connector tasks can be configured based on the expected workload.

The timescale database is initialized when the timescale container is launched for the first time (or its volume is removed). The `postgres/chair1.bigmachine.sql` creates the Table Schema for the prototype machine.

# Known Problems

## Timezones

At some point, the timestamp value created by `producer.py` is assigned to a timezone that is different from the actual timezone. 
Instead of fixing the root of the problem, the grafana queries shift all timestamps by 2 hours.

## Initial Grafana load

Grafana does not display the example panels out of the box. You need to click the `edit` button in each panel and manually run the query for Grafana to show data on the dashboard.
