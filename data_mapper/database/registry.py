import os
import sys
import configparser

from collections import OrderedDict

from data_mapper.exceptions import DataMapperError

from data_mapper.database.base import Database
from data_mapper.database.base import DatabaseProfile
from data_mapper.database.base import DatabaseSystem

from data_mapper.database.mysql import MySQLDatabase
from data_mapper.database.sqlite import SQLiteDatabase


class DatabaseRegistry:
    """
    A database registry to manage (1) various database instances with various
    database systems and (2) various database profiles.
    """
    # The registered databases, per system ("mysql", "sqlite", etc.).
    registered_databases = OrderedDict()
    # The registered database profiles, per profile name.
    registered_profiles = OrderedDict()
    # A boolean flag to indicate whether this registry is initialized.
    is_initialized = False

    @classmethod
    def clear(cls):
        """
        Clears the registered databases and the registered profiles.
        """
        cls.registered_databases.clear()
        cls.registered_profiles.clear()
        cls.is_initialized = False

    @classmethod
    def initialize(cls, profiles_file_path=None):
        """
        Initializes this database registry. Registers all known databases,
        reads the profiles from given path and registers the profiles to this
        registry.

        Args:
            profiles_file_path (str): The path to the file where the
                database profiles are defined.
        """
        # Clear this registry.
        cls.clear()
        # Register the known databases.
        cls.register_database(MySQLDatabase)
        cls.register_database(SQLiteDatabase)

        if profiles_file_path is not None:
            # Read the database profiles from the given path.
            profiles = cls.read_profiles_from_file(profiles_file_path)
            # Register the profiles.
            for profile in profiles:
                cls.register_profile(profile)

        # The registry is now initialized.
        cls.is_initialized = True

    # =========================================================================
    # Register methods.

    @classmethod
    def register_database(cls, database):
        """
        Validates the given database and, if validation succeeded, registers
        the database to this registry.

        Args:
            database (Database): The database to register.
        """
        # Validate the database.
        cls.validate_database(database, error_to_raise=RegisterDatabaseError)

        # Register the database, with the lowercased db system as key.
        db_system_str = database.system.value.lower()
        cls.registered_databases[db_system_str] = database

    @classmethod
    def register_profile(cls, profile):
        """
        Validates the given profile and, if validation succeeded, registers
        the profile to this registry.

        Args:
            profile (DatabaseProfile): The profile to register.
        """
        # Validate the profile.
        cls.validate_profile(profile, error_to_raise=RegisterProfileError)

        # Register the profile, with the name as key.
        cls.registered_profiles[profile.name] = profile

    # =========================================================================
    # Getter methods.

    @classmethod
    def get_database(cls, profile_name=None, profile=None):
        """
        Returns the database related to the given profile name or the given
        profile. If there is no profile given, the last profile in the profile
        config file is chosen.

        Args:
            profile_name (str, optional): The name of an registered profile.
            profile (DatabaseProfile, optional): The profile to use.
        Returns:
            The database related to the given profile.
        """
        if profile_name is not None:
            # Fetch the profile related to the given name.
            profile = cls.get_profile(profile_name)

        if profile is None:
            # Fetch the latest of the registered profiles.
            profile = cls.get_last_registered_profile()

        # Validate the profile.
        cls.validate_profile(profile, error_to_raise=GetDatabaseError)

        # Instantiate a database instance, related to the given profile.
        return cls.registered_databases[profile.system](profile)

    @classmethod
    def get_profile(cls, profile_name):
        """
        Returns the profile related to the given profile name. Raises a
        GetProfileError if there is no profile registered with the given name.

        Args:
            profile_name (str): The name of the profile.
        Returns:
            The profile related to the given name.
        """
        # Validate the profile name.
        cls.validate_profile_name(profile_name, error_to_raise=GetProfileError)
        # Return the related profile.
        return cls.registered_profiles.get(profile_name)

    @classmethod
    def get_first_registered_profile(cls):
        """
        Returns the first registered profile. Raises a GetProfileError if there
        is no such profile.

        Returns:
            The first registered profile.
        """
        if len(cls.registered_profiles) == 0:
            raise GetProfileError(
                code=3,
                msg="There are no registered profiles."
            )
        return list(cls.registered_profiles.values())[0]

    @classmethod
    def get_last_registered_profile(cls):
        """
        Returns the last registered profile. Raises a GetProfileError if there
        is no such profile.

        Returns:
            The last registered profile.
        """
        if len(cls.registered_profiles) == 0:
            raise GetProfileError(
                code=3,
                msg="There are no registered profiles."
            )
        return list(cls.registered_profiles.values())[-1]

    # =========================================================================
    # Validation methods.

    @classmethod
    def validate_database(cls, database, error_to_raise=DataMapperError):
        """
        Validates the given database. Raises the given error (or a generic
        DataMapperError if no error to raise is given) if the validation fails.
        Returns the database if the validation succeeds.

        Args:
            database (Database): The database to validate.
            error_to_raise (DataMapperError): The error to raise on a
                validation error.
        Returns:
            The validated database, if the validation succeeded.
        """
        # Check if there is a database given.
        if database is None:
            raise error_to_raise(
                code=1,
                msg="No database given."
            )
        # Check if the database is a subclass of Database.
        if not issubclass(database, Database):
            raise error_to_raise(
                code=2,
                msg="The given database '%s' is not a subclass of Database.",
                args=database
            )
        # Check if the system is an instance of DatabaseSystem.
        if not isinstance(database.system, DatabaseSystem):
            raise error_to_raise(
                code=3,
                msg="The system '%s' of database '%s' is not valid.",
                args=(database.system, database)
            )
        return database

    @classmethod
    def validate_profile(cls, profile, error_to_raise=DataMapperError):
        """
        Validates the given profile. Raises the given error (or a generic
        DataMapperError if no error to raise is given) if the validation fails.
        Returns the profile if the validation succeeds.

        Args:
            profile (DatabaseProfile): The database profile to validate.
            error_to_raise (DataMapperError): The error to raise on a
                validation error.
        Returns:
            The validated profile, if the validation succeeded.
        """
        # Check if there is a profile given.
        if profile is None:
            raise error_to_raise(
                code=1,
                msg="No profile given."
            )
        # Check if the profile is an instance of DatabaseProfile.
        if not isinstance(profile, DatabaseProfile):
            raise error_to_raise(
                code=2,
                msg="The profile '%s' is not an instance of DatabaseProfile.",
                args=profile
            )
        # Check if there is a name given.
        if profile.name is None or len(profile.name.strip()) == 0:
            raise error_to_raise(
                code=3,
                msg="There is no name given for the profile '%s'.",
                args=profile
            )
        # Check if there is a database system given.
        if profile.system is None or len(profile.system.strip()) == 0:
            raise error_to_raise(
                code=4,
                msg="The profile '%s' does not provide a database system.",
                args=profile.name
            )
        # Check, if there is a database registered for the given system.
        db_system = profile.system.lower().strip()
        if db_system not in cls.registered_databases:
            raise error_to_raise(
                code=5,
                msg="The db system '%s' in profile '%s' is not supported.",
                args=(profile.system, profile.name)
            )
        return profile

    @classmethod
    def validate_profile_name(cls, name, error_to_raise=DataMapperError):
        """
        Validates the given profile name. Raises the given error (or a generic
        DataMapperError if no error to raise is given) if the validation fails.
        Returns the profile name if the validation succeeds.

        Args:
            name (str): The profile name to validate.
            error_to_raise (DataMapperError): The error to raise on a
                validation error.
        Returns:
            The validated profile name, if the validation succeeded.
        """
        # Check if there is a profile name given.
        if name is None or len(name.strip()) == 0:
            raise error_to_raise(
                code=1,
                msg="No profile name given."
            )
        # Check if there is a registered profile with the given name.
        if name not in cls.registered_profiles:
            raise error_to_raise(
                code=2,
                msg="There is no registered profile for the name '%s'.",
                args=name
            )
        return name

    # =========================================================================
    # Utility methods.

    @classmethod
    def read_profiles_from_file(cls, path):
        """
        Reads the database profiles from given file path.

        Args:
            path (str): The path to the file to read from.
        Returns:
            dict of str:DatabaseProfile. A dictionary that maps profile names
                to the related DatabaseProfile objects.
        """
        # Check if the given path exists.
        if not os.access(path, os.F_OK):
            raise ParseProfileConfigFileError(
                code=1,
                msg="The profile config file '%s' does not exist.",
                args=path,
            )
        # Check if the given path can be read.
        if not os.access(path, os.R_OK):
            raise ParseProfileConfigFileError(
                code=2,
                msg="The profile config file '%s' can not be read.",
                args=path
            )
        # Read the profile file using a config parser.
        try:
            profile_file = configparser.ConfigParser()
            profile_file.read(path)
        except:
            raise ParseProfileConfigFileError(
                code=3,
                msg=str(sys.exc_info()[0])  # TODO: Get a meaningful message.
            )

        # Read the profile names of database profiles.
        db_profile_names = profile_file.sections()
        # No need to check if profile_names is empty here, because
        # the method config_parser.read() ensures that there is at least one
        # section.

        # Read the individual database profile sections.
        db_profiles = []
        for db_profile_name in db_profile_names:
            # Get the section in profile file that represents a single profile.
            db_profile_section = profile_file[db_profile_name]

            # Create the related DatabaseProfile object.
            db_profile = DatabaseProfile(db_profile_name)
            db_profile.system = db_profile_section.get("system")
            db_profile.host = db_profile_section.get("host")
            db_profile.port = db_profile_section.get("port")
            db_profile.user = db_profile_section.get("user")
            db_profile.password = db_profile_section.get("password")
            db_profile.db = db_profile_section.get("db")

            # Add the profile to the index.
            db_profiles.append(db_profile)

        return db_profiles

# =============================================================================
# Errors.


class RegisterDatabaseError(DataMapperError):
    """
    An error to raise on any errors related to registering a database.
    """
    prefix = "An error occurred on registering a database: "


class RegisterProfileError(DataMapperError):
    """
    An error to raise on any errors related to registering a profile.
    """
    prefix = "An error occurred on registering a profile: "


class GetDatabaseError(DataMapperError):
    """
    An error to raise on any errors related to getting a database.
    """
    prefix = "An error occurred on getting a database: "


class GetProfileError(DataMapperError):
    """
    An error to raise on any errors related to getting a profile.
    """
    prefix = "An error occurred on getting a profile: "


class ParseProfileConfigFileError(DataMapperError):
    """
    An error to raise on any errors related to parsing a profile config file.
    """
    prefix = "An error occurred on parsing a profile config file: "
