import pytest
import unittest

from flaskjsonvue.models import Demo, DisplayName, JsonModel

#
# DisplayName
#
class DisplayNameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all class methods"""

        class NamedObject(DisplayName):
            def __init__(self, name):
                self.name = name

        class NamelessObject(DisplayName):
            pass

        cls.named_object = NamedObject("test")
        cls.nameless_object = NamelessObject()

    def setUp(self) -> None:
        """Set up run once for every test method"""
        pass

    def test_display_name(self):
        assert self.named_object.display_name == "test"

    def test_diplay_name_without_name(self):
        with pytest.raises(
            NotImplementedError, match="NamelessObject has no display name"
        ):
            self.nameless_object.display_name

    def tearDown(self) -> None:
        """Clean up run after every test method"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Method called after tests in an individual class have run"""
        pass


#
# JsonModel
#
class JsonModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all class methods"""

        class NamedObject(JsonModel):
            def __init__(self, name):
                self.name = name

        class NamelessObject(JsonModel):
            pass

        cls.named_object = NamedObject("test")
        cls.nameless_object = NamelessObject()
        cls.demo_object = Demo(
            id=1,
            address_id=None,
            name="demo",
            decimal_value=1.0,
            entry_date="2022-01-01T01:23:45+01:00",
        )

    def setUp(self) -> None:
        """Set up run once for every test method"""
        pass

    def test_json_model_update(self):
        assert self.named_object.name == "test"
        self.named_object.update(name="test2")
        assert self.named_object.name == "test2"

    def test_json_model_update_no_attribute(self):
        with self.assertLogs("flaskjsonvue", level="INFO") as cm:
            self.nameless_object.update(name="test2")
            # logging.getLogger("flaskjsonvue").info("NamelessObject has no attribute: 'name'")
            self.assertEqual(
                cm.output, ["INFO:flaskjsonvue:NamelessObject has no attribute: 'name'"]
            )

        assert hasattr(self.nameless_object, "name") is False

    def test_json_model_json(self):
        assert self.demo_object.json == {
            "meta": {"display_name": "demo"},
            "data": {
                "address_id": None,
                "decimal_value": 1.0,
                "entry_date": "2022-01-01T01:23:45+01:00",
                "id": 1,
                "name": "demo",
            },
        }

    def test_json_model_json_no_table(self):
        with pytest.raises(
            NotImplementedError,
            match="NamelessObject has no table",
        ):
            self.nameless_object.json

    def tearDown(self) -> None:
        """Clean up run after every test method"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Method called after tests in an individual class have run"""
        pass


#
# Demo
#
class DemoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all class methods"""

        cls.demo_object = Demo(
            id=1,
            address_id=None,
            name="demo",
            decimal_value=1.0,
            entry_date="2022-01-01T00:00:00+01:00",
        )

    def setUp(self) -> None:
        """Set up run once for every test method"""
        pass

    def test_demo_repr(self):
        assert self.demo_object.__repr__() == "<Demo demo (1)>"

    def tearDown(self) -> None:
        """Clean up run after every test method"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Method called after tests in an individual class have run"""
        pass
