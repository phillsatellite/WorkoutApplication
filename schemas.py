from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Username cannot be blank.")
    )
    email = fields.Email(required=True, error_messages={"validator_failed": "Invalid email address."})

    # Never serialize the password hash
    class Meta:
        load_only = ("password",)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Title cannot be blank.")
    )
    notes = fields.Str(load_default="")
    duration = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration must be a positive number.")
    )
    user_id = fields.Int(dump_only=True)


user_schema = UserSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)