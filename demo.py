from orm import Model, IntegerField, StringField

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(nullable=False)
    email = StringField()

def main():
   
    with User.connect() as conn, conn.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS "user";')
        conn.commit()

    User.create_table()
    print("Table created successfully")

    new_user = User.create(id=1, name="Fadwa", email="Fadwa@gmail.com")
    print("Created:", dict(new_user))

    user = User.get(new_user['id'])
    print("Retrieved:", dict(user))

    updated_user = User.update(new_user['id'], name="Fadwa Updated", email="Fadwa2@gmail.com")
    print("Updated:", dict(updated_user))

    deleted_user = User.delete(new_user['id'])
    print("Deleted user with ID:", deleted_user['id'])

if __name__ == "__main__":
    main()
