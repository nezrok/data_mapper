# TODO: Implement logic to validate, save, edit, delete, get from database.
# TODO: Unique ids.
# TODO: Thread-safe?


class Mapper:
    def __init__(self, database, database_fields):
        self.database = database
        self.database_fields = database_fields
