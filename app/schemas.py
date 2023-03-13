from marshmallow import fields, Schema


class Expense(Schema):
    id = fields.Integer(required=True, dump_only=True)
    description = fields.String(default="")
    amount = fields.Integer(required=True)
    category = fields.String(required=True)


class Category(Schema):
    name = fields.String(required=True)
    category_id = fields.String(required=True, dump_only=True)


class User(Schema):
    id = fields.Integer(required=True, dump_only=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
