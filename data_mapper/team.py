import os

from data_mapper.database.registry import DatabaseRegistry
from data_mapper.database.fields import DatabaseStringField

from data_mapper.mapper.registry import MapperRegistry

from data_mapper.model import Model


def resolve_file_path(path):
    """
    Returns the absolute file path to given path that is seen as a path,
    relative to the directory in which this script is stored.
    """
    dirname = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(dirname, path)


DatabaseRegistry.initialize(
    profiles_file_path=resolve_file_path("resources/database_profiles.conf")
)


@MapperRegistry.register(
   db_profile=None,
   db_profile_name=None,
   db_fields={
       "name": DatabaseStringField("name"),
       "token": DatabaseStringField("token")
   }
)
class Team(Model):
    def __init__(self):
        self.mapper = MapperRegistry.get_mapper(self.__class__)
        # self.mapper.create_db_table()


Team()
# profile = DatabaseProfile(db_user="root", db_password="admin")
# db = MySqlDatabase(profile)
# db.create_db_table(Team)
