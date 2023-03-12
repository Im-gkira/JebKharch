from marshmallow import fields, Schema


class Expense(Schema):
    id = fields.Integer(required=True, load_only=True)
    description = fields.String(default="")
    amount = fields.Integer(required=True)
    category = fields.String(required=True)


class Category(Schema):
    name = fields.String(required=True)
    category_id = fields.String(required=True, load_only=True)
