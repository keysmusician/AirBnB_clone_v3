#!/usr/bin/python3
"""
Unittests for DBStorage, the database storage engine.
"""
import inspect
import models
from models.engine import db_storage
from models.engine.db_storage import DBStorage
import pep8
import unittest
from models import storage
from models.state import State
from models.city import City


class TestDBStorageDocs(unittest.TestCase):
    """Tests the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        test_path = 'tests/test_models/test_engine/test_db_storage.py'
        result = pep8s.check_files([test_path])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """Tests get method from db storage"""
        dic = {"name": "Amazingland"}
        instance = State(**dic)
        storage.new(instance)
        storage.save()
        get_instance = storage.get(State, instance.id)
        self.assertEqual(get_instance, instance)

    def test_count(self):
        """Tests count method from db storage"""
        dic = {"name": "Wonderland"}
        state = State(**dic)
        storage.new(state)
        dic = {"name": "Fabulouscity", "state_id": state.id}
        city = City(**dic)
        storage.new(city)
        storage.save()
        count = storage.count()
        self.assertEqual(len(storage.all()), count)
