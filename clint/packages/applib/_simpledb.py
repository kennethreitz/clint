# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

"""Simple wrapper around SQLalchemy

This module hides the complexity of SQLAlchemy to provide a simple interface to
store and manipulate Python objects each with a set of properties. Unlike the
default behaviour of sqlalchemy's declaritive_base, inheritance of objects will
not require "join", rather it creates a separate table. This makes it easy to
use objects around from parts of not-so-related applications.

For example, a ``SourcePackage`` table is created by Grail. Then, PyPM will
extend it as ``BinaryPackage`` which gets extended to ``RepoPackage``. The table
for RepoPackage will be concretely inherited, meaning - there will be just be
one table without having to 'join' to another SourcePackage table.

At the moment, PyPM and Grail use this module. It may not be of use to others,
and we may change the api/behaviour. Hence, it makes sense to keep it as an
internal module.
"""

import sys
import os
from os.path import exists, dirname
from contextlib import contextmanager
import json

from sqlalchemy import Table, Column, MetaData
from sqlalchemy import create_engine
from sqlalchemy.types import String, Text, Boolean, PickleType
from sqlalchemy.orm import sessionmaker, scoped_session, mapper


# A PickleType that will work on both Python 2.x and 3.x
# i.e., if you *write* to a DB entry using Python 3.x, we are letting
# Python 3.x apps to read from it as well.
# WARNING: Ideally, if you are starting a new project, please
# use something else like JSON. See
# http://twitter.com/zzzeek/status/9765871731867648
Pickle2Type = PickleType(protocol=2)


def setup(db_class, simple_object_cls, primary_keys):
    """A simple API to configure the metadata"""
    table_name = simple_object_cls.__name__
    column_names = simple_object_cls.FIELDS
    
    metadata = MetaData()
    table = Table(table_name, metadata,
                  *[Column(cname, _get_best_column_type(cname),
                           primary_key=cname in primary_keys)
                    for cname in column_names])

    db_class.metadata = metadata
    db_class.mapper_class = simple_object_cls
    db_class.table = table

    mapper(simple_object_cls, table)
    

def sqlalchemy_escape(val, escape_char, special_chars):
    """Escape a string according for use in LIKE operator

    >>> sqlalchemy_escape("text_table", "\\", "%_")
    'text\_table'
    """
    if sys.version_info[:2] >= (3, 0):
        assert isinstance(val, str)
    else:
        assert isinstance(val, basestring)
    result = []
    for c in val:
        if c in special_chars + escape_char:
            result.extend(escape_char + c)
        else:
            result.extend(c)
    return ''.join(result)


class SimpleDatabase(object):
    metadata = None # to be set up derived classes

    class DoesNotExist(IOError):
        def __init__(self, path):
            super(IOError, self).__init__(
                'database file %s does not exist' % path)
    
    def __init__(self, path, touch=False):
        """
        touch - create database, if it does not exist
        """
        self.path = path
        sqlite_uri = 'sqlite:///%s' % self.path
        self.engine = create_engine(sqlite_uri, echo=False)
        self.create_session = sessionmaker(
            bind=self.engine,
            autocommit=False,

            # See the comment by Michael Bayer
            # http://groups.google.com/group/sqlalchemy/browse_thread/thread/7c1eb642435adde7
            # expire_on_commit=False
        )
        self.create_scoped_session = scoped_session(self.create_session)
        
        if not exists(self.path):
            if touch:
                assert exists(dirname(self.path)), 'missing: ' + dirname(self.path)
                self.metadata.create_all(self.engine)
            else:
                raise self.DoesNotExist(path)

    def reset(self):
        """Reset the database

        Drop all tables and recreate them
        """
        self.metadata.drop_all(self.engine)
        self.metadata.create_all(self.engine)

    def close(self):
        self.engine.dispose()

    @contextmanager
    def transaction(self, session=None):
        """Start a new transaction based on the passed session object. If session
        is not passed, then create one and make sure of closing it finally.
        """
        local_session = None
        if session is None:
            local_session = session = self.create_scoped_session()
        try:
            yield session
        finally:
            # Since ``local_session`` was created locally, close it here itself
            if local_session is not None:
                # but wait!
                # http://groups.google.com/group/sqlalchemy/browse_thread/thread/7c1eb642435adde7
                # To workaround this issue with sqlalchemy, we can either:
                #  1) pass the session object explicitly
                #  2) do not close the session at all (bad idea - could lead to memory leaks)
                #
                # Till pypm implements atomic transations in client.installer,
                # we retain this hack (i.e., we choose (2) for now)
                pass # local_session.close()

    def __str__(self):
        return '{0.__class__.__name__}<{0.path}>'.format(self)


