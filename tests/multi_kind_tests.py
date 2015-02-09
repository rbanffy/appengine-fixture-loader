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


class Dog(ndb.Model):
    """Another sample class"""
    name = ndb.StringProperty()
    processed = ndb.BooleanProperty(default=False)


class MultiLoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file with more than one kind"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture('tests/persons_and_dogs.json',
                                        {'Person': Person, 'Dog': Dog})

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_count(self):
        """Make sure we got 2 objects from the JSON file"""
        self.assertEqual(len(self.loaded_data), 2)

    def test_loaded(self):
        """Check whether the attributes we imported match the JSON contents"""
        # Test if the Person got in
        person = Person.query(Person.first_name == 'John').get()
        self.assertEqual(person.first_name, 'John')
        self.assertEqual(person.last_name, 'Doe')
        self.assertEqual(person.born, datetime.datetime(1968, 3, 3))
        self.assertEqual(person.thermostat_set_to, 18.34)
        self.assertFalse(person.processed)

        # Test if the Dog got in
        dog = Dog.query(Dog.name == 'Fido').get()
        self.assertEqual(dog.name, 'Fido')


class ProcessedMultiLoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file and post-process it"""
    def setUp(self):

        def process(p):
            p.processed = True

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture(
            'tests/persons_and_dogs.json',
            {'Person': Person, 'Dog': Dog},
            post_processor=process
        )

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_count(self):
        """Make sure we got 2 objects from the JSON file"""
        self.assertEqual(len(self.loaded_data), 2)

    def test_loaded_types(self):
        """Make sure all objects we loaded were processed"""
        self.assertTrue(all([p.processed for p in self.loaded_data]))


if __name__ == '__main__':
    unittest.main()
