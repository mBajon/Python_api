from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from code.resources.user import (
    UserRegister, 
    User, 
    UserLogin,
    UserLogout,
    TokenRefresh
)
from code.resources.item import Item, ItemList
from code.resources.store import Store, StoreList
from code.db import db
from code.blacklist import BLACKLIST

app=Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
app.secret_key='maciek'

jwt=JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"isAdmin":True}
    return {"isAdmin":False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "message":"token has expired",
        "error":"token_expired"
    }),401

@jwt.invalid_token_loader
def invalid_token_callback():
        return jsonify({
        "message":"token is invalid",
        "error":"invalid_token"
    }),401

@jwt.unauthorized_loader
def missing_token_callback():
        return jsonify({
        "message":"Request does not contain an access token",
        "error":"authorization_required"
    }),401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
        return jsonify({
        "message":"The token is not fresh",
        "error":"fresh_token_required"
    }),401

@jwt.revoked_token_loader
def revoked_token_callback():
        return jsonify({
        "message":"The token has been revoked",
        "error":"token_revoked"
    }),401

@jwt.token_in_blacklist_loader
def check_if_blacklisted(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(Item,'/Item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/User/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogin, '/logout')
api.add_resource(TokenRefresh, '/refresh')
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__=="__main__":
    db.init_app(app)
    app.run(debug=True)