class DatabaseField:
    """
    The base class for all database fields.
    """
    def __init__(self):
        """
        Creating instances of DatabaseField is not allowed
        """
        raise TypeError("Creating instances of DatabaseField is not allowed.")

# =============================================================================
# Strings.


class DatabaseStringField(DatabaseField):
    """
    A database field definition for a field that stores a string object.
    """
    def __init__(self, name, default_value=None, mandatory=False,
                 choices=None, min_length=None, max_length=None):
        """
        Creates a database field definition to store a string object.

        Args:
            name (str): The name of the field.
            default_value (str, optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
            choices (list, optional): The allowed values for the string.
            min_length (int, optional): The minimal length of the string.
            max_length (int, optional): The maximal length of the string.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory
        self.choices = choices
        self.min_length = min_length
        self.max_length = max_length

# =============================================================================
# Boolean.


class DatabaseBooleanField(DatabaseField):
    """
    A database field definition for a field that stores a boolean value.
    """
    def __init__(self, name=None, default_value=None, mandatory=False):
        """
        Creates a database field definition to store a boolean value.

        Args:
            name (str): The name of the field.
            default_value (bool, optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory

# =============================================================================
# Numeric values.


class DatabaseIntField(DatabaseField):
    """
    A database field definition for a field that stores an int value.
    """
    def __init__(self, name=None, default_value=None, mandatory=False,
                 unsigned=False, choices=None, min_value=None, max_value=None,
                 width=None):
        """
        Creates a database field definition to store an int value.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
            unsigned (bool, optional): A boolean flag that indicates whether
                the number is unsigned.
            choices (list, optional): The allowed values for this field.
            min_value (int, optional): The minimal value for this field.
            max_value (int, optional): The maximal value for this field.
            width (int, optional): The number of digits. Values with
                less than <width>-many digits will be 0-padded.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory
        self.unsigned = unsigned
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.width = width


class DatabaseFloatField(DatabaseField):
    """
    A database field definition for a field that stores a float value.
    """
    def __init__(self, name=None, default_value=None, mandatory=False,
                 unsigned=False, choices=False, min_value=None, max_value=None,
                 precision=None):
        """
        Creates a database field definition to store a float value.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
            unsigned (bool, optional): A boolean flag that indicates whether
                the number is unsigned.
            choices (list, optional): The allowed values for this field.
            min_value (int, optional): The minimal value for this field.
            max_value (int, optional): The maximal value for this field.
            precision (int, optional): The precision of this float.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory
        self.unsigned = unsigned
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.precision = precision


class DatabaseDoubleField(DatabaseField):
    """
    A database field definition for a field that stores a double value.
    """
    def __init__(self, name=None, default_value=None, mandatory=False,
                 unsigned=False, choices=None, min_value=None, max_value=None,
                 precision=None):
        """
        Creates a database field definition to store a double value.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
            unsigned (bool, optional): A boolean flag that indicates whether
                the number is unsigned.
            choices (list, optional): The allowed values for this field.
            min_value (int, optional): The minimal value for this field.
            max_value (int, optional): The maximal value for this field.
            precision (int, optional): The precision of this double.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory
        self.unsigned = unsigned
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.precision = precision

# =============================================================================
# Collections.


class DatabaseListField(DatabaseField):
    """
    A database field definition for a field that stores a list.
    """
    def __init__(self, name=None, default_value=None, mandatory=False,
                 choices=None, min_elements=None, max_elements=None):
        """
        Creates a database field definition to store a list.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
            choices (list, optional): The allowed values for this field.
            min_elements (int, optional): The minimal number of elements.
            max_elements (int, optional): The maximal number of elements.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory
        self.choices = choices
        self.min_elements = min_elements
        self.max_elements = max_elements

# =============================================================================
# Binary data.


class DatabaseBinaryField(DatabaseField):
    """
    A database field definition for a field that stores binary data.
    """
    def __init__(self, name=None, default_value=None, mandatory=False):
        """
        Creates a database field definition to store binary data.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory


# =============================================================================
# Date & Time.


class DatabaseTimeField(DatabaseField):
    """
    A database field definition for a field that stores a time object.
    """
    def __init__(self, name=None, default_value=None, mandatory=False):
        """
        Creates a database field to store a time object.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory


class DatabaseDateTimeField(DatabaseField):
    """
    A database field definition for a field that stores a datetime object.
    """
    def __init__(self, name=None, default_value=None, mandatory=False):
        """
        Creates a database field to store a datetime object.

        Args:
            name (str): The name of the field.
            default_value (optional): The default value.
            mandatory (bool, optional): A boolean flag that indicates whether
                the field is mandatory.
        """
        self.name = name
        self.default_value = default_value
        self.mandatory = mandatory
