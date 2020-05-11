import sqlite3
from flask_restful import Resource, reqparse

class User:
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

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "The field 'username' is empty or is not of string type."
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field 'password' is empty or is not of string type."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User successfully created."}, 201
