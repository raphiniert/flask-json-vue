from flaskjsonvue.api.v1.schemes.base import BaseJsonSchema


class AddressJsonSchema(BaseJsonSchema):
    name = "Address"
    description = "Address JSON object"
    relations = {}

    @classmethod
    def detail(cls):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{cls.schema_base_url()}/detail.schema.json",
            "title": cls.name,
            "description": cls.description,
            "type": "object",
            "relations": cls.relations,
            "properties": {
                "id": {
                    "description": f"The {cls.name.lower()}'s unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "street": {
                    "description": f"The {cls.name.lower()}'s street name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": [
                "id",
                "street",
            ],
        }
