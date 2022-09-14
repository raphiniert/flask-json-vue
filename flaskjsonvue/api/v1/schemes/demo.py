from flaskjsonvue.api.v1.schemes.base import BaseJsonSchema


class DemoJsonSchema(BaseJsonSchema):
    name = "Demo"
    description = "Demo JSON object"
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
                "name": {
                    "type": "string",
                    "description": f"The {cls.name.lower()}'s name.",
                    "minLength": 1,
                },
                "entry_date": {
                    "description": f"The {cls.name.lower()}'s entry date.",
                    "type": "string",
                    "format": "date-time",
                },
                "decimal_value": {
                    "description": f"The {cls.name.lower()}'s decimal number.",
                    "type": "number",
                },
            },
            "required": [
                "id",
                "name",
                "entry_date",
                "decimal_value",
            ],
        }
