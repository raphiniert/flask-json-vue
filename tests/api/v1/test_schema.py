import pytest
import unittest

from flaskjsonvue.api.v1.schemes.base import BaseJsonSchema
from flaskjsonvue.api.v1.schemes.demo import DemoJsonSchema
from flaskjsonvue.api.v1.schemes.address import AddressJsonSchema

#
# BaseJsonSchema
#
class BaseJsonSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all class methods"""

        class NamedSchema(BaseJsonSchema):
            name = "Named"
            description = "Named schema description"

        class UnnmamedSchema(BaseJsonSchema):
            pass

        class NoDescriptionSchema(BaseJsonSchema):
            name = "No description schema"

        class NamedUmlautSpecialCharSchema(BaseJsonSchema):
            name = "Name w/ äöü"

        class OnlyUmlautsSchema(BaseJsonSchema):
            name = "ÄÖÜ"

        cls.named_schema = NamedSchema()
        cls.unnamed_schema = UnnmamedSchema()
        cls.no_description_schema = NoDescriptionSchema()
        cls.named_umlaut_special_char_schema = NamedUmlautSpecialCharSchema()
        cls.only_umlauts_schema = OnlyUmlautsSchema

    def setUp(self) -> None:
        """Set up run once for every test method"""
        pass

    def test_schema_base_url(self):
        assert self.named_schema.schema_base_url() == "/api/v1/schema/named"
        assert (
            self.no_description_schema.schema_base_url()
            == "/api/v1/schema/no-description-schema"
        )
        assert (
            self.named_umlaut_special_char_schema.schema_base_url()
            == "/api/v1/schema/name-w"
        )

    def test_schema_base_url_invalid_name(self):
        with pytest.raises(NotImplementedError, match="Invalid schema name!"):
            with self.assertLogs("flaskjsonvue", level="ERROR") as cm:
                self.only_umlauts_schema.schema_base_url()
                self.assertEqual(
                    cm.output,
                    [
                        "ERROR:flaskjsonvue:Cannot create schema base url for name: 'ÄÖÜ'"
                    ],
                )

    def test_schema_base_url_unnamed(self):
        with pytest.raises(NotImplementedError, match="No name set!"):
            with self.assertLogs("flaskjsonvue", level="ERROR") as cm:
                self.unnamed_schema.schema_base_url()
                self.assertEqual(
                    cm.output,
                    [
                        "ERROR:flaskjsonvue:Cannot create schema detail for class: 'UnnamedSchema'. No name set!"
                    ],
                )

    def test_schema_detail(self):
        assert self.named_schema.detail() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/named/detail.schema.json",
            "title": "Named",
            "description": "Named schema description",
            "type": "object",
            "relations": {},
            "properties": {
                "id": {
                    "description": "The named's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "name": {"description": "The named's name", "type": "string"},
            },
            "required": ["id", "name"],
        }

    def test_schema_detail_no_description(self):
        with pytest.raises(NotImplementedError, match="No description set!"):
            with self.assertLogs("flaskjsonvue", level="ERROR") as cm:
                self.no_description_schema.detail()
                self.assertEqual(
                    cm.output,
                    [
                        "ERROR:flaskjsonvue:Cannot create schema detail for class: 'NoDescriptionSchema'. No description set!"
                    ],
                )

    def test_schema_create(self):
        assert self.named_schema.create() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/named/create.schema.json",
            "title": "Named",
            "description": "Named schema description",
            "type": "object",
            "relations": {},
            "properties": {
                "name": {"description": "The named's name", "type": "string"},
            },
            "required": ["name"],
        }

    def test_schema_update(self):
        assert self.named_schema.update() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/named/update.schema.json",
            "title": "Named",
            "description": "Named schema description",
            "type": "object",
            "relations": {},
            "properties": {
                "id": {
                    "description": "The named's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "name": {"description": "The named's name", "type": "string"},
            },
            "required": ["id", "name"],
        }

    def test_schema_delete(self):
        assert self.named_schema.delete() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/named/delete.schema.json",
            "title": "Named",
            "description": "Named schema description",
            "type": "object",
            "relations": {},
            "properties": {
                "id": {
                    "description": "The named's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
            },
            "required": ["id"],
        }

    def test_schema_array(self):
        assert self.named_schema.array() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/named/array.schema.json",
            "title": "Named",
            "description": "Array of Named objects",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "description": "The named's unique identifier",
                        "type": "integer",
                        "min": 1,
                    },
                    "name": {"description": "The named's name", "type": "string"},
                },
                "required": ["id", "name"],
            },
        }

    def tearDown(self) -> None:
        """Clean up run after every test method"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Method called after tests in an individual class have run"""
        pass


class TestDemoJsonSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all class methods"""
        cls.demo_schema = DemoJsonSchema()

    def setUp(self) -> None:
        """Set up run once for every test method"""
        pass

    def test_schema_base_url(self):
        assert self.demo_schema.schema_base_url() == "/api/v1/schema/demo"

    def tearDown(self) -> None:
        """Clean up run after every test method"""
        pass

    def test_schema_detail(self):
        assert self.demo_schema.detail() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/demo/detail.schema.json",
            "title": "Demo",
            "description": "Demo JSON object",
            "type": "object",
            "relations": {"address_id": "address"},
            "properties": {
                "address_id": {
                    "type": ["integer", "null"],
                    "description": f"The demo's address id.",
                },
                "entry_date": {
                    "description": f"The demo's entry date.",
                    "type": "string",
                    "format": "date-time",
                },
                "decimal_value": {
                    "description": f"The demo's decimal number.",
                    "type": "number",
                },
                "id": {
                    "description": "The demo's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "name": {
                    "description": "The demo's name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": ["id", "name", "entry_date", "decimal_value", "address_id"],
        }

    def test_schema_create(self):
        assert self.demo_schema.create() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/demo/create.schema.json",
            "title": "Demo",
            "description": "Demo JSON object",
            "type": "object",
            "relations": {"address_id": "address"},
            "properties": {
                "address_id": {
                    "type": ["integer", "null"],
                    "description": f"The demo's address id.",
                },
                "entry_date": {
                    "description": f"The demo's entry date.",
                    "type": "string",
                    "format": "date-time",
                },
                "decimal_value": {
                    "description": f"The demo's decimal number.",
                    "type": "number",
                },
                "name": {
                    "description": "The demo's name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": ["name", "entry_date", "decimal_value", "address_id"],
        }

    def test_schema_update(self):
        assert self.demo_schema.update() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/demo/update.schema.json",
            "title": "Demo",
            "description": "Demo JSON object",
            "type": "object",
            "relations": {"address_id": "address"},
            "properties": {
                "address_id": {
                    "type": ["integer", "null"],
                    "description": f"The demo's address id.",
                },
                "entry_date": {
                    "description": f"The demo's entry date.",
                    "type": "string",
                    "format": "date-time",
                },
                "decimal_value": {
                    "description": f"The demo's decimal number.",
                    "type": "number",
                },
                "id": {
                    "description": "The demo's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "name": {
                    "description": "The demo's name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": ["id", "name", "entry_date", "decimal_value", "address_id"],
        }

    def test_schema_delete(self):
        assert self.demo_schema.delete() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/demo/delete.schema.json",
            "title": "Demo",
            "description": "Demo JSON object",
            "type": "object",
            "relations": {"address_id": "address"},
            "properties": {
                "id": {
                    "description": "The demo's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
            },
            "required": ["id"],
        }

    def test_schema_array(self):
        assert self.demo_schema.array() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/demo/array.schema.json",
            "title": "Demo",
            "description": "Array of Demo objects",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "address_id": {
                        "type": ["integer", "null"],
                        "description": f"The demo's address id.",
                    },
                    "entry_date": {
                        "description": f"The demo's entry date.",
                        "type": "string",
                        "format": "date-time",
                    },
                    "decimal_value": {
                        "description": f"The demo's decimal number.",
                        "type": "number",
                    },
                    "id": {
                        "description": "The demo's unique identifier",
                        "type": "integer",
                        "min": 1,
                    },
                    "name": {
                        "description": "The demo's name.",
                        "type": "string",
                        "minLength": 1,
                    },
                },
                "required": ["id", "name", "entry_date", "decimal_value", "address_id"],
            },
        }

    @classmethod
    def tearDownClass(cls):
        """Method called after tests in an individual class have run"""
        pass


class TestAddressJsonSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all class methods"""
        cls.schema = AddressJsonSchema()

    def setUp(self) -> None:
        """Set up run once for every test method"""
        pass

    def test_schema_base_url(self):
        assert self.schema.schema_base_url() == "/api/v1/schema/address"

    def tearDown(self) -> None:
        """Clean up run after every test method"""
        pass

    def test_schema_detail(self):
        assert self.schema.detail() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/address/detail.schema.json",
            "title": "Address",
            "description": "Address JSON object",
            "type": "object",
            "relations": {},
            "properties": {
                "id": {
                    "description": "The address's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "street": {
                    "description": "The address's street name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": [
                "id",
                "street",
            ],
        }

    def test_schema_create(self):
        assert self.schema.create() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/address/create.schema.json",
            "title": "Address",
            "description": "Address JSON object",
            "type": "object",
            "relations": {},
            "properties": {
                "street": {
                    "description": "The address's street name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": [
                "street",
            ],
        }

    def test_schema_update(self):
        assert self.schema.update() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/address/update.schema.json",
            "title": "Address",
            "description": "Address JSON object",
            "type": "object",
            "relations": {},
            "properties": {
                "id": {
                    "description": "The address's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
                "street": {
                    "description": "The address's street name.",
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": [
                "id",
                "street",
            ],
        }

    def test_schema_delete(self):
        assert self.schema.delete() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/address/delete.schema.json",
            "title": "Address",
            "description": "Address JSON object",
            "type": "object",
            "relations": {},
            "properties": {
                "id": {
                    "description": "The address's unique identifier",
                    "type": "integer",
                    "min": 1,
                },
            },
            "required": ["id"],
        }

    def test_schema_array(self):
        assert self.schema.array() == {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "/api/v1/schema/address/array.schema.json",
            "title": "Address",
            "description": "Array of Address objects",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "description": "The address's unique identifier",
                        "type": "integer",
                        "min": 1,
                    },
                    "street": {
                        "description": "The address's street name.",
                        "type": "string",
                        "minLength": 1,
                    },
                },
                "required": [
                    "id",
                    "street",
                ],
            },
        }

    @classmethod
    def tearDownClass(cls):
        """Method called after tests in an individual class have run"""
        pass
