from flask.views import MethodView
from flask import request
import uuid
from flask_smorest import Blueprint, abort
from db import shops
from schemas import ShopSchema

blueprint = Blueprint("shops", __name__, description="Operations on Shops")

@blueprint.route("/shop/<shop_id>")
class Shop(MethodView):
    @blueprint.response(200, ShopSchema)
    def get(self, shop_id):
        try:
            return shops[shop_id]
        except KeyError:
            abort(404, message="Shop not Found")

    def delete(self, shop_id):
        try:
            del shops[shop_id]
            return {"message": "Shop deleted"}
        except KeyError:
            abort(404, message="Shop not Found")

@blueprint.route("/shop")
class ShopList(MethodView):
    @blueprint.response(200, ShopSchema(many=True))
    def get(self):
        return list(shops.values())
        # return {"shops": list(shops.values())}
    
    @blueprint.arguments(ShopSchema)
    @blueprint.response(201, ShopSchema)
    def post(sellf, shop_data):
        for shop in shops.values():
            if shop_data["name"] == shop["name"]:
                abort(400, message="Shop already exist")
        shop_id = uuid.uuid4().hex
        shop = {**shop_data, "id": shop_id}
        shops[shop_id] = shop
        return shop