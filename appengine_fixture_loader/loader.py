"""
Tools to automate loading of test fixtures
"""

import json
from datetime import datetime, time, date

from google.appengine.ext.ndb.model import (DateTimeProperty, DateProperty,
                                            TimeProperty)


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

    def _load(od, kind, post_processor, parent=None, presets={}):
        """
        Loads a single dictionary (od) into an object, overlays the values in
        presets, persists it and
        calls itself on the objects in __children__* keys
        """
        if hasattr(kind, 'keys'):  # kind is a map
            objtype = kind[od['__kind__']]
        else:
            objtype = kind

        obj_id = od.get('__id__')
        if obj_id is not None:
            obj = objtype(id=obj_id, parent=parent)
        else:
            obj = objtype(parent=parent)

        # Iterate over the non-special attributes and overlay the presets
        for attribute_name in [k for k in od.keys()
                               if not k.startswith('__') and
                               not k.endswith('__')] + presets.keys():
            attribute_type = objtype.__dict__[attribute_name]
            attribute_value = _sensible_value(attribute_type,
                                              presets.get(
                                                  attribute_name,
                                                  od.get(attribute_name)))
            obj.__dict__['_values'][attribute_name] = attribute_value

        if post_processor:
            post_processor(obj)

        # Saving obj is required to continue with the children
        obj.put()

        loaded = [obj]

        # Process ancestor-based __children__
        for item in od.get('__children__', []):
            loaded.extend(_load(item, kind, post_processor, parent=obj.key))

        # Process other __children__[key]__ items
        for child_attribute_name in [k for k in od.keys()
                                     if k.startswith('__children__')
                                     and k != '__children__']:
            attribute_name = child_attribute_name.split('__')[-2]

            for child in od[child_attribute_name]:
                loaded.extend(_load(child, kind, post_processor,
                                    presets={attribute_name: obj.key}))

        return loaded

    tree = json.load(open(filename))

    loaded = []

    # Start with the top-level of the tree
    for item in tree:
        loaded.extend(_load(item, kind, post_processor))

    return loaded
