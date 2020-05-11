import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = users

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        # we always pass tuple in executing query that's why (username,)
        result = cursor.execute(query, (username,))
        # taking the first row out of filtered rows
        row = result.fetchone()
        if row:
            row = cls(*row) # passing row as args which will act as (row[0], row[1], row[2])
        else:
            row = None

        connection.close()
        return row

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        # we always pass tuple in executing query that's why (_id,)
        result = cursor.execute(query, (_id,))
        # taking the first row out of filtered rows
        row = result.fetchone()
        if row:
            row = cls(*row) # passing row as args which will act as (row[0], row[1], row[2])
        else:
            row = None

        connection.close()
        return row
