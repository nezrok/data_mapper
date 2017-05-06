class Model:
    # The database field specifications.
    db_fields = {}
    # The mapper for this model.
    mapper = None

    def __init__(self, **kwargs):
        """
        Creates a new base model.
        """
        self._name = self.__class__.__name__
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """
        Writes the values of fields defined by DB_FIELDS to database.
        """
        # Check, if the property "DB_FIELDS" is given.
        if not hasattr(self, 'DB_FIELDS'):
            raise ValueError("Model '%s' has no DB_FIELDS." % self._name)

        # TODO: Validate.

        # Process the DB_FIELDS one after another.
        for field_name, field_spec in self.DB_FIELDS.items():
            self.save_db_field(field_name, field_spec)

    def save_db_field(self, field_name, field_spec):
        """
        Writes the value of given DbField to database.
        """
        if field_name is None:
            return

        # Make sure that the name of the field is a string.
        field_name = str(field_name)
        if len(field_name) == 0:
            return

        # Make sure that the spec of the field is an instance of DbField.
        # if not isinstance(field_spec, db_fields.DbField):
        #    raise ValueError("Ignoring field '%s' in model '%s'." %
        # (field_name, self._name))

        # Fetch the model value for the given database field, or the default
        # value defined by the specification if no such value is set.
        getattr(self, field_name, field_spec.default_value)

    def get(self, max_num=None, **kwargs):
        # * Implement filters like name == "X" OR/AND name == "Y"
        pass

    def delete(self):
        pass
