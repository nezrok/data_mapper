from enum import Enum

# =============================================================================
# Database and Database Fields.


class Database:
    """
    An abstract class that acts as an interface to any database system.
    """
    system = None

    def save(self, instance):
        """
        Writes the given model instance to the underlying database.

        Args:
            instance (Model): The model instance to write to the database.
        Returns:
            True if the model was successfully written to the database; False
            otherwise.
        """
        pass

    def exists_db_table(self, model):
        """
        Returns True, if there exists a table for the given model class in the
        underyling database.

        Args:
            model (class of Model): The model class to process.
        Returns:
            True, if there exists a table for the given model class in the
                underyling database; False otherwise.
        """
        pass

    def create_db_table(self, model):
        """
        Creates a table for the given model in the underlying database.

        Args:
            model (class of Model): The model class to process.
        Returns:
            True if the table was successfully created; False otherwise.
        """
        pass

# =============================================================================
# Util classes.


class DatabaseProfile:
    """
    A class that gives metadata and credentials of a concrete database
    instance.
    """
    def __init__(self, name, system=None, host=None, port=None, user=None,
                 password=None, db=None):
        """
        Creates a new database profile.

        Args:
            name (str): The name of the profile.
            system (DatabaseSystem): The system of the underlying database.
            host (str): The host to use on connecting to the database.
            port (int): The port to use on connecting to the database.
            user (str): The username to use on authentication.
            password (str): The password to use on authentication.
            db (str): The name of the database.
        """
        self.name = name
        self.system = system
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def __str__(self):
        return "DatabaseProfile(%s)" % self.__dict__

    def __repr__(self):
        return self.__str__()


class DatabaseSystem(Enum):
    """
    An enumeration of various database systems.
    """
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    COUCHDB = "couchdb"
