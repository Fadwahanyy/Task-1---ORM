

class IntegerField:
    def __init__(self, primary_key=False, nullable=True):
        self.primary_key = primary_key
        self.nullable = nullable
        self.column_type = 'SERIAL' if primary_key else 'INTEGER'

class StringField:
    def __init__(self, length=255, primary_key=False, nullable=True):
        self.column_type = f'VARCHAR({length})'
        self.primary_key = primary_key
        self.nullable = nullable


