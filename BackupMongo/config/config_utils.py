import os
import sys
from typing import Optional

from config import response_codes
from db_utils import mongo_db_uri


def print_usage(exit_app: bool):
    """
    Print the usage message and optionally, exit the app.

    :param exit_app: bool. If True, the app will exit after printing the message. If False, it will
           print the message and return
    """
    app_name = os.path.split(os.path.abspath(__file__))[1]

    print(f"""
Remember you can pass a configuration file to skip
typing the parameters every time this way:
./{app_name} <configuration file>

where,
  configuration file: A json file that provides the input parameters.\n""")

    if exit_app:
        exit(-1)


def load_config_file() -> Optional[dict]:
    """
    Load a configuration file specified on the app parameters, if provided.

    :return: dict|None
             Return either the loaded configuration if the parameter was supplied and the configuration was loaded,
             or False if no parameters supplied.

    Note: If there was an error attempting to load the configuration, the function prints an error and exits.
    """

    config = None

    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print_usage(exit_app=True)

        # load configuration json
        import json

        try:
            with open(sys.argv[1], 'rt') as f:
                config = json.loads(f.read())

            t = type(config)
            if t != dict:
                raise Exception(f'Invalid configuration, it should be a dictionary, not a "{t}"')

        except Exception as e:
            print(f'Error loading the configuration file: {e}')
            exit(-1)

    else:
        print_usage(exit_app=False)

    return config


def capture_input_parameters(list_data: dict):
    """
    Capture the source and destination databases for any db operation you want to do after.
    This function first tries to get the parameters from the json file passed as the command-line parameter
    to this tool, if none is specified, it asks the user the parameters via console input.

    If the parameters were capture from a file (without user intervention), a confirmation message will be displayed
    before returning the function. If the user answers 'N' the operation will be cancelled.
    """
    config = load_config_file()

    src_username = list_data['source']['username']
    src_password = list_data['source']['password']
    src_auth_source = list_data['source']['auth']
    src_host = list_data['source']['host']
    src_port = list_data['source']['port']
    src_dbname = list_data['source']['dbname']

    source_part = {
        'username': src_username,
        'password': src_password,
        'host': src_host,
        'port': src_port,
        'dbname': src_dbname,
    }

    source_mongo_uri = mongo_db_uri(src_username, src_password,
                                    src_host, src_port, src_dbname, src_auth_source)

    dest_username = list_data['destination']['username']
    dest_password = list_data['destination']['password']
    dest_auth_source = list_data['destination']['auth']
    dest_host = list_data['destination']['host']
    dest_port = list_data['destination']['port']
    dest_dbname = list_data['destination']['dbname']

    config = {
        'source': source_part,

        'destination': {
            'username': dest_username,
            'password': dest_password,
            'host': dest_host,
            'port': dest_port,
            'dbname': dest_dbname,
        }
    }

    backup_name = list_data['backup_name']
    try:
        destination_mongo_uri = mongo_db_uri(dest_username, dest_password,
                                             dest_host, dest_port, dest_dbname, dest_auth_source)
        return_code = response_codes.SUCCESS
    except Exception as ex:
        return_code = response_codes.NOT_CONNECT
        destination_mongo_uri = None

    return return_code, config, source_mongo_uri, destination_mongo_uri, backup_name, list_data

