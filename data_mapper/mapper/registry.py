from collections import OrderedDict

from data_mapper.database.registry import DatabaseRegistry
from data_mapper.database.fields import DatabaseField

from data_mapper.mapper.base import Mapper

from data_mapper.exceptions import DataMapperError

from data_mapper.model import Model


class MapperRegistry:
    """
    A mapper registry to manage mappers of models.
    """
    # The registered mappers, per model.
    registered_mappers = OrderedDict()
    # A boolean flag to indicate whether this registry is initialized.
    is_initialized = False

    @classmethod
    def clear(cls):
        """
        Clears the registered mappers.
        """
        cls.registered_mappers.clear()
        cls.is_initialized = False

    @classmethod
    def initialize(cls):
        """
        Initializes this mapper registry.
        """
        # Clear this registry.
        cls.clear()
        # The registry is now initialized.
        cls.is_initialized = True

    # =========================================================================
    # Register methods.

    @classmethod
    def register(cls, db_profile=None, db_profile_name=None, db_fields=None):
        """
        Returns a decorator that instantiates and registers a mapper for the
        given model.

        Args:
            db_profile (DatabaseProfile, optional): The database profile to use
                for the given model.
            db_profile_name (str): The database profile name to use for the
                given model.
            db_fields (dict of str:DatabaseField): The database fields for the
                given model.
        Returns:
            A decorator, that registers a mapper for the given model.
        """
        def decorator(model):
            # Validate the model.
            cls.validate_model(model, error_to_raise=RegisterMapperError)
            # Validate the database fields.
            cls.validate_fields(db_fields, error_to_raise=RegisterMapperError)

            # Request a database from the DatabaseRegistry.
            database = DatabaseRegistry.get_database(
                profile=db_profile,
                profile_name=db_profile_name
            )

            # Create a mapper from the given database and register it.
            cls.registered_mappers[model] = Mapper(database, db_fields)
            return model
        return decorator

    # =========================================================================
    # Getter methods.

    @classmethod
    def get_mapper(cls, model):
        """
        Returns the registered mapper for the given model. If there is no
        registered mapper for the given model, a GetMapperError is raised.

        Args:
            model (Model): The model to process.
        Returns:
            The registered mapper for the given model
        """
        # Validate the model.
        cls.validate_model(model, error_to_raise=GetMapperError)

        # TODO: Move this validation into a validation method. But moving it
        # into validate_model() doesn't work, because this method is also
        # called before registering a mapper for a model.
        if model not in cls.registered_mappers:
            raise GetMapperError(
                code=4,
                msg="There is no registered mapper for the model '%s'.",
                args=model
            )
        else:
            return cls.registered_mappers[model]

    # =========================================================================
    # Validate methods.

    @classmethod
    def validate_model(cls, model, error_to_raise=DataMapperError):
        """
        Validates the given model. Raises the given error (or a generic
        DataMapperError if no error to raise is given) if the validation fails.
        Returns the model if the validation succeeds.

        Args:
            model (Model): The model to validate.
            error_to_raise (DataMapperError): The error to raise on a
                validation error.
        Returns:
            The validated model, if the validation succeeded.
        """
        # Check if a model is given.
        if model is None:
            raise error_to_raise(
                code=1,
                msg="No model given."
            )
        # Check if the model is a class.
        if not isinstance(model, type):
            raise error_to_raise(
                code=2,
                msg="The given model '%s' is not a class.",
                args=model
            )
        # Check if the given model is an instance of Model.
        if not issubclass(model, Model):
            raise error_to_raise(
                code=3,
                msg="The given model '%s' is not a subclass of Model.",
                args=model
            )
        return model

    @classmethod
    def validate_fields(cls, db_fields, error_to_raise=DataMapperError):
        """
        Validates the given database fields. Raises the given error (or a
        generic DataMapperError if no error to raise is given) if the
        validation fails. Returns the validated database fields if the
        validation succeeds.

        Args:
            db_fields (dict of str:DatabaseField): The database fields to
                validate.
            error_to_raise (DataMapperError): The error to raise on a
                validation error.
        Returns:
            The validated database fields, if the validation succeeded.
        """
        # Check if database fields are given.
        if db_fields is None:
            raise error_to_raise(
                code=3,
                msg="No database fields given."
            )
        # Check if the database fields are given as a dictionary.
        if not isinstance(db_fields, dict):
            raise error_to_raise(
                code=4,
                msg="The database fields must be given as a dictionary."
            )
        # Check if the dict contains at least one database field.
        if len(db_fields) == 0:
            raise error_to_raise(
                code=5,
                msg="No database fields given."
            )
        # Validate each single entry in the given database fields.
        for field_name, field in db_fields.items():
            # Check if the field name is a string.
            if not isinstance(field_name, str):
                raise error_to_raise(
                    code=6,
                    msg="The database field name '%s' must be a string.",
                    args=field_name
                )
            # Check if the field name is empty.
            if len(field_name.strip()) == 0:
                raise error_to_raise(
                    code=7,
                    msg="The database field name '%s' must not be empty.",
                    args=field_name
                )
            # Check if the field is an instance of DatabaseField.
            if not isinstance(field, DatabaseField):
                raise error_to_raise(
                    code=8,
                    msg="The field '%s' is not an instance of DatabaseField.",
                    args=field_name
                )
        return db_fields

# =============================================================================
# Errors.


class RegisterMapperError(DataMapperError):
    """
    An error to raise on any errors related to registering a mapper.
    """
    prefix = "An error occurred on registering a mapper: "


class GetMapperError(DataMapperError):
    """
    An error to raise on any errors related to getting a mapper.
    """
    prefix = "An error occurred on getting a mapper: "
