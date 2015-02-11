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


class AncestorLoaderTest(unittest.TestCase):
    """Tests if we can load a JSON file containing __children__"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.loaded_data = load_fixture('tests/hard_coded_id.json', Person)

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded(self):
        """Check whether the attributes we imported match the JSON contents"""
        # Test if John got in
        john_key = ndb.Key('Person', 'jdoe')
        john = john_key.get()
        self.assertEqual(john.first_name, 'John')
        self.assertEqual(john.last_name, 'Doe')
        self.assertEqual(john.born, datetime.datetime(1968, 3, 3))
        self.assertEqual(john.thermostat_set_to, 18.34)
        self.assertFalse(john.processed)


if __name__ == '__main__':
    unittest.main()
