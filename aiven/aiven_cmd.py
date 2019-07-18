# Code to handle command line

from aiven.log import setupLogging
from aiven.config import get_config
from aiven.messaging import get_kafka_consumer, get_kafka_producer, publish_message, consume_msg
from aiven.db import get_insert_event_to_db
import argparse
import logging


def parse_arguments():
    ' This will parse the arguments and return the args objects '
    parser = argparse.ArgumentParser(description="Aiven command line tool")
    parser.add_argument('--config', help='The config file for kafka and postgres connections. Default: config.ini')
    parser.add_argument('--topic', help='Specify the topic to use to listen and send to. Default: aiven_event')

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', dest='command')
    subparsers.required = True
    parser_post = subparsers.add_parser('post', help='Post message to the Kafka topic')
    parser_post.add_argument('message', help='The message to send')

    subparsers.add_parser('sub', help='Subscribe to the topic')

    return parser.parse_args()


if __name__ == '__main__':
    # Read logging setup from json file or use default conf
    setupLogging()
    # Setup a logger with the name of the current module
    logger = logging.getLogger(__name__)

    args = parse_arguments()

    if args.config is not None:
        config = get_config(args.config)
    else:
        config = get_config('config.ini')

    if args.topic is not None:
        topic = args.topic
    else:
        topic = 'aiven_event'

    if args.command == 'post':
        logger.info('Posting message to kafka server')
        kafka_producer = get_kafka_producer(config['kafka']['bootstrap_servers'],
                           config['kafka']['ssl_cafile'],
                           config['kafka']['ssl_certfile'],
                           config['kafka']['ssl_keyfile'])
        publish_message(kafka_producer, topic, args.message)
        kafka_producer.close()
    else:
        logger.info('Starting consumer. Press Ctl-C to stop this consumer.')
        kafka_consumer = get_kafka_consumer(config['kafka']['bootstrap_servers'],
                           config['kafka']['ssl_cafile'],
                           config['kafka']['ssl_certfile'],
                           config['kafka']['ssl_keyfile'],
                           topic)
        insert_event_to_db = get_insert_event_to_db(config['postgres']['host'],
                           config['postgres']['port'],
                           config['postgres']['dbname'],
                           config['postgres']['user'],
                           config['postgres']['password'],
                           config['postgres']['sslcert'])
        try:
            consume_msg(kafka_consumer, insert_event_to_db)
        except KeyboardInterrupt:
            logger.info('Detected Ctl-C. Leaving')
            # TODO: Add proper cleanup