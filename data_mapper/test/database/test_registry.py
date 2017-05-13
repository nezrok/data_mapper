import unittest
import os
import os.path

from data_mapper.database.base import Database
from data_mapper.database.base import DatabaseSystem
from data_mapper.database.base import DatabaseProfile

from data_mapper.exceptions import DataMapperError

from data_mapper.database.registry import DatabaseRegistry
from data_mapper.database.registry import RegisterDatabaseError
from data_mapper.database.registry import RegisterProfileError
from data_mapper.database.registry import GetProfileError
from data_mapper.database.registry import GetDatabaseError
from data_mapper.database.registry import ParseProfileConfigFileError


class TestDatabaseRegistry(unittest.TestCase):
    """
    Tests for class DatabaseRegistry.
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

    # Define the path to a profiles file that does not exist.
    profiles_file_not_existing = resolve_file_path(
        "resources/db_profiles_not_existing.conf"
    )
    # Define the path to a profiles file that is not readable.
    profiles_file_not_readable = resolve_file_path(
        "resources/db_profiles_not_readable.conf"
    )
    # Define the path to a profiles file that is malformed.
    profiles_file_malformed = resolve_file_path(
        "resources/db_profiles_malformed.conf"
    )
    # Define the path to a profiles file with a profile with no db system.
    profiles_file_no_system = resolve_file_path(
        "resources/db_profiles_no_db_system.conf"
    )
    # Define the path to a profiles file with a profile with an invalid system.
    profiles_file_invalid_system = resolve_file_path(
        "resources/db_profiles_no_db_system.conf"
    )
    # Define the path to a profiles file that contains a single valid profile.
    profiles_file_single_profile = resolve_file_path(
        "resources/db_profiles_single_profile.conf"
    )
    # Define the path to a profiles file that contains two valid profiles.
    profiles_file_two_profiles = resolve_file_path(
        "resources/db_profiles_two_profiles.conf"
    )

    # =========================================================================

    def tearDown(self):
        """
        Defines actions to execute after each unittest method.
        """
        DatabaseRegistry.clear()

    # =========================================================================
    # Tests for the method clear() and initialize().

    def test_clear_and_initialize(self):
        """
        Tests the method clear() and initialize().
        """
        # Test the method, given that the registry is uninitialized.
        DatabaseRegistry.clear()
        # Make sure that there are no registered databases and profiles.
        self.assertTrue(len(DatabaseRegistry.registered_databases) == 0)
        self.assertTrue(len(DatabaseRegistry.registered_profiles) == 0)
        self.assertFalse(DatabaseRegistry.is_initialized)

        # Initialize the registry in order to have a registered profile.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)
        # Make sure, that there are registered databases and profiles now.
        self.assertTrue(len(DatabaseRegistry.registered_databases) > 0)
        self.assertTrue(len(DatabaseRegistry.registered_profiles) > 0)
        self.assertTrue(DatabaseRegistry.is_initialized)

        # Clear the registry again.
        DatabaseRegistry.clear()
        # Make sure, that there are *no* registered databases and profiles now.
        self.assertTrue(len(DatabaseRegistry.registered_databases) == 0)
        self.assertTrue(len(DatabaseRegistry.registered_profiles) == 0)
        self.assertFalse(DatabaseRegistry.is_initialized)

    # =========================================================================
    # Tests for the method initialize().

    def test_initialize_without_profile_file(self):
        """
        Tests the method initialize() *without* passing a path to a profile
        config file.
        """
        # Initialize the registry.
        DatabaseRegistry.initialize()

        # Make sure that there are registered databases, but no profiles.
        self.assertTrue(len(DatabaseRegistry.registered_databases) > 0)
        self.assertTrue(len(DatabaseRegistry.registered_profiles) == 0)
        self.assertTrue(DatabaseRegistry.is_initialized)

    def test_initialize_with_profile_file_with_single_profile(self):
        """
        Tests the method initialize() *with* passing a path to a profile
        config file that contains a single profile.
        """
        # Initialize the registry in order to have a registered profile.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # Make sure that there are databases and exactly one profile.
        self.assertTrue(len(DatabaseRegistry.registered_databases) > 0)
        self.assertTrue(len(DatabaseRegistry.registered_profiles) == 1)
        self.assertTrue(DatabaseRegistry.is_initialized)

    def test_initialize_with_profile_file_with_two_profiles(self):
        """
        Tests the method initialize() *with* passing a path to a profile
        config file that contains two profiles.
        """
        # Initialize the registry in order to have two registered profiles.
        DatabaseRegistry.initialize(self.profiles_file_two_profiles)

        # Make sure that there are databases and exactly two profiles.
        self.assertTrue(len(DatabaseRegistry.registered_databases) > 0)
        self.assertTrue(len(DatabaseRegistry.registered_profiles) == 2)
        self.assertTrue(DatabaseRegistry.is_initialized)

    # =========================================================================
    # Tests for the method register_database().

    def test_register_database_with_no_database(self):
        """
        Tests the method register_database() *without* passing a database.
        """
        # Try to register a database "None". Make sure that an error is raised.
        with self.assertRaises(RegisterDatabaseError) as context:
            DatabaseRegistry.register_database(None)
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_register_database_with_invalid_database(self):
        """
        Tests the method register_database() with an object that is not a
        subclass of Database.
        """
        # Define a dummy database that is *not* a subclass of Database.
        class DummyDatabase:
            pass

        # Try to register the database. Make sure that an error is raised.
        with self.assertRaises(RegisterDatabaseError) as context:
            DatabaseRegistry.register_database(DummyDatabase)
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_register_database_with_database_of_invalid_system(self):
        """
        Tests the method register_database() with an database of an invalid
        system.
        """
        # Define a dummy database with an invalid database system.
        class DummyDatabase(Database):
            system = "DummySystem"

        # Try to register the database. Make sure that an error is raised.
        with self.assertRaises(RegisterDatabaseError) as context:
            DatabaseRegistry.register_database(DummyDatabase)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_register_database_with_valid_database(self):
        """
        Tests the method register_database() with an valid database.
        """
        # Define a dummy database with an valid database system.
        class DummyDatabase(Database):
            system = DatabaseSystem.MYSQL

        # Register the database. Make sure that *no* error is raised.
        DatabaseRegistry.register_database(DummyDatabase)
        registered_databases = DatabaseRegistry.registered_databases

        # Make sure that the database was registered correctly.
        self.assertEqual(len(registered_databases), 1)
        self.assertTrue(DummyDatabase.system.value in registered_databases)
        self.assertTrue(DummyDatabase in registered_databases.values())

    # =========================================================================
    # Tests for the method register_profile().

    def test_register_profile_with_no_profile(self):
        """
        Tests the method register_profile() *without* passing a profile.
        """
        # Try to register a profile "None". Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(None)
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_register_database_with_invalid_profile(self):
        """
        Tests the method register_profile() *with* an object that is *not* an
        instance of DatabaseProfile.
        """
        # Try to register a profile that is not an instance of DatabaseProfile.
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(object())
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_register_profile_with_no_name(self):
        """
        Tests the method register_profile() with no/empty name.
        """
        # Try to register a profile that has no name.
        profile = DatabaseProfile(None)
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Try to register a profile with an empty name.
        profile = DatabaseProfile("")
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Register a profile with a name that consists only of white spaces.
        profile = DatabaseProfile("     ")
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_register_profile_with_no_db_system(self):
        """
        Tests the method register_profile() with no/empty database system.
        """
        # Try to register a profile that has no system.
        profile = DatabaseProfile("myprofile")
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 4.
        self.assertEqual(context.exception.code, 4)

        # Try to register a profile with an empty system.
        profile = DatabaseProfile("myprofile", system="")
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 4.
        self.assertEqual(context.exception.code, 4)

        # Try to register a profile with a system that consists only of spaces.
        profile = DatabaseProfile("myprofile", system="    ")
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 4.
        self.assertEqual(context.exception.code, 4)

    def test_register_profile_with_invalid_db_system(self):
        """
        Tests the method register_profile() with an profile that has an invalid
        database system.
        """
        # Try to register a profile with an invalid system "dummy".
        profile = DatabaseProfile("myprofile", system="dummy")
        # Make sure that an error is raised.
        with self.assertRaises(RegisterProfileError) as context:
            DatabaseRegistry.register_profile(profile)
        # We expect the error code 5.
        self.assertEqual(context.exception.code, 5)

    def test_register_profile_with_valid_profile(self):
        """
        Tests the method register_profile() with an valid profile.
        """
        # Initialize the registry in order to have registered databases.
        DatabaseRegistry.initialize()

        # Test the method three times, each time with the same system, but
        # different cases (to check if system validation is case-insensitive).

        # (1) Try to register a profile with system "mysql".
        # Make sure that *no* error is raised.
        profile = DatabaseProfile("myprofile", system="mysql")
        DatabaseRegistry.register_profile(profile)
        registered_profiles = DatabaseRegistry.registered_profiles
        self.assertEqual(len(registered_profiles), 1)
        self.assertTrue(profile.name in registered_profiles)
        self.assertTrue(profile in registered_profiles.values())

        # (2) Try to register a profile with system "MYSQL".
        # Make sure that *no* error is raised.
        profile = DatabaseProfile("myprofile", system="MYSQL")
        DatabaseRegistry.register_profile(profile)
        registered_profiles = DatabaseRegistry.registered_profiles
        self.assertEqual(len(registered_profiles), 1)
        self.assertTrue(profile.name in registered_profiles)
        self.assertTrue(profile in registered_profiles.values())

        # (3) Try to register a profile with system "mYsQl".
        # Make sure that *no* error is raised.
        profile = DatabaseProfile("myprofile", system="mYsQl")
        DatabaseRegistry.register_profile(profile)
        registered_profiles = DatabaseRegistry.registered_profiles
        self.assertEqual(len(registered_profiles), 1)
        self.assertTrue(profile.name in registered_profiles)
        self.assertTrue(profile in registered_profiles.values())

    # =========================================================================
    # Tests for method get_database()

    def test_get_database_with_no_profile_and_no_profile_name(self):
        """
        Tests the method get_database() with no given profile and no given
        profile name.
        """
        # Test the method when *no* databases and *no* profiles are registered.
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database()
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Test the method when databases but *no* profiles are registered.
        DatabaseRegistry.initialize()
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database()
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Test the method when a single profile is registered.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)
        database = DatabaseRegistry.get_database()
        # Make sure that the database for the *latest* profile is returned.
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "my-profile")

        # Test the method when two profiles are registered.
        DatabaseRegistry.initialize(self.profiles_file_two_profiles)
        database = DatabaseRegistry.get_database()
        # Make sure that the *latest* registered database is returned.
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.SQLITE)
        self.assertEqual(database.db_profile.name, "second-profile")

    def test_get_database_with_profile_name(self):
        """
        Tests the method get_database() with given profile name.
        """
        # Test the method when *no* databases and *no* profiles are registered.
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database("my-profile")
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # Test the method when databases but *no* profiles are registered.
        DatabaseRegistry.initialize()
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database("my-profile")
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # Test the method when a single profile is registered, but the profile
        # name "fake-profile" is invalid.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database("fake-profile")
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # Test the method when a single profile is registered and the profile
        # name "my-profile" is valid.
        database = DatabaseRegistry.get_database("my-profile")
        # Make sure that the correct database was returned.
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "my-profile")

        # Test the method when two profiles are registered and the profile
        # name "fake-profile" is invalid.
        DatabaseRegistry.initialize(self.profiles_file_two_profiles)
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database("fake-profile")
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # Test the method when two profiles are registered and the profile
        # name is valid.
        database = DatabaseRegistry.get_database("first-profile")
        # Make sure that the correct database was returned.
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "first-profile")

        database = DatabaseRegistry.get_database("second-profile")
        # Make sure that the correct database was returned.
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.SQLITE)
        self.assertEqual(database.db_profile.name, "second-profile")

    def test_get_database_with_profile(self):
        """
        Tests the method get_database() with given profile.
        """
        # ---------------------------------------------------------------------
        # Test the method when *no* databases and *no* profiles are registered.

        # The given profile is invalid. Make sure that an error is raised.
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=object())
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The given profile has no name. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="mysql")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile has no system. Make sure that an error is raised.
        profile = DatabaseProfile(None)
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The profile has an invalid system. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="dummy")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile is valid. Make sure that an error is raised
        # (because there are no registered databases).
        profile = DatabaseProfile("DummyProfile", system="mysql")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 5.
        self.assertEqual(context.exception.code, 5)

        # ---------------------------------------------------------------------
        # Test the method when databases but no profiles are registered.
        DatabaseRegistry.initialize()

        # The given profile is invalid. Make sure that an error is raised.
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=object())
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The given profile has no name. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="mysql")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile has no system. Make sure that an error is raised.
        profile = DatabaseProfile(None)
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The profile has an invalid system. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="dummy")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile is valid. Make sure that *no* exception is raised.
        profile = DatabaseProfile("DummyProfile", system="mysql")
        database = DatabaseRegistry.get_database(profile=profile)
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "DummyProfile")

        # ---------------------------------------------------------------------
        # Test the method when databases and a single profile is registered.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # The given profile is invalid. Make sure that an error is raised.
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=object())
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The given profile has no name. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="mysql")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile has no system. Make sure that an error is raised.
        profile = DatabaseProfile(None)
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The profile has an invalid system. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="dummy")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile is valid. Make sure that *no* exception is raised.
        profile = DatabaseProfile("DummyProfile", system="mysql")
        database = DatabaseRegistry.get_database(profile=profile)
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "DummyProfile")

        # ---------------------------------------------------------------------
        # Test the method when databases and two profiles are registered.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # The given profile is invalid. Make sure that an error is raised.
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=object())
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The given profile has no name. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="mysql")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile has no system. Make sure that an error is raised.
        profile = DatabaseProfile(None)
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The profile has an invalid system. Make sure that an error is raised.
        profile = DatabaseProfile(None, system="dummy")
        with self.assertRaises(GetDatabaseError) as context:
            DatabaseRegistry.get_database(profile=profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # The given profile is valid. Make sure that *no* exception is raised.
        profile = DatabaseProfile("DummyProfile", system="mysql")
        database = DatabaseRegistry.get_database(profile=profile)
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "DummyProfile")

    def test_get_database_with_profile_name_and_profile(self):
        """
        Tests the method get_database() with a profile name and a profile.
        """
        # ---------------------------------------------------------------------
        # Test the method when *no* databases and *no* profiles are registered.

        # The profile name is empty *and* the profile is valid. Make sure that
        # an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # The profile name is invalid *and* the profile is valid. Make sure
        # that an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="xxx",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The profile name *and* the profile is valid. Make sure that an error
        # is raised (because profile_name is preferred and there are no
        # registered databases).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="mysql",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # ---------------------------------------------------------------------
        # Test the method when databases but *no* profiles are registered.
        DatabaseRegistry.initialize()

        # The profile name is empty *and* the profile is valid. Make sure that
        # an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # The profile name is invalid *and* the profile is valid. Make sure
        # that an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="xxx",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The profile name and the profile is valid. Make sure that an error is
        # raised (because there are no profiles and profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="my-profile",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # ---------------------------------------------------------------------
        # Test the method when databases *and* a single profile is registered.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # The profile name is empty *and* the profile is valid. Make sure that
        # an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # The profile name is invalid *and* the profile is valid. Make sure
        # that an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="xxx",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The profile name and the profile is valid.
        database = DatabaseRegistry.get_database(
            profile_name="my-profile",
            profile=DatabaseProfile("DummyProfile", system="mysql")
        )
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "my-profile")

        # ---------------------------------------------------------------------
        # Test the method when databases *and* two profiles are registered.
        DatabaseRegistry.initialize(self.profiles_file_two_profiles)

        # The profile name is empty *and* the profile is valid. Make sure that
        # an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # The profile name is invalid *and* the profile is valid. Make sure
        # that an error is raised (because profile_name is preferred).
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_database(
                profile_name="xxx",
                profile=DatabaseProfile("DummyProfile", system="mysql")
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

        # The profile name *and* the profile is valid.
        database = DatabaseRegistry.get_database(
            profile_name="first-profile",
            profile=DatabaseProfile("DummyProfile", system="mysql")
        )
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.MYSQL)
        self.assertEqual(database.db_profile.name, "first-profile")

        # The profile name *and* the profile is valid.
        database = DatabaseRegistry.get_database(
            profile_name="second-profile",
            profile=DatabaseProfile("DummyProfile", system="mysql")
        )
        self.assertIsNotNone(database)
        self.assertIsNotNone(database.db_profile)
        self.assertEqual(database.system, DatabaseSystem.SQLITE)
        self.assertEqual(database.db_profile.name, "second-profile")

    # =========================================================================
    # Tests for method get_profile()

    def test_get_profile_with_no_profile_name(self):
        """
        Tests the method get_profile() with no/empty profile name.
        """
        # Get a profile with name None. Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_profile(None)
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # Get a profile with an empty name. Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_profile("")
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # Try to get a profile with a name that consists only of white spaces.
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_profile("   ")
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_get_profile_with_invalid_profile_name(self):
        """
        Tests the method get_profile() with an invalid profile_name.
        """
        # Try to get a profile with an invalid (unregistered) profile name.
        # Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_profile("dummy")
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_get_profile_with_valid_profile_name(self):
        """
        Tests the method get_profile() with a valid profile_name.
        """
        # Initialize the registry in order to have a registered profile.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # Get a profile with valid name.
        profile = DatabaseRegistry.get_profile("my-profile")

        # Make sure that the correct profile was returned.
        self.assertIsNotNone(profile)
        self.assertEqual(profile.name, "my-profile")

    # =========================================================================
    # Tests for method get_first_registered_profile()

    def test_get_first_registered_profile(self):
        """
        Tests the method get_first_registered_profile()
        """
        # Initialize the registry in order to have registered databases.
        DatabaseRegistry.initialize()

        # Get the first registered profile, given that there are no profiles.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_first_registered_profile()
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Register the first profile.
        p1 = DatabaseProfile("profile1", system="mysql")
        DatabaseRegistry.register_profile(p1)
        # Make sure that the first profile is returned.
        self.assertEqual(p1, DatabaseRegistry.get_first_registered_profile())

        # Register the second profile.
        p2 = DatabaseProfile("profile2", system="mysql")
        DatabaseRegistry.register_profile(p2)
        # Make sure that the first profile is returned.
        self.assertEqual(p1, DatabaseRegistry.get_first_registered_profile())

        # Register the third profile.
        p3 = DatabaseProfile("profile3", system="mysql")
        DatabaseRegistry.register_profile(p3)
        # Make sure that the first profile is returned.
        self.assertEqual(p1, DatabaseRegistry.get_first_registered_profile())

    # =========================================================================
    # Tests for method get_last_registered_profile()

    def test_get_last_registered_profile(self):
        """
        Tests the method get_first_registered_profile()
        """
        # Initialize the registry in order to have registered databases.
        DatabaseRegistry.initialize()

        # Try to get the last registered profile, given that there are no
        # registered profiles.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.get_last_registered_profile()
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Register the first profile.
        p1 = DatabaseProfile("profile1", system="mysql")
        DatabaseRegistry.register_profile(p1)
        # Make sure that the first profile is returned.
        self.assertEqual(p1, DatabaseRegistry.get_last_registered_profile())

        # Register the second profile.
        p2 = DatabaseProfile("profile2", system="mysql")
        DatabaseRegistry.register_profile(p2)
        # Make sure that the second profile is returned.
        self.assertEqual(p2, DatabaseRegistry.get_last_registered_profile())

        # Register the third profile.
        p3 = DatabaseProfile("profile3", system="mysql")
        DatabaseRegistry.register_profile(p3)
        # Make sure that the third profile is returned.
        self.assertEqual(p3, DatabaseRegistry.get_last_registered_profile())

    # =========================================================================
    # Tests for method validate_database()

    def test_validate_database_with_no_database(self):
        """
        Tests the method validate_database() *without* passing a database.
        """
        # Validate a "None" database.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_database(None)
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_validate_database_with_invalid_database(self):
        """
        Tests the method validate_database() with an object that is not a
        subclass of Database.
        """
        # Define a dummy database that is *not* a subclass of Database.
        class DummyDatabase:
            pass
        # Validate the database. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_database(DummyDatabase)
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_validate_database_with_database_of_invalid_system(self):
        """
        Tests the method validate_database() with an database of an invalid
        system.
        """
        # Define a dummy database with an invalid database system.
        class DummyDatabase(Database):
            system = "DummySystem"

        # Validate the database. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_database(DummyDatabase)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_validate_database_with_valid_database(self):
        """
        Tests the method validate_database() with an valid database.
        """
        # Define a dummy database with an valid database system.
        class DummyDatabase(Database):
            system = DatabaseSystem.MYSQL

        # Make sure that the validation succeeds.
        validated = DatabaseRegistry.validate_database(DummyDatabase)
        self.assertEqual(DummyDatabase, validated)

    # =========================================================================
    # Tests for method validate_profile()

    def test_validate_profile_with_no_profile(self):
        """
        Tests the method validate_profile() *without* passing a profile.
        """
        # Validate a "None" profile. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(None)
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_validate_profile_with_invalid_profile(self):
        """
        Tests the method validate_profile() with an object that is not an
        instance of DatabaseProfile.
        """
        # Validate an invalid profile. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(object())
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_validate_profile_with_no_name(self):
        """
        Tests the method validate_profile() with no/empty name.
        """
        # Validate a profile with no name.
        profile = DatabaseProfile(None)
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Validate a profile with an empty name.
        profile = DatabaseProfile("")
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

        # Validate a profile with a name that only consists of white spaces.
        profile = DatabaseProfile("     ")
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_validate_profile_with_no_db_system(self):
        """
        Tests the method validate_profile() with no database system.
        """
        # Validate a profile with no system.
        profile = DatabaseProfile("myprofile")
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 4.
        self.assertEqual(context.exception.code, 4)

        # Validate a profile with an empty system.
        profile = DatabaseProfile("myprofile", system="")
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 4.
        self.assertEqual(context.exception.code, 4)

        # Validate a profile with a system that consists only of white spaces.
        profile = DatabaseProfile("myprofile", system="    ")
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 4.
        self.assertEqual(context.exception.code, 4)

    def test_validate_profile_with_invalid_db_system(self):
        """
        Tests the method validate_profile() with an invalid database system.
        """
        # Validate a profile with an invalid system "dummy".
        # Make sure that an error is raised.
        profile = DatabaseProfile("myprofile", system="dummy")
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile(profile)
        # We expect the error code 5.
        self.assertEqual(context.exception.code, 5)

    def test_validate_profile_with_valid_profile_1(self):
        """
        Tests the method validate_profile() with an valid profile.
        """
        DatabaseRegistry.initialize()

        # Test the method three times, each time with the same system, but
        # different cases (to check if system validation is case-insensitive).

        # (1) Validate a profile with an valid system.
        profile = DatabaseProfile("myprofile", system="mysql")
        validated = DatabaseRegistry.validate_profile(profile)
        # Make sure that the validation succeeded.
        self.assertEqual(profile, validated)

        # (2) Define a profile with an valid system (with alternative cases).
        profile = DatabaseProfile("myprofile", system="MYSQL")
        validated = DatabaseRegistry.validate_profile(profile)
        # Make sure that the validation succeeded.
        self.assertEqual(profile, validated)

        # (3) Define a profile with an valid system (with alternative cases).
        profile = DatabaseProfile("myprofile", system="mYsQl")
        validated = DatabaseRegistry.validate_profile(profile)
        # Make sure that the validation succeeded.
        self.assertEqual(profile, validated)

    # =========================================================================
    # Tests for method validate_profile_name()

    def test_validate_profile_name_with_no_name(self):
        """
        Tests the method validate_profile_name() with no/empty name.
        """
        # Validate a "None" name. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile_name(None)
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # Validate an empty name. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile_name("")
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # Validate a name that only consists of white spaces.
        # Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile_name("    ")
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

        # Test another error to raise. Make sure that an error is raised.
        with self.assertRaises(GetProfileError) as context:
            DatabaseRegistry.validate_profile_name(
                None, error_to_raise=GetProfileError
            )
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_validate_profile_name_with_invalid_name(self):
        """
        Tests the method validate_profile_name() with an invalid profile name.
        """
        # Initialize the registry in order to have registered profiles.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # Validate an invalid profile name. Make sure that an error is raised.
        with self.assertRaises(DataMapperError) as context:
            DatabaseRegistry.validate_profile_name("dummy")
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_validate_profile_name_with_valid_name(self):
        """
        Tests the method validate_profile_name() with a valid profile name.
        """
        # Initialize the registry in order to have registered profiles.
        DatabaseRegistry.initialize(self.profiles_file_single_profile)

        # Make sure that the validation succeeded.
        validated = DatabaseRegistry.validate_profile_name("my-profile")
        self.assertEqual(validated, "my-profile")

    # =========================================================================
    # Tests for method read_profiles_from_file()

    def test_read_profiles_with_non_existing_file(self):
        """
        Tests the method read_profiles_from_file() with a non-existing file.
        """
        # Read from a non-existing file. Make sure that an error is raised.
        with self.assertRaises(ParseProfileConfigFileError) as context:
            DatabaseRegistry.read_profiles_from_file(
                self.profiles_file_not_existing
            )
        # We expect the error code 1.
        self.assertEqual(context.exception.code, 1)

    def test_read_db_profiles_with_non_readable_file(self):
        """
        Tests the method read_profiles_from_file() with a non-readable file.
        """
        # Read from a non-readable file. Make sure that an error is raised.
        with self.assertRaises(ParseProfileConfigFileError) as context:
            DatabaseRegistry.read_profiles_from_file(
                self.profiles_file_not_readable
            )
        # We expect the error code 2.
        self.assertEqual(context.exception.code, 2)

    def test_read_db_profiles_with_malformed_file(self):
        """
        Tests the method read_profiles_from_file() with a malformed file.
        """
        # Read from a malformed file. Make sure that an error is raised.
        with self.assertRaises(ParseProfileConfigFileError) as context:
            DatabaseRegistry.read_profiles_from_file(
                self.profiles_file_malformed
            )
        # We expect the error code 3.
        self.assertEqual(context.exception.code, 3)

    def test_read_db_profiles_with_single_profile(self):
        """
        Tests the method read_profiles_from_file() on a file with a single
        valid profile.
        """
        # Initialize the registry in order to have registered databases.
        DatabaseRegistry.initialize()

        # Read from a valid file with a single profile.
        db_profiles = DatabaseRegistry.read_profiles_from_file(
             self.profiles_file_single_profile
        )

        # Make sure that a proper instance of DatabaseProfile was returned.
        self.assertNotEqual(db_profiles, None)
        self.assertEqual(len(db_profiles), 1)

        profile = db_profiles[0]
        self.assertNotEqual(profile, None)
        self.assertEqual(profile.system, "mysql")
        self.assertEqual(profile.host, None)
        self.assertEqual(profile.port, None)
        self.assertEqual(profile.user, "Hans Dampf")
        self.assertEqual(profile.password, "test123")
        self.assertEqual(profile.db, "test")

    def test_read_db_profiles_with_two_profiles(self):
        """
        Tests the method read_profiles_from_file() with two valid profiles.
        """
        # Initialize the registry in order to have registered databases.
        DatabaseRegistry.initialize()

        # Read from a valid file with two profiles.
        db_profiles = DatabaseRegistry.read_profiles_from_file(
             self.profiles_file_two_profiles
        )

        # Make sure that two proper instances of DatabaseProfile were returned.
        self.assertNotEqual(db_profiles, None)
        self.assertEqual(len(db_profiles), 2)

        first_profile = db_profiles[0]
        self.assertNotEqual(first_profile, None)
        self.assertEqual(first_profile.system, "mysql")
        self.assertEqual(first_profile.host, None)
        self.assertEqual(first_profile.port, None)
        self.assertEqual(first_profile.user, "Hans Dampf")
        self.assertEqual(first_profile.password, "test123")
        self.assertEqual(first_profile.db, "test")

        second_profile = db_profiles[1]
        self.assertNotEqual(second_profile, None)
        self.assertEqual(second_profile.system, "sqlite")
        self.assertEqual(second_profile.host, "localhost")
        self.assertEqual(second_profile.port, "666")
        self.assertEqual(second_profile.user, "Hans Dampf")
        self.assertEqual(second_profile.password, None)
        self.assertEqual(second_profile.db, "test")
