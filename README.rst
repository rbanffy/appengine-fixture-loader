appengine-fixture-loader
========================

A simple way to load Django-like fixtures into the local development datastore, originally intended to be used by `testable_appengine <https://github.com/rbanffy/testable_appengine>`_.

Single-level loads
------------------

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

    loaded_data = load_fixture('tests/persons.json', kind = Person)

In our example, `loaded_data` will contain a list of already persisted Person models you can then manipulate and persist again.

Multi-kind loads
----------------

It's convenient to be able to load multiple kinds of objects from a single file. For those cases, we provide a simple way to identify the kind of object being loaded and to provide a set of models to use when loading the objects.

Consider our original example model::

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

and let's add a second one::

    class Dog(ndb.Model):
        """Another sample class"""
        name = ndb.StringProperty()

Now, if we wanted to make a single file load objects of the two kinds, we'd need to use the "__kind__" attribute in the JSON::

    [
        {
            "__kind__": "Person",
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
        {
            "__kind__": "Dog",
            "name": "Fido"
        }
    ]

And, to load the file, we'd have to::

    from appengine_fixture_loader.loader import load_fixture

and::

    loaded_data = load_fixture('tests/persons_and_dogs.json',
                               kinds={'Person': Person, 'Dog': Dog})

will result in a list of Persons and Dogs (in this case, one person and one dog).
