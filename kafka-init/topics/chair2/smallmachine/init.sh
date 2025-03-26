
kafka-topics.sh --create --topic chair2.smallmachine --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181
curl -d@jsonschema.json 'http://kafka-ui:8080/api/clusters/local/schemas' -X POST -H 'Content-Type: application/json'
curl -d@jdbc-connector.json 'http://kafka-ui:8080/api/clusters/local/connects/first/connectors' -X POST -H 'Content-Type: application/json'
