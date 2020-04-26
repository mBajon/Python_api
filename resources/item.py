from flask_jwt import JWT, jwt_required
from flask_restful import Resource, reqparse
import sqlite3
from flask import jsonify
from code.models.item import ItemModel
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank'
        )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store id'
        )

    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)

        if item:
            return item.json()
        else:
            return {"message":"item not found"},404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name: {} already exists'.format(name)},400
            
        request_data=Item.parser.parse_args()
        item=ItemModel(name, request_data["price"], request_data["store_id"])

        try:
            item.save_to_db()
        except Exception:
            return {'message':'can not insert item'},500
        
        return item.json(), 201

    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message":"item: {} deleted".format(name)}

    def put(self,name):
        request_data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, request_data["price"], request_data["store_id"])
        else:
            item.price=request_data["price"]

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.find_all()]}
