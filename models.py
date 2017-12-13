from app import db


class Risk(db.Model):
    """docstring for Property"""

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    user = db.Column(db.String)


    def __init__(self, type, user):
        self.type = type
        self.user = user


import sqlite3

def drop_table():
    with sqlite3.connect('risks.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS risk_types;""")
        c.execute("""DROP TABLE IF EXISTS risk_fields;""")
    return True


def create_db():
    with sqlite3.connect('risks.db') as connection:
        c = connection.cursor()
        types = """CREATE TABLE risk_types(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            user TEXT DEFAULT 'anonymous'
        );"""
        fields = """CREATE TABLE risk_fields(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            risk_type TEXT NOT NULL,
            data_type TEXT NOT NULL
        );"""
        c.execute(types)
        c.execute(fields)
    return True

if __name__ == '__main__':
    drop_table()
    create_db()
