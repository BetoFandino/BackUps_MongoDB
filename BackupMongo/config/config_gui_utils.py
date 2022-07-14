from typing import Optional, Tuple

from BackupMongo.Backup_process.backup_utils import list_existing_backups
from BackupMongo.console_utils import ask_yes_or_no
from BackupMongo.db_utils import mongo_db_uri


def capture_input_parameters(config, accept_transfer_message: str, skip_use_backup: bool = False) -> \
        Tuple[dict, Optional[str], str, Optional[str]]:
    """
    Capture the source and destination databases for any db operation you want to do after.
    This function first tries to get the parameters from the json file passed as the command-line parameter
    to this tool, if none is specified, it asks the user the parameters via console input.

    If the parameters were capture from a file (without user intervention), a confirmation message will be displayed
    before returning the function. If the user answers 'N' the operation will be cancelled.

    :param accept_transfer_message: str. The subject of the question on the confirmation message;
      For example, "indices" if you are transferring the indices from a db to another or "collections" if you are
      transferring the collections from a db to another.

    :param skip_use_backup: bool. If True, will not use any existing backup regardless what the provided
      configuration says. This is used mainly when restoring the indices, as the feature to back up the indices on
      disk it is not available yet. If not provided, the parameter defaults to False.

    :return: Tuple[dict, Optional[str], str, Optional[str]]. The first value contains the input parameters.
      The second value is the source mongo_uri (the uri to connect to the source database) or
      None if provided an existing backup to use.
      The third value is the destination mongo_uri (the uri to connect to the destination database)
      The fourth value is the provided existing backup to use or None if the backup needs to be created from the
      actual MongoDB database
    """

    if config:
        # Configuration file provided

        source = config.get('source')
        dest = config.get('destination')
        use_backup = None if skip_use_backup else config.get('use_backup')

        src_username = source.get('username')
        src_password = source.get('password')
        src_auth_source = source.get('authSource') or 'admin'
        src_host = source.get('host') or 'localhost'
        src_port = source.get('port') or 27017
        src_dbname = source.get('dbname')

        dest_username = dest.get('username')
        dest_password = dest.get('password')
        dest_auth_source = dest.get('authSource') or 'admin'
        dest_host = dest.get('host') or 'localhost'
        dest_port = dest.get('port') or 27017
        dest_dbname = dest.get('dbname')

        if not src_dbname:
            print('Error: The source dbname is not defined on the configuration')
            exit(-1)

        if not dest_dbname:
            print('Error: The destination dbname is not defined on the configuration')
            exit(-1)

        if use_backup:
            existing_backups = list_existing_backups()

            if not existing_backups:
                print('\nThere are not backups available')
                exit(-1)

            if use_backup == '{{last}}':
                use_backup = existing_backups[-1]

            elif use_backup not in existing_backups:
                print(f'\nThe backup "{use_backup}" is not available')
                exit(-1)

            print(f'* Use an existing backup: \n'
                  f'    From: {use_backup} \n'
                  f'    To:   {dest_host}:{dest_port}/{dest_dbname}')

        else:
            print(f'* Transferring the {accept_transfer_message}: \n'
                  f'    From: {src_host}:{src_port}/{src_dbname} \n'
                  f'    To:   {dest_host}:{dest_port}/{dest_dbname}')

        if not ask_yes_or_no('Is that correct?'):
            print('\nCancelled')
            exit(-1)

        if use_backup:
            source_mongo_uri = None
        else:
            source_mongo_uri = mongo_db_uri(src_username, src_password,
                                            src_host, src_port, src_dbname, src_auth_source)

    else:
        # Configuration file not provided, read command-line input

        use_backup = False if skip_use_backup else \
            not ask_yes_or_no('Get fresh data? \n'
                              'Enter "Y" to connect to a source MongoDB or "N" to use an existing backup')

        if use_backup:
            existing_backups = list_existing_backups()

            print('Available backups:')
            n = 0
            for f in existing_backups:
                print(f'  {n}: {f}')
                n += 1

            if n > 1:
                error_msg = 'The value entered is not a valid.'
                print()

                while True:
                    # noinspection PyBroadException
                    try:
                        num = int(input(f'What backup to use? [between 0 and {n-1}] '))
                        if 0 <= num < len(existing_backups):
                            use_backup = existing_backups[num]
                            break
                        else:
                            print(error_msg)
                    except Exception:
                        print(error_msg)

            else:
                if ask_yes_or_no('Ok to use this one?'):
                    use_backup = existing_backups[0]
                else:
                    print('\nCancelled')
                    exit(0)

            source_part = {
                'use_backup': use_backup
            }

            source_mongo_uri = None

        else:
            print('\nSource server credentials:')
            src_username = input('Username [leave it blank if not needed]: ')
            src_password = input('Password [leave it blank if not needed]: ')
            src_auth_source = input('Auth Source [leave it blank for "admin"]: ')
            src_host = input('Host [leave it blank for localhost]: ')
            src_port = input('Port [leave it blank for 27017]: ')
            src_dbname = input('Database name: ')

            source_part = {
                'username': src_username,
                'password': src_password,
                'host': src_host,
                'port': src_port,
                'dbname': src_dbname,
            }

            source_mongo_uri = mongo_db_uri(src_username, src_password,
                                            src_host, src_port, src_dbname, src_auth_source)

        print('\nDestination server credentials:')
        dest_username = input('Username [leave it blank if not needed]: ')
        dest_password = input('Password [leave it blank if not needed]: ')
        dest_auth_source = input('Auth Source [leave it blank for "admin"]: ')
        dest_host = input('Host [leave it blank for localhost]: ')
        dest_port = input('Port [leave it blank for 27017]: ')
        dest_dbname = input('Database to restore: ')

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

    destination_mongo_uri = mongo_db_uri(dest_username, dest_password,
                                         dest_host, dest_port, dest_dbname, dest_auth_source)

    return config, source_mongo_uri, destination_mongo_uri, use_backup
