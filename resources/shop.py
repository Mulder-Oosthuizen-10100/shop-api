from flask import request
import uuid
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import ShopSchema
from models import ShopModel

blueprint = Blueprint("shops", __name__, description="Operations on Shops")

@blueprint.route("/shop/<shop_id>")
class Shop(MethodView):
    @blueprint.response(200, ShopSchema)
    def get(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        return shop
    
        # try:
        #     return shops[shop_id]
        # except KeyError:
        #     abort(404, message="Shop not Found")

    def delete(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)

        db.session.delete(shop)
        db.session.commit()

        return {"message": "Shop deleted"}        
        # raise NotImplementedError("Deleting not Implented")

        # try:
        #     del shops[shop_id]
        #     return {"message": "Shop deleted"}
        # except KeyError:
        #     abort(404, message="Shop not Found")

@blueprint.route("/shop")
class ShopList(MethodView):
    @blueprint.response(200, ShopSchema(many=True))
    def get(self):
        return ShopModel.query.all()
        # return list(shops.values())
        # return {"shops": list(shops.values())}
    
    @blueprint.arguments(ShopSchema)
    @blueprint.response(201, ShopSchema)
    def post(sellf, shop_data):

        shop = ShopModel(**shop_data)

        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A shop with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the shop")

        # for shop in shops.values():
        #     if shop_data["name"] == shop["name"]:
        #         abort(400, message="Shop already exist")
        # shop_id = uuid.uuid4().hex
        # shop = {**shop_data, "id": shop_id}
        # shops[shop_id] = shop
        return shop