import json
import os
import time

from kafka import KafkaConsumer

def read_queue():
    consumer = KafkaConsumer(
        "product-topic",
        bootstrap_servers="localhost:29092",
        auto_offset_reset="earliest",
        # group_id='fastapi-group',
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    while True:
        for message in consumer:
            data = message.value
            print(json.dumps(data, indent=4, ensure_ascii=False))
        time.sleep(1)

if __name__ == "__main__":
    print(f"Start Consumer #{os.getpid()}")
    read_queue()
