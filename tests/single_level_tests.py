"""
Test the one-level loader
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


class LoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture('tests/persons.json', Person)

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_count(self):
        """Make sure we got 4 objects from the JSON file"""
        self.assertEqual(len(self.loaded_data), 4)

    def test_loaded_types(self):
        """Make sure all objects we loaded are instances of Person"""
        self.assertTrue(all([type(p) == Person for p in self.loaded_data]))

    def test_loaded(self):
        """Check whether the attributes we imported match the JSON contents"""
        # Test if the first record got in
        person = Person.query(Person.first_name == 'John').get()
        self.assertEqual(person.first_name, 'John')
        self.assertEqual(person.last_name, 'Doe')
        self.assertEqual(person.born, datetime.datetime(1968, 3, 3))
        self.assertEqual(person.thermostat_set_to, 18.34)
        self.assertFalse(person.processed)

        # Test for the third one
        person = Person.query(Person.last_name == 'Schneier' and
                              Person.first_name == 'Alice').get()
        self.assertEqual(person.first_name, 'Alice')
        self.assertEqual(person.last_name, 'Schneier')
        self.assertEqual(person.born, datetime.datetime(1999, 9, 19))
        self.assertTrue(person.snores)
        self.assertFalse(person.processed)

        # Test for the last one
        person = Person.query(
            Person.born == datetime.datetime(1980, 5, 25, 0, 0, 0)).get()
        self.assertEqual(person.first_name, 'Bob')
        self.assertEqual(person.last_name, 'Schneier')
        self.assertEqual(person.born, datetime.datetime(1980, 5, 25))
        self.assertFalse(person.processed)


class ProcessedLoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file and post-process it"""
    def setUp(self):

        def process(p):
            p.processed = True

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture(
            'tests/persons.json',
            Person,
            post_processor=process
        )

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_count(self):
        """Make sure we got 4 objects from the JSON file"""
        self.assertEqual(len(self.loaded_data), 4)

    def test_loaded_types(self):
        """Make sure all objects we loaded were processed"""
        self.assertTrue(all([p.processed for p in self.loaded_data]))


class ProcessedLoaderTest(unittest.TestCase):
    """Tests if the processor is invoked once per loaded entity"""
    def setUp(self):

        self.counter = 0

        def counted_process(p):
            p.processed = True
            self.counter += 1

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture(
            'tests/persons.json',
            Person,
            post_processor=counted_process
        )

    def tearDown(self):
        self.testbed.deactivate()

    def test_single_invoke(self):
        """Make sure processor is invoked once per imported entity"""
        self.assertEqual(self.counter, 4)


if __name__ == '__main__':
    unittest.main()
