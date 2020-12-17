kafka-jam
============
This jam I set up a dockerized Kafka cluster with 3 consumer apps reading events from a single Kafka topic 
(split into 3 partitions). I also made a simple python script for producing events to this partitioned topic. 
When producing events I randomized the message key in order to get a feel for how Kafka partitioning works. 
The consuming apps are all connected as one consumer group. This approach gives insight in to how Kafka delivers events
when the consumer is a distributed service.

## Usage

### Start a cluster:
Start the services (kafka broker, zookeeper and consumer apps) by running:
```docker-compose up --scale consumer-app=3 ```

### Start producer:

All set, consumers should now be ready to receive events. Start producing events by running: ```python producer.py ```
(in a python 3.8 env).

### Destroy the cluster:
In order to make sure volumes are deleted, use -v flag when destroying the cluster:
- ```docker-compose down -v  ```

### Manual creation of topics
Topics can be created manually as well:

exec into the kafka broker container:
```docker exec -it <kafka_container_id> /bin/bash ```

cd into kafka folder:
```cd opt/kafka ```

Create a new topic (replicated once, split over 3 partitions):
```bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic <topic_name> --create --replication-factor 1 --partitions 3```

To verify that topic is created and correctly partitioned:
```bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic <topic_name> --describe```


## Credits

The image is available directly from [Docker Hub](https://hub.docker.com/r/wurstmeister/kafka/).

All credits belong to: [http://wurstmeister.github.io/kafka-docker/](http://wurstmeister.github.io/kafka-docker/)
