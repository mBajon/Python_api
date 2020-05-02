import sqlite3
from flask_restful import Resource,reqparse
from code.models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt
    )
from code.blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be left blank'
        )
_user_parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be left blank'
        )

class UserRegister(Resource):

    def post(self):
        request_data=_user_parser.parse_args()
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


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data=_user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.id, fresh=True) 
            refresh_token=create_refresh_token(user.id)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            },200

        return {"message":"Invalid credentials"},401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti=get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"User logged out successfully"},200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token= create_refresh_token(current_user,fresh=False)
        return {'access token':new_token },200