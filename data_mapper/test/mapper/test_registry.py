import os
import os.path
import unittest

from data_mapper.mapper.registry import MapperRegistry
from data_mapper.mapper.registry import RegisterMapperError
from data_mapper.mapper.registry import GetMapperError

from data_mapper.database.base import DatabaseProfile
from data_mapper.database.base import DatabaseSystem
from data_mapper.database.registry import DatabaseRegistry
from data_mapper.database.registry import GetProfileError
from data_mapper.database.registry import GetDatabaseError
from data_mapper.database.fields import DatabaseStringField

from data_mapper.model import Model
from data_mapper.exceptions import DataMapperError


class TestMapperRegistry(unittest.TestCase):
    """
    Tests for class MapperRegistry.
    """

    # =========================================================================
    # Define some paths to profile files, needed in the unittests below.

    def resolve_file_path(path):
        """
        Returns the absolute file path to the given path that is seen as a
        path, relative to the directory in which this script is stored.
        """
        dirname = os.path.realpath(os.path.dirname(__file__))
        return os.path.join(dirname, path)

    # Define the path to a profiles file that contains a single valid profile.
    profiles_file_single_profile = resolve_file_path(
        "../database/resources/db_profiles_single_profile.conf"
    )
    # Define the path to a profiles file that contains two valid profiles.
    profiles_file_two_profiles = resolve_file_path(
        "../database/resources/db_profiles_two_profiles.conf"
    )

    # =========================================================================

    def tearDown(self):
        """
        Defines actions to execute after each unittest method.
        """
        MapperRegistry.clear()

    # =========================================================================
    # Tests for the method clear() and initialize().

    def test_clear_and_initialize(self):
        """
        Tests the method clear() and initialize().
        """
        # Test the method, given that the registry is uninitialized.
        MapperRegistry.clear()
        # Make sure that the registry is not initialized.
        self.assertTrue(len(MapperRegistry.registered_mappers) == 0)
        self.assertFalse(MapperRegistry.is_initialized)

        # Initialize the registry.
        MapperRegistry.initialize()
        # Make sure, that the registry is now initialized.
        self.assertTrue(len(MapperRegistry.registered_mappers) == 0)
        self.assertTrue(MapperRegistry.is_initialized)

        # Clear the registry again.
        MapperRegistry.clear()
        # Again, make sure that the registry is not initialized.
        self.assertTrue(len(MapperRegistry.registered_mappers) == 0)
        self.assertFalse(MapperRegistry.is_initialized)

    # =========================================================================
    # Tests for the method clear() and initialize().

    def test_register_with_invalid_model(self):
        """
        Tests the method register() on a class that is not a subclass of Model.
        """
        # Register with no given profile and no database fields.
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register()  # NOQA
            class DummyModel:
                pass
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Register with given profile name.
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register()  # NOQA
            class DummyModel:
                pass
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Register with given profile.
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_profile=DatabaseProfile("MyProfile"))  # NOQA
            class DummyModel:
                pass
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_register_with_various_database_fields(self):
        """
        Tests the method register() on various db_fields.
        """
        # Register model with no given database fields.
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register()  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Register model with *list* of database fields (dict is expected).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields=[])  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 4.
        self.assertEqual(context.exception.code, 4)

        # Register model with empty dict of database fields.
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 5.
        self.assertEqual(context.exception.code, 5)

        # Register model with malformed database fields (name is None).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={None: None})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 6.
        self.assertEqual(context.exception.code, 6)

        # Register model with malformed database fields (name is empty).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={"": None})   # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 7.
        self.assertEqual(context.exception.code, 7)

        # Register model with malformed database fields (name consists only of
        # white spaces).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={"   ": None})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 7.
        self.assertEqual(context.exception.code, 7)

        # Register model with malformed database fields (name is not a string).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={1: None})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 6.
        self.assertEqual(context.exception.code, 6)

        # Register model with malformed database fields (field is None).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={"field": None})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 8.
        self.assertEqual(context.exception.code, 8)

        # Register model with malformed database fields (field is not an
        # instance of DatabaseField).
        with self.assertRaises(RegisterMapperError) as context:
            @MapperRegistry.register(db_fields={"key": "value"})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 8.
        self.assertEqual(context.exception.code, 8)

        # Register model with valid database fields, but no given profiles.
        with self.assertRaises(GetProfileError) as context:
            @MapperRegistry.register(db_fields={"k": DatabaseStringField("k")})  # NOQA
            class DummyModel(Model):
                pass
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_register_with_various_profile_names(self):
        """
        Tests the method register() with various profile names.
        """
        # Test empty profile name.
        with self.assertRaises(GetProfileError) as context:
            @MapperRegistry.register(  # NOQA
                db_profile_name="",
                db_fields={
                    "key": DatabaseStringField("key")
                }
            )
            class DummyModel(Model):
                pass
        # We expect error code 1.
        self.assertEqual(context.exception.code, 1)

        # Test profile name with only white spaces.
        with self.assertRaises(GetProfileError) as context:
            @MapperRegistry.register(  # NOQA
                db_profile_name="  ",
                db_fields={
                    "key": DatabaseStringField("key")
                }
            )
            class DummyModel(Model):
                pass
        # We expect error code 1.
        self.assertEqual(context.exception.code, 1)

        # Test valid profile name.
        # Initialize the db registry in order to have registered profiles.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)
        db_fields = {"key": DatabaseStringField("key")}

        @MapperRegistry.register(  # NOQA
            db_profile_name="my-profile",
            db_fields=db_fields
        )
        class DummyModel(Model):
            pass

        # Make sure that a mapper was registered.
        self.assertTrue(len(MapperRegistry.registered_mappers) == 1)
        mapper = list(MapperRegistry.registered_mappers.values())[0]
        self.assertIsNotNone(mapper)
        self.assertIsNotNone(mapper.database)
        self.assertIsNotNone(mapper.database_fields)
        self.assertEqual(mapper.database.system, DatabaseSystem.MYSQL)
        self.assertDictEqual(mapper.database_fields, db_fields)

    def test_register_with_various_profils(self):
        """
        Tests the method register() with various profiles.
        """
        # Test profile that is not an instance of DatabaseProfile.
        with self.assertRaises(GetDatabaseError) as context:
            @MapperRegistry.register(  # NOQA
                db_profile="",
                db_fields={
                    "key": DatabaseStringField("key")
                }
            )
            class DummyModel(Model):
                pass
        # We expect error code 2.
        self.assertEqual(context.exception.code, 2)

        # Test profile that has no name.
        with self.assertRaises(GetDatabaseError) as context:
            @MapperRegistry.register(  # NOQA
                db_profile=DatabaseProfile(None),
                db_fields={
                    "key": DatabaseStringField("key")
                }
            )
            class DummyModel(Model):
                pass
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Test profile that has no system.
        with self.assertRaises(GetDatabaseError) as context:
            @MapperRegistry.register(  # NOQA
                db_profile=DatabaseProfile("MyProfile"),
                db_fields={
                    "key": DatabaseStringField("key")
                }
            )
            class DummyModel(Model):
                pass
        # We expect error code 4.
        self.assertEqual(context.exception.code, 4)

        # Test valid profile.
        # Initialize the db registry in order to have registered profiles.
        db_fields = {"key": DatabaseStringField("key")}

        @MapperRegistry.register(  # NOQA
            db_profile=DatabaseProfile("Profile", system="sqlite"),
            db_fields=db_fields
        )
        class DummyModel(Model):
            pass

        # Make sure that a mapper was registered.
        self.assertTrue(len(MapperRegistry.registered_mappers) == 1)
        mapper = list(MapperRegistry.registered_mappers.values())[0]
        self.assertIsNotNone(mapper)
        self.assertIsNotNone(mapper.database)
        self.assertIsNotNone(mapper.database_fields)
        self.assertEqual(mapper.database.system, DatabaseSystem.SQLITE)
        self.assertDictEqual(mapper.database_fields, db_fields)

    # =========================================================================
    # Tests for the method get_mapper()

    def test_get_mapper(self):
        """
        Test the method get_mapper().
        """
        # Test get_mapper with no input.
        with self.assertRaises(GetMapperError) as context:
            MapperRegistry.get_mapper(None)
        # We expect error code 1.
        self.assertEqual(context.exception.code, 1)

        # Test get_mapper with a model that is not a class.
        with self.assertRaises(GetMapperError) as context:
            MapperRegistry.get_mapper("model")
        # We expect error code 2.
        self.assertEqual(context.exception.code, 2)

        # Test get_mapper with a model that is not a subclass of Model.
        with self.assertRaises(GetMapperError) as context:
            MapperRegistry.get_mapper(str)
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Test get_mapper with a model that is not registered.
        class NotRegisteredModel(Model):
            pass
        with self.assertRaises(GetMapperError) as context:
            MapperRegistry.get_mapper(NotRegisteredModel)
        # We expect error code 4.
        self.assertEqual(context.exception.code, 4)

        # Test get_mapper with a registered model and registered databases.
        DatabaseRegistry.initialize()
        db_fields = {"key": DatabaseStringField("key")}
        @MapperRegistry.register(  # NOQA
            db_profile=DatabaseProfile("Profile", system="sqlite"),
            db_fields=db_fields
        )
        class RegisteredModel(Model):
            pass
        mapper = MapperRegistry.get_mapper(RegisteredModel)
        self.assertIsNotNone(mapper)
        self.assertIsNotNone(mapper.database)
        self.assertEqual(mapper.database.system, DatabaseSystem.SQLITE)
        self.assertIsNotNone(mapper.database_fields)
        self.assertDictEqual(mapper.database_fields, db_fields)

    # =========================================================================
    # Tests for the method validate_model()

    def test_validate_model(self):
        """
        Tests the method validate_model().
        """
        # Test model None.
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_model(None)
        # We expect error code 1.
        self.assertEqual(context.exception.code, 1)

        # Test model that is not a class.
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_model("model")
        # We expect error code 3.
        self.assertEqual(context.exception.code, 2)

        # Test model that is not a subclass of Model.
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_model(str)
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Test valid model.
        class ValidModel(Model):
            pass
        model = MapperRegistry.validate_model(ValidModel)
        self.assertEqual(model, ValidModel)

    # =========================================================================
    # Tests for the method validate_fields()

    def test_validate_fields(self):
        """
        Tests the method validate_fields() on various db_fields.
        """
        # Validate fields "None".
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields(None)
        # We expect error code 3.
        self.assertEqual(context.exception.code, 3)

        # Validate *list* of database fields (dict is expected).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields([])
        # We expect error code 4.
        self.assertEqual(context.exception.code, 4)

        # Validate empty dict of database fields.
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({})
        # We expect error code 5.
        self.assertEqual(context.exception.code, 5)

        # Validate malformed database fields (name is None).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({None: None})
        # We expect error code 6.
        self.assertEqual(context.exception.code, 6)

        # Validate malformed database fields (name is empty).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({"": None})
        # We expect error code 7.
        self.assertEqual(context.exception.code, 7)

        # Validate malformed database fields (name consists of white spaces).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({"  ": None})
        # We expect error code 7.
        self.assertEqual(context.exception.code, 7)

        # Validate malformed database fields (name is not a string).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({1: None})
        # We expect error code 6.
        self.assertEqual(context.exception.code, 6)

        # Validate malformed database fields (field is None).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({"field": None})
        # We expect error code 8.
        self.assertEqual(context.exception.code, 8)

        # Validate malformed database fields (field is not an instance of
        # DatabaseField).
        with self.assertRaises(DataMapperError) as context:
            MapperRegistry.validate_fields({"key": "value"})
        # We expect error code 8.
        self.assertEqual(context.exception.code, 8)

        # Validate valid database fields.
        db_fields = {"name": DatabaseStringField("name")}
        validated = MapperRegistry.validate_fields(db_fields)
        self.assertEqual(db_fields, validated)
