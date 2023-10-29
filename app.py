import uuid
from flask import Flask, request
from db import shops, products

app = Flask(__name__)

#########
# SHOPS #
#########

@app.route('/shop')
def get_shops():
    return {"shops": list(shops.values())}

@app.route('/shop/<shop_id>')
def get_shop(shop_id):
    try:
        return shops[shop_id]
    except KeyError:
        return {"message": "Shop not found"}, 404

@app.route('/shop', methods=['POST'])
def create_shop():
    shop_data = request.json
    shop_id = uuid.uuid4().hex
    shop = {**shop_data, "id": shop_id}
    shops[shop_id] = shop
    return shop

@app.route("/shop/<shop_id>", methods=['DELETE'])
def delete_shop(shop_id):
    try:
        del shops[shop_id]
        return {"message": "Shop deleted"}
    except KeyError:
        return {"message": "Shop not Found"}, 404

############
# PRODUCTS #
############

@app.route('/product')
def get_products():
    return {"products": list(products.values())}

@app.route('/product/<product_id>')
def get_product(product_id):
    try:
        return products[product_id]
    except KeyError:
        return {"message": "Product not found"}, 404

@app.route('/product', methods=['POST'])
def create_product():
    new_product = request.json
    if new_product["shop_id"] not in shops:
        return {"message": "Shop not found"}, 404
    product_id = uuid.uuid4().hex
    product = {**new_product, "product_id": product_id}
    products[product_id] = product

    return product

@app.route("/product/<product_id>")
def update_product(product_id):
    product_data = request.json
    if "price" not in product_data or "name" not in product_data:
        return {"message": "Please ensure 'price' and 'name' are included in the request"}, 400
    try:
        product = products[product_id]
        # | -> Merge the dictionaries
        product |= product_data
        return product
    except KeyError:
        return {"message": "Product not Found"}, 404

@app.route("/product/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    try:
        del products[product_id]
        return {"message": "Product deleted"}
    except KeyError:
        return {"message": "Product not Found"}, 404

app.run()