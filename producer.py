from confluent_kafka import Producer
import random
import time
import json

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to produce messages to
kafka_topic = 'chair1.bigmachine'

# Create Kafka Producer instance configuration
producer_conf = {
    'bootstrap.servers': bootstrap_servers
}

# Create Kafka Producer
producer = Producer(producer_conf)


# Function to generate random message
def generate_random_message():
    number_of_samples = int(random.uniform(180, 320))
    base_time = time.time()
    start_perf = time.perf_counter()
    tuples = []
    for i in range(number_of_samples):
        tuples.append({'timestamp': base_time + (time.perf_counter() - start_perf),
                       'x': (1664525 * (i * 3 + 1) + 1013904223) % 100, 'y': (1664525 * (i * 3 + 2) + 1013904223) % 100,
                       'z': (1664525 * (i * 3 + 3) + 1013904223) % 100, "event": "data"})

    return json.dumps(tuples)


# Function to delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def stop_experiment():
    message = json.dumps({'timestamp': time.time(), 'event': 'stop'})
    producer.produce(kafka_topic, message.encode('utf-8'), callback=delivery_report)


def start_experiment():
    message = json.dumps({'timestamp': time.time(), 'event': 'start'})
    producer.produce(kafka_topic, message.encode('utf-8'), callback=delivery_report)


# Produce random messages
try:
    while True:
        # Generate random message
        start_experiment()
        number_of_measurements = random.randint(10000, 20000)

        for _ in range(number_of_measurements):
            message = generate_random_message()
            # Produce message to Kafka topic
            producer.produce(kafka_topic, message.encode('utf-8'), callback=delivery_report)
            time.sleep(random.uniform(0.001, 0.01))

        stop_experiment()
        # Flush messages to ensure delivery
        producer.flush()

        # Sleep for a random interval
        time.sleep(random.uniform(2, 4))
except KeyboardInterrupt:
    # Clean up resources on keyboard interrupt
    producer.flush()
    producer.close()
