from data_mapper.model.base import Model
from data_mapper.database.registry import DatabaseRegistry

# TODO: Implement logic to validate, save, edit, delete, get from database.
# TODO: Unique ids.
# TODO: Thread-safe?


class MapperRegistry:
    # The database field specifications per model.
    db_fields_per_model = {}
    # The mappers per model.
    registered_mappers = {}

    @classmethod
    def register(cls, db_profile=None, db_profile_name=None, db_fields=None):
        def decorator(model):
            # Check if the given model is valid.
            if not issubclass(model, Model):
                raise MapperRegistryError(
                    mess="The model '%s' must implement '%s'."
                         % (model.__name__, Model),
                    code=1
                )

            # Check if the model is already registered.
            if model in cls.registered_mappers:
                raise MapperRegistryError(
                    mess="The model '%s' is already registered."
                         % (model.__name__),
                    code=2
                )

            # Check if there are db fields given.
            if db_fields is None or len(db_fields) == 0:
                raise MapperRegistryError(
                    mess="No db field specifications given for model '%s'."
                         % (model.__name__),
                    code=2
                )

            # Try to get the related database instance.
            database = DatabaseRegistry.get_database(
                profile=db_profile,
                profile_name=db_profile_name
            )

            # Instantiate the mapper.
            mapper = Mapper(database)

            # Register the mapper.
            cls.registered_mappers[model] = mapper

            # print(cls.registered_mappers)

            return model
        return decorator


class Mapper:
    def __init__(self, database):
        self.database = database


class MapperRegistryError(Exception):
    """
    An error to raise on registering a database.
    """
    def __init__(self, mess=None, code=-1):
        """
        Creates a new DatabaseRegistryError.

        Args:
            mess (str): The message to show.
            code (int): The status code.
        """
        super().__init__(mess)
        self.code = code
