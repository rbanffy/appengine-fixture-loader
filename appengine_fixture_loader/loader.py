"""
Tools to automate loading of test fixtures
"""

import json
from datetime import datetime, time, date

try:
    from google.appengine.ext.ndb.model import (DateTimeProperty, DateProperty,
                                                TimeProperty)
except:
    raise ImportError("This library needs the Google App Engine SDK installed")


def _sensible_value(attribute_type, value):
    if type(attribute_type) is DateTimeProperty:
        retval = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    elif type(attribute_type) is TimeProperty:
        try:
            dt = datetime.strptime(value, '%H:%M:%S')
        except ValueError:
            dt = datetime.strptime(value, '%H:%M')
        retval = time(dt.hour, dt.minute, dt.second)
    elif type(attribute_type) is DateProperty:
        dt = datetime.strptime(value, '%Y-%m-%d')
        retval = date(dt.year, dt.month, dt.day)
    else:
        retval = value

    return retval


def load_fixture(filename, kind, post_processor=None):
    """
    Loads a file into entities of a given class, run the post_processor on each
    instance before it's saved
    """

    def _loader(kind):
        "Create a loader for this type"

        def _load(od):
            "Load the attributes defined in od into a new object and saves it"
            if hasattr(kind, 'keys'): # kind is a map
                objtype = kind[od['__kind__']]
            else:
                objtype = kind
            obj = objtype()
            for attribute_name in [k for k in od.keys()
                                   if not k.startswith('__') and
                                   not k.endswith('__')]:
                attribute_type = objtype.__dict__[attribute_name]
                attribute_value = _sensible_value(attribute_type,
                                                  od[attribute_name])
                obj.__dict__['_values'][attribute_name] = attribute_value
                if post_processor:
                    post_processor(obj)
            obj.put()
            return obj

        # Returns a function that takes a class and creates a populated
        # instance of it
        return _load

    data = json.load(open(filename), object_hook=_loader(kind=kind))

    return data
