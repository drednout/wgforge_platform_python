class DbError(Exception):
    pass


class DbEntityNotFound(DbError):
    pass