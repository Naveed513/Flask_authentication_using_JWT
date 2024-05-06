import hashlib
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from schemas import UserSchema, UserQuerySchema, SuccessMessageSchema
from db.user import UserDatabase
from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/login")
class UserLogin(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UserSchema)
    def post(self, request_data):
        username = request_data['username']
        password = hashlib.sha256(request_data['password'].encode('utf-8')).hexdigest()
        user_id = self.db.verify_user(username=username, password=password)
        if user_id:
            return {
                "access_token":create_access_token(identity=user_id)
            }
        abort(400, message="Username or password is incorrect.")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}

@blp.route('/user')
class Users(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    @blp.response(200, UserSchema)
    @blp.arguments(UserQuerySchema, location='query')
    def get(self, args):
        user_id = args.get('id')
        result = self.db.get_user(user_id=user_id)
        if result:
            return result
        abort(404, message="User doesn't exist.")

    @blp.arguments(UserSchema)
    @blp.response(201, SuccessMessageSchema)
    def post(self, request_data):
        if self.db.add_user(username=request_data['username'],
                         password=hashlib.sha256(
                             request_data['password'].encode('utf-8')).hexdigest()
                             ):
            return {'message':'User added successfully'}, 201
        abort(403, message="User already exists.")

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location='query')
    def delete(self, args):
        user_id = args.get('id')
        if self.db.delete_user(user_id=user_id):
            return {"message":"User deleted successfully."}
        abort(404, message="Record doesn't exists.")
