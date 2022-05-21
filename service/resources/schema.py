from marshmallow_jsonapi import Schema, fields


class DoorSchema(Schema):
    id = fields.Str(dump_only=True)
    series = fields.Str()

    class Meta:
        type_ = "door"
        self_url = "/door/{id}"
        self_url_kwargs = {"id": "<id>"}
        self_url_many = "/door/"
