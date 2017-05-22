import logging
from mysql import connector

host = 'host'
port = 'port'
username = 'username'
password = 'password'

def get_mysql_conn(schema):
    conn = connector.connect(host=host,
                             user=username,
                             password=password,
                             port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("USE {}".format(schema))
    return conn, cursor

def create_connection():
    pass


def create_table(schema, table):
    conn, cursor = get_mysql_conn()
    if table_exists(table):
        logging.warning('Table already exists')
        return
    cols = {'first_name': "VARCHAR(32)",
            'last_name': "VARCHAR(32)"}
    col_str = ', '.join([key + ' ' + cols[key] for key in cols])
    cursor.execute("""CREATE TABLE {}.{} ({})""".format(schema, table, col_str))
    conn.disconnect()


def drop_table(schema, table):
    conn, cursor = get_mysql_conn()
    if table_exists(table):
        cursor.execute("""DROP TABLE {}.{}""".format(schema, table))
    conn.disconnect()


def table_exists(schema, table):
    conn, cursor = get_mysql_conn()
    cursor.execute("""SELECT * FROM information_schema.tables
                      WHERE table_schema = '{}'
                      AND table_name = '{}'
                      LIMIT 1;""".format(schema, table))
    results = cursor.fetchall()
    conn.disconnect()
    return bool(results)


def reset_table(table):
    if table_exists(table):
        drop_table(table)
    create_table(table)
