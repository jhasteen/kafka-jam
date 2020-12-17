from time import sleep
from json import dumps
from kafka import KafkaProducer
from random import randint
import platform
import asyncio
import os

platform_name = platform.system().lower()

if platform_name == 'linux':
    BROKER_URL = 'kafka:29092'
elif platform_name == 'darwin':
    BROKER_URL = 'localhost:9092'

TOPIC_NAME = 'ExampleTopic'


async def produce(topic):
    producer = KafkaProducer(
        bootstrap_servers=[BROKER_URL],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    iteration = 0

    for _ in range(20):
        res = producer.send(topic, value={'counter': iteration}, key=bytes(str(randint(1, 5)), 'utf-8'))
        metadata = res.get(timeout=10)
        print(f"topic: {metadata.topic}, partition: {metadata.partition}, offset: {metadata.offset}")
        iteration += 1

        print("Iteration", _)

        await asyncio.sleep(1)


async def start_producer():
    produce_task = asyncio.create_task(produce(TOPIC_NAME))
    await produce_task


def main():
    print(f"BROKER URL: {BROKER_URL}")
    print(f"TOPIC_NAME: {TOPIC_NAME}")

    try:
        asyncio.run(start_producer())
    except KeyboardInterrupt as e:
        print("Shutting down\n")
    finally:
        print("Handling exception...\n")


if __name__ == '__main__':
    main()
