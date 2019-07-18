import sys
from typing import Callable

from kafka import KafkaConsumer, KafkaProducer
import logging


logger = logging.getLogger(__name__)

TOPIC_NAME="test_topic"

def get_kafka_consumer(bootstrap_servers: str,
                       ssl_cafile: str,
                       ssl_certfile: str,
                       ssl_keyfile: str,
                       topic_name: str) -> KafkaConsumer:
    ' Helper function to retrieve a Kafka Consumer'
    try:
        consumer = KafkaConsumer(
            topic_name,
            auto_offset_reset="earliest",
            bootstrap_servers=bootstrap_servers,
            client_id="demo-client-1",
            group_id="demo-group",
            security_protocol="SSL",
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        )
    except Exception as ex:
        logger.error('Not able to create Kafka consumer')
        logger.error(str(ex))
        sys.exit(1)
    else:
        return consumer


def get_kafka_producer(bootstrap_servers: str,
                       ssl_cafile: str,
                       ssl_certfile: str,
                       ssl_keyfile: str) -> KafkaProducer:
    ' Helper function to create the kafka producer and handle exceptions '
    producer = None
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                  security_protocol='SSL',
                                  ssl_cafile=ssl_cafile,
                                  ssl_certfile=ssl_certfile,
                                  ssl_keyfile=ssl_keyfile,
                                  # We want to fail fast
                                  max_block_ms = 1000)
    except Exception as ex:
        logger.error('Exception occured while connecting to Kafka.')
        logger.error(str(ex))
        sys.exit(1)
    else:
        return producer


def consume_msg(consumer: KafkaConsumer, handle_msg: Callable) -> None:
    ' Function to consumer message from the given consumer and process it using the handle_msg callback '

    # We use the iterator from the consumer to retrieve the messages
    # By default it will block forever until a message is available
    # Commit is auto by default and offset will be updated periodically to avoid consuming the same message
    for msg in consumer:
        logger.info("Received Kafka message: {}".format(msg.value))
        handle_msg(msg.value.decode("utf-8"))


def publish_message(producer: KafkaProducer, topic_name: str, message: str) -> None:
    ' Will publish a string message on a topic given a producer '
    print(type(message))
    print(message)
    try:
        future = producer.send(topic_name, str.encode(message))
        producer.flush()

        # Block for 'synchronous' sends
        record_metadata = future.get(timeout=10)
        logger.info(f'Message published successfully.')
        logger.info(f'Topic name: {record_metadata.topic}')
        logger.info(f'Partition: {record_metadata.partition}')
        logger.info(f'Current offset: {record_metadata.offset}')
    except Exception as ex:
        logger.error('Error while publishing meesage to Kafka.')
        logger.error(str(ex))
        sys.exit(1)