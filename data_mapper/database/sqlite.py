from data_mapper.database.base import Database
from data_mapper.database.base import DatabaseSystem


class SQLiteDatabase(Database):
    """
    A class that acts as an interface to an instance of a SQLite database.
    """
    system = DatabaseSystem.SQLITE

    def __init__(self, db_profile):
        self.db_profile = db_profile
