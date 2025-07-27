import psycopg2
from psycopg2.extras import RealDictCursor

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

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)
        fields = {k: v for k, v in attrs.items() if isinstance(v, (IntegerField, StringField))}
        attrs['__fields__'] = fields
        attrs['__table__'] = name.lower()
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    @classmethod
    def connect(cls):
        return psycopg2.connect(
            dbname='orm_demo',
            user='postgres',
            password='Fadwa@2511',
            host='localhost',
            port='5432',
            cursor_factory=RealDictCursor
        )

    @classmethod
    def create_table(cls):
        columns = []
        for name, field in cls.__fields__.items():
            if isinstance(field, IntegerField) and field.primary_key:
                col = f'"{name}" SERIAL PRIMARY KEY'
            else:
                col = f'"{name}" {field.column_type}'
                if field.primary_key:
                    col += ' PRIMARY KEY'
                if not field.nullable:
                    col += ' NOT NULL'
            columns.append(col)
        sql = f'CREATE TABLE IF NOT EXISTS "{cls.__table__}" ({", ".join(columns)});'
        with cls.connect() as conn, conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()

    @classmethod
    def create(cls, **kwargs):
        fields = cls.__fields__
        insert_kwargs = {
            k: v for k, v in kwargs.items()
            if not (fields[k].primary_key and fields[k].column_type == 'SERIAL')
        }
        if not insert_kwargs:
            raise ValueError("No valid fields to insert.")
        keys = ', '.join(f'"{k}"' for k in insert_kwargs)
        placeholders = ', '.join(['%s'] * len(insert_kwargs))
        values = list(insert_kwargs.values())
        sql = f'INSERT INTO "{cls.__table__}" ({keys}) VALUES ({placeholders}) RETURNING *;'
        with cls.connect() as conn, conn.cursor() as cur:
            cur.execute(sql, values)
            result = cur.fetchone()
            conn.commit()
            return result

    @classmethod
    def get(cls, id):
        pk = next(k for k, v in cls.__fields__.items() if v.primary_key)
        sql = f'SELECT * FROM "{cls.__table__}" WHERE "{pk}" = %s;'
        with cls.connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (id,))
            return cur.fetchone()

    @classmethod
    def update(cls, id, **kwargs):
        pk = next(k for k, v in cls.__fields__.items() if v.primary_key)
        updates = ', '.join(f'"{k}" = %s' for k in kwargs)
        sql = f'UPDATE "{cls.__table__}" SET {updates} WHERE "{pk}" = %s RETURNING *;'
        with cls.connect() as conn, conn.cursor() as cur:
            cur.execute(sql, list(kwargs.values()) + [id])
            result = cur.fetchone()
            conn.commit()
            return result

    @classmethod
    def delete(cls, id):
        pk = next(k for k, v in cls.__fields__.items() if v.primary_key)
        sql = f'DELETE FROM "{cls.__table__}" WHERE "{pk}" = %s RETURNING *;'
        with cls.connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (id,))
            result = cur.fetchone()
            conn.commit()
            return result
