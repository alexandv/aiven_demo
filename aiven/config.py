import configparser

CONFIG_FILE='example.ini'

def get_config():
    ' Initialize config values '
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if
        raise Exception(f'kafka section cannot be found in file {CONFIG_FILE}')

    if 'kafka' not in config:
        raise Exception(f'kafka section cannot be found in file {CONFIG_FILE}')

    if 'postgres' not in config:
        raise Exception(f'postgres section cannot be found in file {CONFIG_FILE}')
