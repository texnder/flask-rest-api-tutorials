from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from blacklist import BLACKLIST
# use brackets while import is long
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token
)

# private convension starts from underscore..
_parse_user_data = reqparse.RequestParser()
_parse_user_data.add_argument("username", 
    type=str, 
    required=True, 
    help="field cannot be empty"
)

_parse_user_data.add_argument("password", 
    type=str, 
    required=True, 
    help="field cannot be empty"
)


class UserRegister(Resource):
    def post(self):
        data = _parse_user_data.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "'{}' already exists".format(data['username'])}, 400
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201


class User(Resource):
    # class method is more useful than the static method
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found!!"}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found!!"}, 404
        user.delete_from_db()
        return {"message": "user deleted!!"}, 200


class UserLogin(Resource):
    def post(self):
        data = _parse_user_data.parse_args()
        user = UserModel.find_by_username(data["username"])
        # similar to authfunction  we created in security..
        if user and safe_str_cmp(user.password, data["password"]):
            # similar to identity in security..
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "invalid credentials!!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        # jti unique identifier for JWT 
        # it is better than sending JWT token in header.. with extended we need Bearer fresh_token
        jti = get_raw_jwt()["jti"] 
        user_id = get_jwt_identity()
        # to logout blacklist the token..
        # but not sure if after destroing session blacklist data will be saved or not..
        BLACKLIST.add(jti)
        return {"message": "User id ='{}' successfully logged out.".format(user_id)}, 200


class TokenRefresh(Resource):
    # refresh token when user comes after token expires..
    # do we use cookie or not?
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)
        return {"access_token": new_token}, 200
