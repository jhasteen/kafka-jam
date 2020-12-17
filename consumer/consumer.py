import asyncio
import platform
import os
from json import loads
from time import sleep
from kafka import KafkaConsumer


TOPIC_NAME = 'ExampleTopic'

platform_name = platform.system().lower()

if platform_name == 'linux':
    BROKER_URL = 'kafka:29092'
elif platform_name == 'darwin':
    BROKER_URL = 'localhost:9092'


async def consume(topic):
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[BROKER_URL],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        client_id='test_client',
        group_id='my-consumer-group',
        key_deserializer=lambda x: str(x.decode('utf-8')),
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for event in consumer:
        event_data = event.value
        event_key = event.key
        partition = event.partition
        offset = event.offset
        print(f"here is value: {event_data}, key: {event_key}, partition: {partition} and offset: {offset}")
        await asyncio.sleep(1)


async def start_consumer():
    while True:
        try:
            consume_task = asyncio.create_task(consume(TOPIC_NAME))
            await consume_task
            return consume_task
        except:
            sleep(5)
            pass

def main():

    print(f"TOPIC_NAME: {TOPIC_NAME}")
    print(f"BROKER_URL: {BROKER_URL}")

    try:
        asyncio.run(start_consumer())
    except KeyboardInterrupt as e:
        print("Shutting down\n")
    finally:
        print("Handling exception...\n")


if __name__ == "__main__":
    main()
