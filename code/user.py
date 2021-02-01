import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('mydata.db')
        curser = connection.cursor()
        
        select_query = "SELECT * FROM users WHERE username = ?"
        result = curser.execute(select_query, (username,))
        row = result.fetchone()
        print(row)
        if row:
            # user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_userId(cls, _id):
        connection = sqlite3.connect('mydata.db')
        curser = connection.cursor()
        
        select_query = "SELECT * FROM users WHERE id = ?"
        result = curser.execute(select_query, (_id,))
        row = result.fetchone()

        if row:
            # user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type= str, 
        required= True, 
        help= 'this field cannot be blank'
    )

    parser = reqparse.RequestParser()
    parser.add_argument('password', 
        type= str, 
        required= True, 
        help= 'this field cannot be blank'
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'A user with the username: "{}" is already exist'.format(data['username'])}

        connection = sqlite3.connect('mydata.db')
        curser = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?,? )"
        curser.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'user created successfully!'}, 201 