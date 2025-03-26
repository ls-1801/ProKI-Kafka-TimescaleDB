#!/usr/bin/env python
from datetime import datetime
import random
from confluent_kafka import Producer, avro
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import time
from uuid import uuid4
import argparse
from datetime import datetime
import random
from uuid import uuid4
import time
import numpy as np
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


def main():
    parser = argparse.ArgumentParser(description='Produce sensor data to Kafka.')
    parser.add_argument('--chair', type=str, required=True, help='Chair ID (e.g., chair1, chair2).')
    parser.add_argument('--machine', type=str, required=True, help='Machine type (e.g., bigmachine, smallmachine).')
    parser.add_argument('--num_messages', type=int, default=100, help='Number of messages to produce.')
    args = parser.parse_args()

    chair = args.chair
    machine = args.machine
    num_messages = args.num_messages

    topic = f"{chair}.{machine}"

    # Avro schema definitions
    big_machine_schema_str = """
    {
        "type": "record",
        "name": "BigMachine",
        "fields": [
            {"name": "time", "type": {"type": "long", "logicalType": "time-micros"}},
            {"name": "x", "type": "long"},
            {"name": "y", "type": "long"},
            {"name": "z", "type": "long"}
        ]
    }
    """

    small_machine_schema_str = """
    {
        "type": "record",
        "name": "SmallMachine",
        "fields": [
            {"name": "time", "type": {"type": "long", "logicalType": "time-micros"}},
            {"name": "x", "type": "long"},
            {"name": "y", "type": "long"}
        ]
    }
    """

    # Select schema based on machine type
    if machine == "bigmachine":
        schema_str = big_machine_schema_str
        class Measurement:
            def __init__(self, x, y, z):
                self.time = np.datetime64(datetime.now()).view('<i8')
                self.x = x
                self.y = y
                self.z = z

        def measurement_to_dict(measurement, ctx):
            return dict(time=measurement.time, x=measurement.x, y=measurement.y, z=measurement.z)

        def generate_sensor_data():
            x = random.random() * 10
            y = random.random() * 10
            z = random.random() * 10
            return Measurement(x, y, z)


    elif machine == "smallmachine":
        schema_str = small_machine_schema_str
        class Measurement:
            def __init__(self, x, y):
                self.time = np.datetime64(datetime.now()).view('<i8')
                self.x = x
                self.y = y

        def measurement_to_dict(measurement, ctx):
            return dict(time=measurement.time, x=measurement.x, y=measurement.y)

        def generate_sensor_data():
            x = random.random() * 10
            y = random.random() * 10
            return Measurement(x, y)
    else:
        print("Invalid machine type. Choose 'bigmachine' or 'smallmachine'.")
        return

    # Kafka producer configuration
    producer_config = {
        'bootstrap.servers': 'localhost:9092',
    }
    producer = Producer(producer_config)

    schema_registry_conf = {'url': 'http://localhost:8085'}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    avro_serializer = AvroSerializer(schema_registry_client, schema_str, measurement_to_dict)
    string_serializer = StringSerializer('utf_8')

    def delivery_report(err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    # Produce messages
    for _ in range(num_messages):
        data = generate_sensor_data()
        try:
            producer.produce(
                topic=topic,
                key=string_serializer(str(uuid4())),
                value=avro_serializer(data, SerializationContext(topic, MessageField.VALUE)),
                callback=delivery_report
            )
        except BufferError:
            producer.flush()

        producer.poll(0)  # Trigger delivery reports
        time.sleep(0.01)

    producer.flush()  # Wait for all messages to be delivered


if __name__ == "__main__":
    main()
