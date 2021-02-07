from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required= True, 
        help= 'this field cannot be left blank!'
    )

    parser.add_argument("store_id", 
        type=int, 
        required=True, 
        help="must have store_id"
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "item not found"}, 404
    
    # authentication require with fresh token
    @fresh_jwt_required
    def post(self, name):

        if ItemModel.find_by_name(name):
            return {"message": "item name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        # used kwargs.. to make it look nice
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting item"}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}, 200
        return {"message": "Item not found."}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}, 200
