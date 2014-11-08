appengine-fixture-loader
========================

A simple way to load Django-like fixtures into the local development datastore, originally intended to be used by `testable_appengine <https://github.com/rbanffy/testable_appengine>`_.

Let's say you have a model like this::

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

If you want to load a data file like this::

    [
        {
            "born": "1968-03-03T00:00:00",
            "first_name": "John",
            "last_name": "Doe",
            "favorite_movies": [
                "2001",
                "The Day The Earth Stood Still (1951)"
            ],
            "snores": false,
            "sleeptime": "23:00",
            "started_school": "1974-02-15",
            "thermostat_set_to": 18.34,
            "userid": 1
        },

    ...

        {
            "born": "1980-05-25T00:00:00",
            "first_name": "Bob",
            "last_name": "Schneier",
            "favorite_movies": [
                "2001",
                "Superman"
            ],
            "snores": true,
            "sleeptime": "22:00",
            "started_school": "1985-08-01",
            "thermostat_set_to": 18.34,
            "userid": -5
        }
    ]

All you need to do is to::

    from appengine_fixture_loader.loader import load_fixture

and then::

    loaded_data = load_fixture('tests/persons.json', Person)

In our example, `loaded_data` will contain a list of already persisted Person models you can then manipulate and persist again.
