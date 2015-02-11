appengine-fixture-loader
========================

A simple way to load Django-like fixtures into the local development datastore, originally intended to be used by `testable_appengine <https://github.com/rbanffy/testable_appengine>`_.

Installing
----------

For the less adventurous, Appengine-Fixture-Loader is available on PyPI at https://pypi.python.org/pypi/Appengine-Fixture-Loader.

Single-kind loads
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
            "__id__": "jdoe",
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

The `__id__` attribute, when defined, will save the object with that given id. In our case, the key to the first object defined will be a `ndb.Key('Person', 'jdoe')`. The key may be defined on an object by object base - where the `__id__` parameter is omitted, an automatic id will be generated - the key to the second one will be something like `ndb.Key('Person', 1)`.

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

Now, if we wanted to make a single file load objects of the two kinds, we'd need to use the `__kind__` attribute in the JSON::

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

Multi-kind, multi-level loads
-----------------------------

Anther common case is having hierarchies of entities that you want to reconstruct for your tests.

Using slightly modified versions of our example classes::

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

and::

    class Dog(ndb.Model):
        """Another sample class"""
        name = ndb.StringProperty()
        processed = ndb.BooleanProperty(default=False)
        owner = ndb.KeyProperty()

And using `__children__[attribute_name]__` like meta-attributes, as in::

    [
        {
            "__kind__": "Person",
            "born": "1968-03-03T00:00:00",
            "first_name": "John",
            "last_name": "Doe",

            ...

            "__children__appropriate_adult__": [
                {
                    "__kind__": "Person",
                    "born": "1970-04-27T00:00:00",

                    ...

                    "__children__appropriate_adult__": [
                        {
                            "__kind__": "Person",
                            "born": "1980-05-25T00:00:00",
                            "first_name": "Bob",

                            ...

                            "userid": 3
                        }
                    ]
                }
            ]
        },
        {
            "__kind__": "Person",
            "born": "1999-09-19T00:00:00",
            "first_name": "Alice",

            ...

            "__children__appropriate_adult__": [
                {
                    "__kind__": "Person",

                    ...

                    "__children__owner__": [
                        {
                            "__kind__": "Dog",
                            "name": "Fido"
                        }
                    ]
                }
            ]
        }
    ]

you can reconstruct entire entity trees for your tests.

Parent/Ancestor-based relationships with automatic keys
-------------------------------------------------------

It's also possible to set the `parent` by using the `__children__` attribute.

For our example classes, importing::

    [
        {
            "__kind__": "Person",
            "first_name": "Alice",

            ...

            "__children__": [
                {
                    "__kind__": "Person",
                    "first_name": "Bob",
                    ...

                    "__children__owner__": [
                        {
                            "__kind__": "Dog",
                            "name": "Fido"
                        }
                    ]
                }
            ]
        }
    ]

should be equivalent to::

    alice = Person(first_name='Alice')
    alice.put()
    bob = Person(first_name='Bob', parent=alice)
    bob.put()
    fido = Dog(name='Fido', parent=bob)
    fido.put()

You can then retrieve fido with::

    fido = Dog.query(ancestor=alice.key).get()


Development
===========

There are two recommended ways to work on this codebase. If you want to keep
one and only one App Engine SDK install, you may clone the repository and run
the tests by::

    $ PYTHONPATH=path/to/appengine/library python setup.py test

Alternatively, this project contains code and support files derived from the
testable_appengine project. Testable_appengine was conceived to make it easier
to write (and run) tests for Google App Engine applications and to hook your
application to Travis CI. In essence, it creates a virtualenv and downloads the
most up-to-date SDK and other support tools into it. To use it, you run
`make`. Calling `make help` will give you a quick list of available make
targets::

    $ make venv
    (lots of output)
    $ source .env/bin/activate
    (.env) $ nosetests
    (hopefully not that much output)
