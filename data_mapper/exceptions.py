class DataMapperError(Exception):
    """
    The base class of errors in the DataMapper.
    """
    prefix = None

    def __init__(self, code=-1, msg=None, args=None):
        """
        Creates a new DataMapperError.

        Args:
            code (int): The reason of this error, as an int.
            prefix (str): An prefix to prepend in fromt of the message.
            msg (str): The reason of this error, as a string.
            args (tuple of str): The arguments to plug into msg.
        """
        self.code = code
        message = ""
        if self.prefix is not None:
            message += self.prefix
        if msg is not None:
            message += msg
        if args is not None:
            message = message % args
        super().__init__(message)