class SimpleObject(object):
    """Object with a collection of fields.

    The following features are supported:

      1) Automatically initialize the fields in __init__
      2) Inherit and extend with additional fields
      2) Ability to convert from other object types (with extra/less fields)
      3) Interoperate with sqlalchemy.orm (i.e., plain `self.foo=value` works)
    """

    # Public fields in this object
    FIELDS = []

    def __init__(self, **kwargs):
        """Initialize the object with FIELDS whose values are in ``kwargs``"""
        self.__assert_field_mapping(kwargs)
        for field in self.FIELDS:
            setattr(self, field, kwargs[field])

    @classmethod
    def create_from(cls, another, **kwargs):
        """Create from another object of different type.

        Another object must be from a derived class of SimpleObject (which
        contains FIELDS)
        """
        reused_fields = {}
        for field, value in another.get_fields():
            if field in cls.FIELDS:
                reused_fields[field] = value
        reused_fields.update(kwargs)
        return cls(**reused_fields)

    def get_fields(self):
        """Return fields as a list of (name,value)"""
        for field in self.FIELDS:
            yield field, getattr(self, field)

    def to_dict(self):
        return dict(self.get_fields())
        
    def to_json(self):
        return json.dumps(self.to_dict())
        
    @classmethod
    def from_json(cls, json_string):
        values = json.loads(json_string)
        return cls(**_remove_unicode_keys(values))
    
    def __assert_field_mapping(self, mapping):
        """Assert that mapping.keys() == FIELDS.
        
        The programmer is not supposed to pass extra/less number of fields
        """
        passed_keys = set(mapping.keys())
        class_fields = set(self.FIELDS)
        
        if passed_keys != class_fields:
            raise ValueError('\n'.join([
                "{0} got different fields from expected".format(
                    self.__class__),
                "  got     : {0}".format(list(sorted(passed_keys))),
                "  expected: {0}".format(list(sorted(class_fields)))]))


class _get_best_column_type():
    """Return the best column type for the given name."""
    mapping = dict(
        name               = String,
        version            = String,
        keywords           = String,
        home_page          = String,
        license            = String,
        author             = String,
        author_email       = String,
        maintainer         = String,
        maintainer_email   = String,
        osarch             = String,
        pyver              = String,
        pkg_version        = String,
        relpath            = String,
        tags               = String,
        original_source    = String,
        patched_source     = String,
        
        summary            = Text,
        description        = Text,
        
        python3            = Boolean,
        metadata_hash      = String,
        
        install_requires   = Pickle2Type,
        files_list         = Pickle2Type,
    )
    
    def __call__(self, name):
        try:
            return self.mapping[name]
        except KeyError:
            raise KeyError(
                'missing key. add type for "{0}" in self.mapping'.format(
                name))
_get_best_column_type = _get_best_column_type()


def _remove_unicode_keys(dictobj):
    """Convert keys from 'unicode' to 'str' type.

    workaround for <http://bugs.python.org/issue2646>
    """
    if sys.version_info[:2] >= (3, 0): return dictobj

    assert isinstance(dictobj, dict)

    newdict = {}
    for key, value in dictobj.items():
        if type(key) is unicode:
            key = key.encode('utf-8')
        newdict[key] = value
    return newdict
