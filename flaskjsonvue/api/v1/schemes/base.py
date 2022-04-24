import logging
import string

logger = logging.getLogger("flaskjsonvue")


class BaseJsonSchema:
    """Basic json schema containing id and name"""

    @classmethod
    def schema_base_url(cls):
        if not hasattr(cls, "name"):
            logger.error(
                f"Cannot create schema base url for class: '{cls.__name__}'. No name set!"
            )
            raise NotImplementedError("No name set!")
        name = "".join(
            [
                letter.lower() if letter in string.ascii_letters else "-"
                for letter in cls.name
            ]
        )
        # remove ending -
        while len(name) and name[-1] == "-":
            name = name[:-1]
        if not len(name):
            logger.error(f"Cannot create schema base url for name: '{cls.name}'")
            raise NotImplementedError("Invalid schema name!")
        return f"/api/v1/schema/{name}"

    @classmethod
    def detail(cls):
        if not hasattr(cls, "description"):
            logger.error(
                f"Cannot create schema detail for class: '{cls.__name__}'. No description set!"
            )
            raise NotImplementedError("No description set!")

        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{cls.schema_base_url()}/detail.schema.json",
            "title": cls.name,
            "description": cls.description,
            "type": "object",
            "relations": cls.relations if hasattr(cls, "relations") else {},
            "properties": {
                "id": {
                    "description": f"The {cls.name.casefold()}'s unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "name": {
                    "description": f"The {cls.name.casefold()}'s name",
                    "type": "string",
                },
            },
            "required": ["id", "name"],
        }

    @classmethod
    def create(cls):
        """Remove id property"""
        schema = cls.detail()
        schema["$id"] = f"{cls.schema_base_url()}/create.schema.json"
        schema["properties"].pop("id")
        # filter properties that are not required on create
        schema["required"] = [
            property_name
            for property_name in schema["required"]
            if property_name not in ["id"]
        ]
        return schema

    @classmethod
    def update(cls):
        schema = cls.detail()
        schema["$id"] = f"{cls.schema_base_url()}/update.schema.json"
        return schema

    @classmethod
    def delete(cls):
        """Remove all properties except for id"""
        schema = cls.detail()
        schema["$id"] = f"{cls.schema_base_url()}/delete.schema.json"
        for property_name in list(schema["properties"].keys()):
            if property_name not in ["id"]:
                schema["properties"].pop(property_name)
        schema["required"] = ["id"]
        return schema

    @classmethod
    def array(cls):
        """Array scheme for detail properties"""
        schema = cls.detail()
        array_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{cls.schema_base_url()}/array.schema.json",
            "title": f"{cls.name}",
            "description": f"Array of {cls.name} objects",
            "type": "array",
            "items": {
                "type": schema["type"],
                "properties": schema["properties"],
                "required": schema["required"],
            },
        }
        return array_schema
