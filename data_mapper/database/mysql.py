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

    def create_table(self, model, database_fields):
        statement = self.get_create_table_statement(model.__name__, None)
        print(statement)

    def exists_table(self, model):
        pass

    def save(self, instance):
        pass

    def get_create_table_statement(self, table_name, db_fields):
        # [IF NOT EXISTS]
        return "CREATE TABLE %s" % table_name

    def get_create_table_statement_entry(self, db_field):
        """
        Returns the entry for the given field in the CREATE TABLE statement.

        Args:
            db_field (DatabaseField): The database field to process.
        Returns:
            The entry for the given field in the CREATE TABLE statement.
        """
        pass

# CREATE TABLE MyGuests (
# id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# firstname VARCHAR(30) NOT NULL,
# lastname VARCHAR(30) NOT NULL,
# email VARCHAR(50),
# reg_date TIMESTAMP
# )

# NOT NULL - Each row must contain a value for that column, null values are not
# allowed
# DEFAULT value - Set a default value that is added when no other value is
# passed
# UNSIGNED - Used for number types, limits the stored data to positive numbers
# and zero
# AUTO INCREMENT - MySQL automatically increases the value of the field by 1
# each time a new record is added
# PRIMARY KEY - Used to uniquely identify the rows in a table. The column with
# PRIMARY KEY setting is often an ID number, and is often used with
# AUTO_INCREMENT
