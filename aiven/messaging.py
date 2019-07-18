import sys
from kafka import KafkaConsumer, KafkaProducer
import logging


logger = logging.getLogger(__name__)

TOPIC_NAME="test_topic"

def get_kafka_consumer(bootstrap_servers: str,
                       ssl_cafile: str,
                       ssl_certfile: str,
                       ssl_keyfile: str,
                       topic_name: str = TOPIC_NAME) -> KafkaConsumer:
    ' Helper function to retrieve a Kafka Consumer'
    consumer = KafkaConsumer(
        topic_name=topic_name,
        auto_offset_reset="earliest",
        bootstrap_servers=bootstrap_servers,
        client_id="demo-client-1",
        group_id="demo-group",
        security_protocol="SSL",
        ssl_cafile=ssl_cafile,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile,
    )

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
                                  ssl_keyfile=ssl_keyfile)
    except Exception as ex:
        logger.error('Exception occured while connecting to Kafka.')
        logger.error(str(ex))
        sys.exit(1)
    else:
        return producer


# TODO: Replace annotation 'function' with real type
def consume_msg(consumer: KafkaConsumer, handle_msg: 'function') -> None:
    ' Function to consumer message from the given consumer and process it using the handle_msg callback '

    # We use the iterator from the consumer to retrieve the messages
    # By default it will block forever until a message is available
    # Commit is auto by default and offset will be updated periodically to avoid consuming the same message
    for msg in consumer:
        logger.info("Received Kafka message: {}".format(msg.value))
        handle_msg(msg.value)


def publish_message(producer: KafkaProducer, topic_name: str, message: str) -> None:
    ' Will publish a string message on a topic given a producer '
    try:
        producer.send(topic_name, message.encoding('UTF-8'))
        producer.flush()
        logger.info('Message published successfully.')
    except Exception as ex:
        logger.error('Error while publishing meesage to Kafka.')
        logger.error(str(ex))
        sys.exit(1)
