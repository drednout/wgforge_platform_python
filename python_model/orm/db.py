import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker





def get_connection(conn_string):
    engine = create_engine(conn_string)
    conn = engine.connect()
    return conn


def init_engine_session(conn_string):
    global Session
    engine = create_engine(conn_string)
    Session = sessionmaker()
    Session.configure(bind=engine)


def get_session():
    session = Session()
    return session


if "WGFORGE_DB_CONNECTION_STRING" not in os.environ:
    raise Exception("WGFORGE_DB_CONNECTION_STRING is empty, please set")

db_connection = get_connection(os.environ["WGFORGE_DB_CONNECTION_STRING"])
Session = None
init_engine_session(os.environ["WGFORGE_DB_CONNECTION_STRING"])
db_session = get_session()
