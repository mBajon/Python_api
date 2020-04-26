import sqlite3
from flask_restful import Resource,reqparse
from code.models.user import UserModel 

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be left blank'
        )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be left blank'
        )


    def post(self):
        request_data=UserRegister.parser.parse_args()
        if UserModel.find_by_username(request_data['username']): 
            return {'message':'user with that username has been already registered'}, 400

        user=UserModel(**request_data)
        user.save_to_db()
        return {'message':'user has been successfully registered'}, 201
        
class User(Resource):
    @classmethod
    def get(cls, user_id):
        user=UserModel.find_by_id(user_id)
        if not user:
            return {"message":"User not found"},404 
        return user.json(),200

    @classmethod
    def delete(cls, user_id):
        user=UserModel.find_by_id(user_id)
        if not user:
            return {"message":"User not found"},404
        user.delete_from_db()
        return {"message":"User deleted"},200