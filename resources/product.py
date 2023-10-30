from flask.views import MethodView
from flask import request
import uuid
from flask_smorest import Blueprint, abort
from db import products
from schemas import ProductSchema, ProductUpdateSchema

blueprint = Blueprint("products", __name__, description="Operations on Products")

@blueprint.route("/product/<product_id>")
class Product(MethodView):
    @blueprint.response(200, ProductSchema)
    def get(self, product_id):
        try:
            return products[product_id]
        except KeyError:
            abort(404, "Product not Found")

    # put arguments first and responce second
    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, ProductSchema)
    def put(self, product_data, product_id): # product_data will be first because the decorator passes it first
        # product_data = request.json
        # if "price" not in product_data or "name" not in product_data:
            # abort(400, message="Please ensure 'price' and 'name' are included in the request")
        try:
            product = products[product_id]
            # | -> Merge the dictionaries
            product |= product_data
            return product
        except KeyError:
            abort(404, message="Product not Found")

    def delete(self, product_id):
        try:
            del products[product_id]
            return {"message": "Product deleted"}
        except KeyError:
            abort(404, message="Product not Found")

@blueprint.route("/product")
class ProductList(MethodView):
    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        return list(products.values())
        # return {"products": list(products.values())}

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, ProductSchema)
    def post(self, new_product):
        for product in products.values():
            if (new_product["name"] == product["name"] and new_product["shop_id"] == product["shop_id"]):
                abort(400, message="Product already exists")

        product_id = uuid.uuid4().hex
        product = {**new_product, "id": product_id}
        products[product_id] = product

        return product
