# TODO: Implement logic to validate, save, edit, delete, get from database.
# TODO: Unique ids.
# TODO: Thread-safe?


class Mapper:
    def __init__(self, database, model, database_fields):
        self.database = database
        self.model = model
        self.database_fields = database_fields

    def create_db_table(self):
        self.database.create_table(self.model, self.database_fields)
