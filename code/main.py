from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister
from items import Item_List,Item

app = Flask(__name__)
app.secret_key = 'jlkjashkljalblka'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Item_List, "/items")
api.add_resource(UserRegister, "/register")

app.run(port=5000,debug=True) 