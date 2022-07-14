from pymongo import MongoClient
from config.config_utils import capture_input_parameters
from console_utils import print_on_same_line


def restore_index(mongo_source_uri, source_db_name, mongo_destination_uri, destination_db_name) -> bool:
    """
    Restore the indices of a database from another source db.

    :param mongo_source_uri: str. The uri to connect to the source MongoDB server
    :param source_db_name: st. The destination database where the indices will be created
    :param mongo_destination_uri: str. The uri to connect to the destination MongoDB server
    :param destination_db_name: str. The source database where the indices are read from
    :return: bool. True on success, False on error. On failure, the error will be logged on the console
    """
    try:
        source_client = MongoClient(mongo_source_uri)
        source_db = source_client[source_db_name]
    except Exception as e:
        print(f'Error connecting to the source server "{mongo_source_uri}" to read the indices: {e}')
        return False

    try:
        destination_client = MongoClient(mongo_destination_uri)
        destination_db = destination_client[destination_db_name]
    except Exception as e:
        print(f'Error connecting to the destination server "{mongo_source_uri}" to restore the indices: {e}')
        return False

    # Read source and destination collection names
    try:
        source_collections = source_db.list_collection_names()
        destination_collections = destination_db.list_collection_names()
    except Exception as e:
        print(f'Error reading the collection names to process: {e}')
        return False

    # These keys should be removed from the index data to maximize compatibility
    index_keys_to_remove = ['v', 'ns', 'background', 'foreground']

    # Transfer the indices
    max_len = 0
    n = 0
    count = len(source_collections)

    try:
        for collection_name in source_collections:
            n += 1
            max_len = print_on_same_line(f'[{n}/{count}] Restore indices for {collection_name} ...', max_len)

            source_index_data = source_db[collection_name].index_information().items()
            for dest_coll in destination_collections:
                if collection_name == dest_coll:
                    for idx_name, idx_data in source_index_data:
                        if idx_name == '_id_':
                            # do not transfer the index "_id_" because it is automatically created
                            continue

                        for k in index_keys_to_remove:
                            if k in idx_data.keys():
                                del idx_data[k]

                        destination_db[dest_coll].create_index(keys=idx_data['key'], name=idx_name, **idx_data)

    except Exception as e:
        print(f'\nError restoring the index: {e}')
        return False

    print('\n')
    return True


def restore_i(list_data):
    return_code, input_params, source_mongo_uri, destination_mongo_uri, backup_name, list_f = \
        capture_input_parameters(list_data=list_data)

    src_dbname = input_params.get('source').get('dbname')
    dest_dbname = input_params.get('destination').get('dbname')

    if restore_index(source_mongo_uri, src_dbname, destination_mongo_uri, dest_dbname):
        print('* Indices restored')
