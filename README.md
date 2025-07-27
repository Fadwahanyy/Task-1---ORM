# Task1 _ORM

Build a Simple ORM in Python with PostgreSQL

Objective
To create a l Python ORM engine that supports:
- Table creation from Python class models
- Basic field types (`IntegerField`, `StringField`)
- Constraints (`primary_key`, `nullable`)
- Safe CRUD operations (Create, Read, Update, Delete)

  
Tech Stack
- Python 3.10+
- PostgreSQL
- psycopg2 (psycopg2-binary)

  
Project Structure
orm_project/
orm.py        # Core ORM logic
demo.py       # Script demonstrating ORM usage
README.md     # Project documentation


 Setup Instructions
1. Clone the Repository
```bash
git clone https://github.com/yourusername/orm_project.git
cd orm_project
```
2. Install Required Python Package
```bash
pip install psycopg2-binary
```
3. Set Up PostgreSQL
- Create a database named `orm_demo`:
```sql
CREATE DATABASE orm_demo;
```
- Update DB credentials in `orm.py` (inside `connect()` method):
```python
psycopg2.connect(
    dbname='orm_demo',
    user='postgres',
    password='YOUR_PASSWORD',
    host='localhost',
    port='5432'
)
```
 How to Run
Run the script from terminal:
```bash
python demo.py
```
What it does:
- Creates a `User` table if not exists
- Inserts a new user
- Retrieves the user by ID
- Updates the user's information
- Deletes the user
 Example Model Definition
```python
from orm import Model, IntegerField, StringField

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(nullable=False)
    email = StringField()
```
 Available ORM Methods
- Model.create_table(): Create SQL table for the model
- Model.create(**kwargs): Insert a new record
- Model.get(id): Fetch a record by ID
- Model.update(id, **kwargs): Update record fields
- Model.delete(id): Delete a record by ID
 Learning Goals
 Learn how ORMs work under the hood
 Understand metaclass usage in Python
 Perform safe DB operations using psycopg2
 Gain SQL + Python integration skills
Deliverables
- orm.py: ORM engine
- demo.py: Demonstration script
- README.md: Documentation and setup instructions

