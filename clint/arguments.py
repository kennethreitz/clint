# -*- coding: utf-8 -*-

import sys
from clint.packages.ordereddict import OrderedDict
from clint.utils import is_collection


class Args(object):
    """CLI Argument management."""

    def __init__(self, args=None):
        if not args:
            self._args = sys.argv[1:]
        else:
            self._args = args


    def __len__(self):
        return len(self._args)


    def __repr__(self):
        return '<args %s>' % (repr(self._args))


    def __getitem__(self, i):
        try:
            return self.all[i]
        except IndexError:
            return None

    def __contains__(self, x):
        return bool(self.first(x))

    def get(self, x):
        try:
            return self.all[x]
        except IndexError:
            return None


    def get_with(self, x):
        return self[self.first_with(x)]


    def remove(self, x):
        """Removes given arg (or list thereof) from Args object."""

        def _remove(x):
            found = self.find(x)
            if found:
                self._args.pop(found)

        if is_collection(x):
            for item in x:
                _remove(x)
        else:
            _remove(x)


    def pop(self, x):
        try:
            return self._args.pop(x)
        except IndexError:
            return None


    def any_contain(self, x):
        """Tests if given object is contained in any stored argument."""
        return bool(self.first_with(x))


    def contains(self, x):
        """Tests if given object is in arguments list. 
           Accepts strings and lists of strings."""
        
        return self.__contains__(x)


    def first(self, x):
        """Returns first found index of given value (or list of values)"""
        
        def _find( x):
            try:
                return self.all.index(str(x))
            except ValueError:
                return None

        if is_collection(x):
            for item in x:
                found = _find(item)
                if found:
                    return found
            return None
        else:
            return _find(x)

    def first_with(self, x):
        """Returns first found index containing value (or list of values)"""

        def _find(x):
            try:
                for arg in self.all:
                    if x in arg:
                        return self.all.index(arg)
            except ValueError:
                return None

        if is_collection(x):
            for item in x:
                found = _find(item)
                if found:
                    return found
            return None
        else:
            return _find(x)


    def first_without(self, x):
        """Returns first found index not containing value (or list of values)"""

        def _find(x):
            try:
                for arg in self.all:
                    if x not in arg:
                        return self.all.index(arg)
            except ValueError:
                return None

        if is_collection(x):
            for item in x:
                found = _find(item)
                if found:
                    return found
            return None
        else:
            return _find(x)

    def contains_at(self, x, index):
        """Tests if given [list of] string is at given index."""

        try:
            if is_collection(x):
                for _x in x:
                    if (_x in self._args[index]) or (_x == self._args[index]):
                        return True
                    else:
                        return False
            else:
                return (x in self._args[index])
        
        except IndexError:
            return False


    def has(self, x):
        """Returns true if argument exists at given index.
           Accepts: integer.
        """
        
        try:
            self._args[x]
            return True
        except IndexError:
            return False


    def value_after(self, x):
        """Returns value of argument after given found argument (or list thereof)."""
        
        try:
            try:
                i = self._args.index(x)
            except ValueError:
                return None
                
            return self._args[i + 1]
            
        except IndexError:
            return None

    @property
    def grouped(self):
        """Extracts --flag groups from argument list.
           Returns {format: [paths], ...}
        """

        collection = OrderedDict(_=list())

        _current_group = None

        for arg in self.all:
            if arg.startswith('-'):
                _current_group = arg
                collection[arg] = []
            else:
                if _current_group:
                    collection[_current_group].append(arg)
                else:
                    collection['_'].append(arg)

        return collection

    @property
    def last(self):
        """Returns last argument."""
        
        try:
            return self.all[-1]
        except IndexError:
            return None

    
    @property
    def all(self):
        """Returns all arguments."""
        
        return self._args


    def all_with(self, x):

        _args = []
        
        for arg in self.all:
            if is_collection(x):
                for _x in x:
                    if _x in arg:
                        _args.append(arg)
                        break
            else:
                if x in arg:
                    _args.append(arg)

        return Args(_args)


    def all_without(self, x):

        _args = []

        for arg in self.all:
            if is_collection(x):
                for _x in x:
                    if _x not in arg:
                        _args.append(arg)
                        break
            else:
                if x not in arg:
                    _args.append(arg)

        return Args(_args)

    @property    
    def no_flags(self):
        """Returns Arg object excluding flagged arguments."""

        return self.all_without('-')

    @property
    def only_flags(self):
        """Returns Arg object excluding non - flagged arguments."""

        return self.all_with(['-', 'fuck'])
        
# TODO: glob expansion
# TODO: support bash expansion


# args.path_expand(list)
# args.

