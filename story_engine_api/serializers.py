from marshmallow import Schema, fields

class DeckSchema(Schema):
    name = fields.Str()
    id = fields.Int()

class PackSchema(Schema):
    name = fields.Str()
    id = fields.Int()
