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
import numpy as np

# Avro schema definition (replace with your specific data types if needed)
schema_str = """
{
	"type": "record",
	"name": "BigMachine",
	"fields": [
		{"name": "time", "type": {"type" : "long", "logicalType": "time-micros" }},
		{"name": "x", "type": "long"},
		{"name": "y", "type": "long"},
		{"name": "z", "type": "long"}
	]
}
"""

# Kafka producer configuration with bootstrap servers
producer = Producer({
  'bootstrap.servers': 'localhost:9092',
})
topic = "chair1.bigmachine"

class Measurement:
  def __init__(self, x,y,z):
    self.time = np.datetime64(datetime.now()).view('<i8')
    self.x = x 
    self.y = y 
    self.z = z 


def measurement_to_dict(measurement, ctx):
  return dict(time=measurement.time, x=measurement.x, y=measurement.y, z = measurement.z)

schema_registry_conf = {'url': 'http://localhost:8085'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(schema_registry_client,
                                 schema_str, measurement_to_dict)
string_serializer = StringSerializer('utf_8')

# Sensor data generation function (replace with your sensor data logic)
def generate_sensor_data():
  x = random.random() * 10  # Replace with your sensor data generation for x
  y = random.random() * 10  # Replace with your sensor data generation for y
  z = random.random() * 10  # Replace with your sensor data generation for z
  return Measurement(x,y,z)


def call_n_times_per_second(fn,cb, n):
  while True:
    last_timestamp = time.perf_counter()
    for i in range(n):
      fn()
    
    cb()
    new_timestamp = time.perf_counter()
    time.sleep(max(1 - (new_timestamp - last_timestamp), 0))
  


def flush():
    producer.flush()

def do_the_thing():
  data = generate_sensor_data()
  try:
    producer.produce(topic=topic,
                   key=string_serializer(str(uuid4())),
                   value=avro_serializer(data, SerializationContext(topic, MessageField.VALUE)))

  except BufferError:
    producer.flush()

call_n_times_per_second(do_the_thing, flush, 10_000)
