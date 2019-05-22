import psycopg2
import psycopg2.pool
from contextlib import contextmanager
import os


def get_connection(conn_string):
    conn = psycopg2.connect(conn_string)
    return conn


if "WGFORGE_DB_CONNECTION_STRING" not in os.environ:
    raise Exception("WGFORGE_DB_CONNECTION_STRING is empty, please set")

db_connection = get_connection(os.environ["WGFORGE_DB_CONNECTION_STRING"])

db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=os.environ["WGFORGE_DB_CONNECTION_STRING"])


# As a member function within the AbstractConnectionPool class
@contextmanager
def db_pool_connection():
    try:
        conn = db_pool.getconn()
        with conn as real_conn:
            yield real_conn
    except:
        raise
    finally:
        db_pool.putconn(conn)
