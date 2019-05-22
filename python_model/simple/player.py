from .error import DbEntityNotFound


class Player(object):
    """Model class for player entity.
    """

    GET_BY_ID = """
        SELECT 
            id, nickname, email, password, created, updated 
        FROM 
            player
        WHERE id=%(id)s
    """
    GET_BY_NICKNAME = """
        SELECT 
            id, nickname, email, password, created, updated 
        FROM 
            player
        WHERE nickname=%(nickname)s
    """
    INSERT = """
        INSERT INTO player 
            (nickname, email, password) 
        VALUES 
            (%(nickname)s, %(email)s, %(password)s)
        RETURNING
            id, created, updated
    """

    UPDATE_BY_ID = """WRITE SQL HERE"""
    DELETE_BY_ID = """WRITE SQL HERE"""

    def __init__(self, nickname=None, email=None, password=None, _id=None,
                 created=None, updated=None, db_connection=None):
        self.nickname = nickname
        self.email = email
        self.password = password
        self.id = _id
        self.created = created
        self.updated = updated
        self.db_connection = db_connection


    def load_by_id(self, _id):
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.GET_BY_ID, {"id": _id})
            row = cursor.fetchone()
            self.id = row[0]
            self.nickname = row[1]
            self.email = row[2]
            self.password = row[3]
            self.created = row[4]
            self.created = row[5]


    def load_by_nickname(self, nickname):
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.GET_BY_NICKNAME, {"nickname": nickname})
            row = cursor.fetchone()
            if row is None:
                raise DbEntityNotFound("Player with nickname `{}` is not found".format(nickname))

            self.id = row[0]
            self.nickname = row[1]
            self.email = row[2]
            self.password = row[3]
            self.created = row[4]
            self.created = row[5]


    def insert(self):
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.INSERT, {"nickname": self.nickname,
                                         "password": self.password,
                                         "email": self.email})
            insert_info = cursor.fetchone()
            self.db_connection.commit()
            self.id = insert_info[0]
            self.created = insert_info[1]
            self.updated = insert_info[2]


    def update(self):
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.UPDATE_BY_ID, {"id": self.id,
                                               "nickname": self.nickname,
                                               "password": self.password,
                                               "email": self.email})
            self.db_connection.commit()

    def delete(self):
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.DELETE_BY_ID, {"id": self.id})
            self.db_connection.commit()


    def as_dict(self):
        d = {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "created": self.created,
            "updated": self.updated
        }
        return d
