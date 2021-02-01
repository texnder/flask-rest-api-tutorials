from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required= True, 
        help= 'this field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('mydata.db')
        curser = connection.cursor()
        
        select_query = "SELECT * FROM items WHERE name = ?"
        result = curser.execute(select_query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'items': row}, 201 if item else 404
        return {'message': 'item not found'}, 400

    def post(self,name):
        if next(filter(lambda x : x['name'] == name, items), None):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()
        
        connection = sqlite3.connect('mydata.db')
        curser = connection.cursor()
        
        insert_query = "INSERT INTO items VALUES (?,?)"
        curser.execute(insert_query,(data['name'],data['price'])))
        connection.commit()
        connection.close()
        return {'message': 'item created successfully!'}, 201 



class Item_List(Resource):
    def get(self):
        connection = sqlite3.connect('mydata.db')
        curser = connection.cursor()
        
        select_query = "SELECT * FROM items"
        result = curser.execute(select_query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'items':{
                'name': row[0], 'price' : row[1]
            }}, 201 if item else 404
        return {'message': 'item not found'}, 400
