class DatabaseField:
    """
    A class to specify any field (column) in a database table.
    """
    def __init__(self, type=None, default_value=None):
        """
        Creates a new specification of any database field (column).

        Args:
            type: The type of the field.
            default_value: The default value to use if no values is given for
                this field.
        """
        self.type = type
        self.default_value = default_value


class DatabaseStringField(DatabaseField):
    """
    A class to specify a string field (column) in a database table.
    """
    def __init__(self, default_value=None):
        """
        Creates a new specification of a field (column) of type 'str'.

        Args:
            default_value: The default value to use if no values is given for
                this field.
        """
        super().__init__(type=str, default_value=default_value)


class DatabaseIntField(DatabaseField):
    """
    A class to specify an int field (column) in a database table.
    """
    def __init__(self, default_value=None):
        """
        Creates a new specification of a field (column) of type "int".

        Args:
            default_value: The default value to use if no values is given for
                this field.
        """
        super().__init__(type=int, default_value=default_value)
