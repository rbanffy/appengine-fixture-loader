"""
Test the one-level, multi-type loader
"""

import datetime
import unittest

# The test will error out if we can't import these items
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from appengine_fixture_loader.loader import load_fixture


class Person(ndb.Model):
    """Our sample class"""
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    born = ndb.DateTimeProperty()
    userid = ndb.IntegerProperty()
    thermostat_set_to = ndb.FloatProperty()
    snores = ndb.BooleanProperty()
    started_school = ndb.DateProperty()
    sleeptime = ndb.TimeProperty()
    favorite_movies = ndb.JsonProperty()
    processed = ndb.BooleanProperty(default=False)
    appropriate_adult = ndb.KeyProperty()


class Dog(ndb.Model):
    """Another sample class"""
    name = ndb.StringProperty()
    processed = ndb.BooleanProperty(default=False)
    owner = ndb.KeyProperty()


class MultiLevelLoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file with key-based hierarchies"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture('tests/persons_children_and_dogs.json',
                                        {'Person': Person, 'Dog': Dog})

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_count(self):
        """Make sure we got 7 total objects from the JSON file"""
        self.assertEqual(len(self.loaded_data), 7)

    def test_total_count(self):
        """Make sure we got 6 objects loaded"""
        self.assertEqual(Person.query().count(), 6)

    def test_loaded(self):
        """Check whether the attributes we imported match the JSON contents"""
        # Test if John got in
        john = Person.query(Person.first_name == 'John').get()
        self.assertEqual(john.first_name, 'John')
        self.assertEqual(john.last_name, 'Doe')
        self.assertEqual(john.born, datetime.datetime(1968, 3, 3))
        self.assertEqual(john.thermostat_set_to, 18.34)
        self.assertFalse(john.processed)

    def test_single_children(self):
        """Tests if a single child was correctly imported"""

        # Get John
        john = Person.query(Person.first_name == 'John').get()

        # Test if Jane got in
        jane = Person.query(Person.appropriate_adult == john.key).get()
        self.assertEqual(jane.first_name, 'Jane')

    def test_multiple_children(self):
        """Tests if multiple children were correctly imported"""

        # Get Alice
        alice = Person.query(Person.first_name == 'Alice').get()
        self.assertEqual(alice.last_name, 'Schneier')

        # Get the good and evil twins
        self.assertEqual(
            Person.query(Person.appropriate_adult == alice.key).count(), 2)

    def test_child_of_a_different_type(self):
        """Tests a child record of a different kind"""
        charlie = Person.query(Person.first_name == 'Charlie').get()
        fido = Dog.query(Dog.owner == charlie.key).get()
        self.assertEqual(fido.name, 'Fido')


if __name__ == '__main__':
    unittest.main()
