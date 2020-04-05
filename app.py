from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from code.security import authenticate,identity
from code.resources.user import UserRegister
from code.resources.item import Item, ItemList
from code.resources.store import Store, StoreList
from code.db import db

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='maciek'
jwt=JWT(app,authenticate,identity)

api.add_resource(Item,'/Item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__=="__main__":
    db.init_app(app)
    app.run(debug=True)