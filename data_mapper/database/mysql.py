# import pymysql

from data_mapper.database.base import Database
from data_mapper.database.base import DatabaseSystem


# cursor.execute("SELECT name FROM teams")
# for x in cursor:


# TODO: Default port if port is not given in profile.
# TODO: Default host.
# TODO: Create database if it not exist.
# TODO: On save an instance, validate the values of each field.
# TODO: On save an instance, check if table exists and create if it not exists.
# TODO: On save an instance, check if field specifications matches the table.

class MySQLDatabase(Database):
    """
    A class that acts as an interface to an instance of a MYQSL database.
    """
    system = DatabaseSystem.MYSQL

    def __init__(self, db_profile):
        self.db_profile = db_profile
        # self.conn = pymysql.connect(
        #    host=db_profile.host,
        #    port=db_profile.port,
        #    user=db_profile.user,
        #    password=db_profile.password,
        #    database=db_profile.name
        # )
        # self.cursor = self.conn.cursor()

    def create_db_table(self, model):
        statement = self.get_create_db_table_statement(model.__name__, None)
        print(statement)

    def exists_db_table(self, model):
        pass

    def save(self, instance):
        pass

    def get_create_db_table_statement(self, table_name, db_fields):
        return "CREATE TABLE %s" % table_name
