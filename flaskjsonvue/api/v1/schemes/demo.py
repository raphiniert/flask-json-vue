from flaskjsonvue.api.v1.schemes.base import BaseJsonSchema


class DemoJsonSchema(BaseJsonSchema):
    title = "Demo"
    description = "Demo JSON Object"
    relations = []

    @classmethod
    def detail(cls):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{cls.schema_base_url()}/detail.schema.json",
            "title": cls.title,
            "description": cls.description,
            "type": "object",
            "relations": cls.relations,
            "properties": {
                "id": {
                    "description": f"The {cls.title.lower()}'s unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "name": {
                    "type": ["string", "null"],
                    "description": f"The {cls.title.lower()}' name.",
                    "minLength": 1,
                },
                "entry_date": {
                    "description": f"The {cls.title.lower()}'s entry date.",
                    "type": "string",
                    "format": "date-time",
                },
                "decimal_number": {
                    "description": f"The {cls.title.lower()}'s decimal number.",
                    "type": "number",
                },
            },
            "required": [
                "id",
                "name",
                "entry_date",
                "decimal_number",
            ],
        }
