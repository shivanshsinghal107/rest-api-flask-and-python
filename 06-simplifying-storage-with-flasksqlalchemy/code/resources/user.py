import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

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

        # step for ensuring that no two users have same username
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exists. Choose another."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User successfully created."}, 201
