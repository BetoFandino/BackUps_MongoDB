import datetime
import os
from typing import Tuple


def backups_root():
    """Return the root directory where the backups are located."""
    root = os.environ.get('BACKUP_ROOT', '')
    return os.path.join(root, '../BackUps')


def backup_folder_for(backup_name: str) -> str:
    """
    Return the directory where a specific backups is/should be located.
    :param backup_name: str. The name of the backup. It can be either an existing backup or a new one to be created
    :return: str. The directory path for the backup
    """
    return os.path.join(backups_root(), backup_name)


def list_existing_backups() -> list:
    """
    Return a list of the existing backups in the backup root directory.

    :return: list. The name of the existing backups
    """
    root = backups_root()
    result = list([f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))])
    result.sort()
    return result


def create_folder_backup(db_name: str, backup_na: str) -> Tuple[str, str]:
    """
    Create the directory where the backup will be stored and return the path to it. Any intermediate directory
    will be created if needed.

    :param db_name: str. The name of the database to back up
    :return: Tuple[str, str]. The first value is the directory for the backup. The second value is the backup name
    """
    dt = datetime.datetime.now()
    backup_name = f'{backup_na}_{db_name}_{dt.month}-{dt.day}-{dt.year}__{dt.hour}_{dt.minute}'
    backup_dir = backup_folder_for(backup_name)

    if os.path.exists(backup_dir):
        print(f'Backup files in "{backup_dir}" will be overwritten...')
    else:
        os.makedirs(backup_dir)

    return backup_dir, backup_name
