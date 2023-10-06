from marshmallow import Schema, fields, validates, ValidationError

class ForecastSchema(Schema):
    studio_id = fields.Integer(required=True)
    program_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    month = fields.Integer(required=True)
    year = fields.Integer(required=True)