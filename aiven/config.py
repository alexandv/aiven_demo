import configparser
from configparser import ConfigParser
import os
import logging

CONFIG_FILE='config.ini'

logger = logging.getLogger(__name__)


def _check_config(config, config_value):
    ' Helper function to check if config value is present in a dictionary '
    if config_value not in config:
        logger.error(f'{config_value} cannot be found in config file')
        raise Exception('{config_value} cannot be found in config')


def get_config(config_file: str = CONFIG_FILE) -> ConfigParser:
    '''
    Read config value file and make sure that it is valid

    :param config_file: The path to the file containing the config values
    :return: The dictionary like structure with the configuration options
    '''

    # Check if config file exists on disk
    if not(os.path.exists(config_file)):
        raise FileNotFoundError(f'The config file {config_file} was not found. You can also provide a different file with --config.')

    config = configparser.ConfigParser()
    config.read(config_file)

    # Check that each required configuration item exists
    # If one of them is missing exit
    _check_config(config, 'kafka')
    _check_config(config['kafka'], 'bootstrap_servers')
    _check_config(config['kafka'], 'ssl_cafile')
    _check_config(config['kafka'], 'ssl_certfile')
    _check_config(config['kafka'], 'ssl_keyfile')
    _check_config(config, 'postgres')
    _check_config(config['postgres'], 'host')
    _check_config(config['postgres'], 'port')
    _check_config(config['postgres'], 'dbname')
    _check_config(config['postgres'], 'user')
    _check_config(config['postgres'], 'password')
    _check_config(config['postgres'], 'sslcert')

    return config