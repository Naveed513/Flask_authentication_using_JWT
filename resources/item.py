from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import (ItemSchema, ItemGetSchema,
SuccessMessageSchema, ItemOptionalQuerySchema,
 ItemQuerySchema)
from db.item import ItemDatabase
from flask_jwt_extended import jwt_required


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route('/item')
class Items(MethodView):

    def __init__(self):
        self.db = ItemDatabase()

    @jwt_required()
    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOptionalQuerySchema, location='query')
    def get(self, args):
        item_id = args.get('id')
        if not item_id:
            return self.db.get_items()
        result = self.db.get_item(item_id=item_id)
        if result:
            return result
        abort(404, message="Record doesn't exists.")

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, SuccessMessageSchema)
    def post(self, request_data):
        self.db.add_item(body=request_data)
        return {'message':'Item added successfully'}, 201

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location='query')
    def put(self, request_data, args):
        item_id = args.get('id')
        if self.db.update_item(item_id=item_id, body=request_data):
            return {'message':'Item updated successfully'}
        abort(404, message="Record doesn't exists.")

    @jwt_required()
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location='query')
    def delete(self, args):
        item_id = args.get('id')
        if self.db.delete_item(item_id=item_id):
            return {"message":"Item deleted successfully."}
        abort(404, message="Record doesn't exists.")
