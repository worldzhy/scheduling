from marshmallow import Schema, fields, validates, ValidationError

class ForecastSchema(Schema):
    studio = fields.String(required=True)
    program = fields.String(required=True)
    location = fields.String(required=True)
    month = fields.Integer(required=True)
    year = fields.Integer(required=True)

    @validates('studio')
    def validate_studio(self, value: str):
        if not value.strip():
            raise ValidationError('studio cannot be an empty string')

    @validates('program')
    def validate_program(self, value: str):
        if not value.strip():
            raise ValidationError('program cannot be an empty string')
        
    @validates('location')
    def validate_location(self, value: str):
        if not value.strip():
            raise ValidationError('location cannot be an empty string')