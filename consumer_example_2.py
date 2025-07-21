import json
import os
import time

from kafka import KafkaConsumer
def des(value):
    try:
        result = json.loads(value.decode("utf-8"))
    except:
        result = str(value)
    return value

def read_queue():
    consumer = KafkaConsumer(
        "product-topic-test",
        bootstrap_servers="localhost:29092",
        auto_offset_reset="earliest",
        # group_id='fastapi-group',
        value_deserializer=des
    )

    while True:
        for message in consumer:
            data = message.value
            try:
                print(json.dumps(data, indent=4, ensure_ascii=False))
            except:
                print(data)
        time.sleep(1)

if __name__ == "__main__":
    print(f"Start Consumer #{os.getpid()}")
    read_queue()
