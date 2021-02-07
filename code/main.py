from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager # give the extra flexibility to make secure authentication
from db import db # flask sqlAlchemy instance..
from blacklist import BLACKLIST #custom set of blacklist..

# RestFull resources..
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydata.db"

# flask alchamey track modification turns off
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

# enable blacklist logout and blocking users.. 
app.config["JWT_BLACKLIST_ENABLED"] = True 

# logout can be done by black listing access token and refresh token
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access","refresh"]  

app.secret_key = "random-os-key -generator" 

# define flask restful api
# restful makes it easy to define routes.. and add some security feactures
api = Api(app)

# create tables in database if not exist before..
@app.before_first_request
def create_tables():
    db.create_all()


# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app) # more flexibility 


# this method will check if a token is blacklisted, here jwt internal decorator invoked
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # jti is internal jwt decryted token dictionary.. 
    # we dont need to set it to identity anymore in jwt extended 
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

# app.run(port=5000,debug=True) 
if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
