from flask import Flask, request

app = Flask(__name__)

shops = [{"name":"PnP", "products":[{"name":"apple", "price": 800}]}]

@app.route('/shops')
def get_shops():
    return shops

@app.route('/shops', methods=['POST'])
def create_shop():
    shop = request.json

    # print("Shop", shop)

    shops.append(shop)

    return shop, 201

app.run()