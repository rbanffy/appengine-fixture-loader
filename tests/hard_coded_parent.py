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


class Dog(ndb.Model):
    """Another sample class"""
    name = ndb.StringProperty()


class Flea(ndb.Model):
    """Another sample class"""
    name = ndb.StringProperty()


class LoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file with more than one kind"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        load_fixture('tests/hard_coded_parent_person_dog.json',
                     {'Person': Person, 'Dog': Dog})
        load_fixture('tests/hard_coded_parent_fleas.json',
                     {'Dog': Dog, "Flea", Flea})


    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded(self):
        """Check whether the attributes we imported match the JSON contents"""
        # Test if the Person got in
        person = Person.query(Person.first_name == 'John').get()
        self.assertEqual(person.first_name, 'John')
        self.assertEqual(person.last_name, 'Doe')
        self.assertEqual(person.born, datetime.datetime(1968, 3, 3))
        self.assertEqual(person.thermostat_set_to, 18.34)

        # Test if the Dog got in
        dog = Dog.query(Dog.name == 'Fido').get()
        self.assertEqual(dog.name, 'Fido')

        # Check for Flido and Fliido


    def test_ancestor_query(self):
        """Check whether the objects imported preserve their ancestry"""
        pass

if __name__ == '__main__':
    unittest.main()
