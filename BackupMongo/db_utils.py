import urllib.parse


def mongo_db_uri(username, password, host, port, dbname, auth_source):
    """
    Calculate a MongoDB uri given its connection parameters.

    :param username: str. The login username. If empty, no user/password will be included on the result
    :param password: str. The login password
    :param host: str. The server host to connect. If empty, it defaults to 'localhost'
    :param port: str. The server port. If empty, it defaults to '27017'
    :param dbname: str. The database to connect
    :param auth_source: str. The field authSource on the connection string. It is usually "admin" for global users or
           the database you are connecting to for db-specific users. Check the MongoDB documentation for more info
    :return: str. The uri you can use when connecting to the MongoDB server
    """
    if not host:
        host = 'localhost'

    if not port:
        port = '27017'

    is_local = len(username) == 0

    if is_local:
        user_part = ''
    else:
        if password:
            enc_password = urllib.parse.quote(password)
            user_part = f'{username}:{enc_password}@'
        else:
            user_part = f'{username}@'

    if auth_source:
        auth_source_part = f'authSource={auth_source}&'
    else:
        auth_source_part = ''

    return f'mongodb://{user_part}{host}:{port}/{dbname}?{auth_source_part}readPreference=primary&ssl=false'
