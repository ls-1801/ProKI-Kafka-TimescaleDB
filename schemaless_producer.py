from datetime import datetime

import time
import json
import random
from confluent_kafka import Producer

# Kafka producer configuration
producer = Producer({'bootstrap.servers': '130.149.139.21'})
topic = "IAT.machine1"

# Sensor data generation function (replace with your sensor data logic)
def generate_sensor_data():
  timestamp = datetime.utcnow().isoformat()
  x = random.random() * 10  # Replace with your sensor data generation for x
  y = random.random() * 10  # Replace with your sensor data generation for y
  z = random.random() * 10  # Replace with your sensor data generation for z
  return {"timestamp": timestamp, "x": x, "y": y, "z": z}

while True:
  # Generate sensor data
  data = generate_sensor_data()

  # Encode data as JSON string
  data_json = json.dumps(data)

  # Send data to Kafka topic
  producer.produce(topic, data_json.encode('utf-8'))
  producer.flush()

  # Simulate sensor data generation interval
  time.sleep(1)  # Adjust this based on your sensor data generation frequency

producer.flush()
