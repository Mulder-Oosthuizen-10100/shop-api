from marshmallow import Schema, fields

class PlainPructSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainShopSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)    

class ProductSchema(PlainPructSchema):
    shop_id = fields.Str(required=True)
    shop = fields.Nested(PlainShopSchema(), dump_only=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class ShopSchema(PlainShopSchema):
    products = fields.List(fields.Nested(PlainPructSchema()), dump_only=True)

