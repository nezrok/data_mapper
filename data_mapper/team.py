from data_mapper.database.registry import DatabaseRegistry
from data_mapper.mapper.base import MapperRegistry
from data_mapper.database.base import DatabaseStringField
from data_mapper.model.base import Model

DatabaseRegistry.initialize(profiles_file_path="database_profiles.conf")


@MapperRegistry.register(
   db_profile=None,
   db_profile_name=None,
   db_fields={
       "name": DatabaseStringField(),
       "token": DatabaseStringField()
   }
)
class Team(Model):
    pass


# profile = DatabaseProfile(db_user="root", db_password="admin")
# db = MySqlDatabase(profile)
# db.create_db_table(Team)
