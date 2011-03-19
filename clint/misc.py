# -*- coding: utf-8 -*-

class Borg(object):
    """All instances of Borg have the same value."""
    _shared_state = {}
    def __new__(cls, *a, **k):
        obj = object.__new__(cls, *a, **k)
        obj.__dict__ = cls._shared_state
        return obj