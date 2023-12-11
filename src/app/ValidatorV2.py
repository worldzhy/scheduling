from marshmallow import Schema, ValidationError, fields, validates

class ForecastParamsSchema(Schema):
    studio_id = fields.Integer(required=True)
    program_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    timeslot_start_id = fields.Integer(required=True)
    timeslot_end_id = fields.Integer(required=True)
    month = fields.Integer(required=True)
    year = fields.Integer(required=True)

class ForecastConfigSchema(Schema):
    force_fetch = fields.Boolean(required=False)

class ForecastSchema(Schema):
    params = fields.Nested(ForecastParamsSchema, required=True)
    config = fields.Nested(ForecastConfigSchema)

    @validates("config")
    def validate_config(self, config: fields.Nested):
        if config and not isinstance(config.get("force_fetch"), bool):
            raise ValidationError("'fetch_force' in 'config' must be a boolean.")