from flask_restful import Resource, reqparse
from code.models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    def get(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message":"store not found"},404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'An store with name: {} already exists'.format(name)},400
            
        request_data=Store.parser.parse_args()
        store=StoreModel(name, request_data["price"], request_data["store_id"])

        try:
            store.save_to_db()
        except Exception:
            return {'message':'can not insert store'},500
        
        return store.json(), 201

    def delete(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message":"item: {} deleted".format(name)}
        
class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.find_all()]}