#!/usr/bin/python
import os
import os.path
from typing import Optional

import bson
from pymongo import MongoClient
from pymongo import errors as pymongo_errors

from config import response_codes
from .backup_utils import create_folder_backup, backup_folder_for
from config.config_utils import capture_input_parameters
from console_utils import print_on_same_line


def run_backup(mongo_uri: str, dbname: str, backup_name: str) -> Optional[str]:
    """
    Connect to the server specified by mongo_uri and back up all the collection in the specified database.
    The backup is a serie of binary json files inside the backup directory (See "create_folder_backup" for more info).

    :param mongo_uri: str. The mongo uri to connect to the source server
    :param dbname: str. The database name to back up
    :return: Optional[str]. The backup name or None if there was an error.
      On failure, the error will be logged on the console
    """
    client = MongoClient(mongo_uri)
    db = client[dbname]
    collections = db.list_collection_names()
    backup_dir, backup_name = create_folder_backup(dbname, backup_name)

    max_len = 0
    n = 1
    count = len(collections)

    for collection_name in collections:
        max_len = print_on_same_line(f'[{n}/{count}] Backup {collection_name} ...', max_len)

        try:
            with open(os.path.join(backup_dir, f'{collection_name}.bson'), 'wb+') as f:
                for doc in db[collection_name].find():
                    f.write(bson.BSON.encode(doc))

        except Exception as e:
            print(f'\nAn error occurred creating the backup: {e}')
            return None

        n += 1

    print('\n')
    return backup_name


def restore_db(mongo_uri: str, dbname: str, directory: str) -> bool:
    """
    Connect to the server specified by mongo_uri and restore all the collection in the backup directory to
    the specified database.
    The backup is a serie of binary json files inside the backup directory (See "create_folder_backup" for more info).

    :param mongo_uri: str. The mongo uri to connect to the destination server
    :param dbname: str. The database name that will be populated with the backup data
    :param directory: str. The directory containing the backup as created by the function "run_backup"
    :return: bool. True on success, False on error. On failure, the error will be logged on the console
    """
    client = MongoClient(mongo_uri)
    db = client[dbname]

    dir_files = os.listdir(directory)
    max_len = 0
    n = 0
    count = len(dir_files)

    for filename in dir_files:
        n += 1

        if not filename.endswith('.bson'):
            print(f'\nSkip file "{filename}" because it is not part of the backup')
            continue

        collection_name = os.path.splitext(filename)[0]
        max_len = print_on_same_line(f'[{n}/{count}] Restore {collection_name} ...', max_len)

        try:
            with open(os.path.join(directory, filename), 'rb+') as f:
                data = bson.decode_all(f.read())

                if not data:
                    # skip empty collections as it is an error to do an "insert_many" with no data
                    print(f'Skip it because it is empty.')
                else:
                    db[collection_name].insert_many(data)

        except pymongo_errors.BulkWriteError as e1:
            print(f'\n{e1.details["writeErrors"][0]["errmsg"]}')
            print('It is possible that you are trying to restore the db again')
            return False

        except Exception as e2:
            print(f'\nError creating the collection "{collection_name}" from backup file "{filename}": {e2}')
            return False

    print('\n')
    return True


def backup_data(bool_restore, list_data):
    return_code, input_params, source_mongo_uri, destination_mongo_uri, backup_name, list_f = \
        capture_input_parameters(list_data=list_data)
    if return_code == response_codes.SUCCESS:
        try:
            src_dbname = input_params.get('source').get('dbname')
            dest_dbname = input_params.get('destination').get('dbname')


            # Create a new backup from the actual MongoDB database
            backup_name = run_backup(source_mongo_uri, src_dbname, backup_name)

            if backup_name:
                print(f'* A new backup "{backup_name}" was created successfully')
            else:
                exit(-1)
            if bool_restore:
                if restore_db(destination_mongo_uri, dest_dbname, backup_folder_for(backup_name)):
                   pass
        except Exception as ex:
            return_code = response_codes.UNEXPECTED_ERRROR
        return return_code
    else:
        return return_code